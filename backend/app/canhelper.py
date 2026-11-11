import shutil
import can
import cantools
import os
from pathlib import Path
from .settings import settings

import pandas as pd

class CANHelper:
    """
    Handles any analysis or retrieval relating to CAN data
    """
    def __init__(self):
        dbc_dir = Path(settings.dbc_dir)

        self.dbs = []
        for dbc_path in dbc_dir.glob("*.dbc"):
            self.dbs.append(cantools.db.load_file(dbc_path))

    def generate_parsed(self, path: str):
        parsed_msgs = []
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

                parsed_msgs.append((
                    msg.timestamp,
                    message.senders[0] if message.senders else "Unknown",
                    f'{msg.arbitration_id:X}',
                    message.name,
                    parsed_data
                ))

                for signal in message.signals:
                    signals.add(signal.name)

        signals_list = sorted(signals)
        data = []

        for timestamp, source, id, msg_name, decoded in parsed_msgs:
            msg = {
                "Timestamp [s]": timestamp,
                "Source": source,
                "ID": id,
                "Message": msg_name,
            }
            msg.update(decoded)
            data.append(msg)

        df = pd.DataFrame(
            data,
            columns = ["Timestamp [s]", "Source", "ID", "Message"] + signals_list
        )
        df.to_csv(os.path.join(settings.can_parsed_path, Path(log).with_suffix('.csv')).replace('candump', 'FE14'), index=False)

        # Generate PDF report
        
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