import shutil
import can
import cantools
import os
import csv
from pathlib import Path
from .settings import settings

class CANHelper:
    """
    Handles any analysis or retrieval relating to CAN data
    """
    def __init__(self, config):
        self.config = config

        dbc_dir = Path(settings.dbc_dir)

        self.dbs = []

        for dbc_path in dbc_dir.glob("*.dbc"):
            self.dbs.append(cantools.db.load_file(dbc_path))

    def generate_parsed(self, path: str):
        parsed_msgs = []
        ids = set()
        signals = set()
        f_ids = set()
        f_count = 0

        log = os.path.basename(path)
        print(f'[LOG PARSER] Parsing {log}...')

        with can.LogReader(path) as reader:
            for msg in reader:
                message = None

                for db in self.dbs:
                    try:
                        message = db.get_message_by_frame_id(msg.arbitration_id)
                        break
                    except KeyError:
                        continue

                if message is None:
                    print(f'[LOG PARSER] >> Unrecognized ID {msg.arbitration_id:X} at timestamp: {msg.timestamp}')
                    f_ids.add(msg.arbitration_id)
                    f_count += 1
                    continue

                try:
                    parsed_data = message.decode(msg.data)
                except (ValueError, cantools.database.DecodeError) as e:
                    print(f'[LOG PARSER] >> Failed to decode {msg.arbitration_id:X}: {e}')
                    f_count += 1
                    continue

                id_str = f'{msg.arbitration_id:X}'

                parsed_msgs.append((
                    msg.timestamp,
                    message.senders[0] if message.senders else "Unknown",
                    id_str,
                    message.name,
                    parsed_data
                ))

                ids.add(id_str)

                for signal in message.signals:
                    signals.add(signal.name)

        parsed_path = os.path.join(settings.can_parsed_path, Path(log).with_suffix('.csv'))
        with open(parsed_path, 'w', newline='') as log_parsed:
            signals_list = sorted(signals)
            header = ['Timestamp [s]', 'Source', 'ID', 'Message'] + signals_list

            writer = csv.writer(log_parsed)
            writer.writerow(header)

            for timestamp, source, id_str, msg_name, decoded in parsed_msgs:
                row_data = [timestamp, source, id_str, msg_name]

                for sig in signals_list:
                    row_data.append(decoded.get(sig, ""))

                writer.writerow(row_data)

        print(f'[LOG PARSER] >> Total failed rows: {f_count}')

        shutil.move(path, os.path.join(settings.can_raw_path, log))

    def get_messages(self, dbc_path):
        db = cantools.db.load_file(dbc_path)
        dbc_name = Path(dbc_path).name

        messages = {}
        for message in db.messages:
            sender = message.senders[0].lower()
            if sender not in messages:
                messages[sender] = {}
            messages[sender][message.name.lower()] = {
                "id": message.frame_id,
                "signals": [signal.name.lower() for signal in message.signals]
            }

        return {dbc_name: messages}