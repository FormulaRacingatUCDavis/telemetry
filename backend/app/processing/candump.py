import can
import cantools
import os
from pathlib import Path
from ..core.settings import settings
import pandas as pd

class Analyzer:
    def __init__(self):
        """
        Decodes CANDump logs and handles data preprocessing
        """
        self.data = None
        self.dbs = []
        self.failed = set() # Change to DataFrame

        for dbc_path in Path(settings.DBC_DIR).glob("*.dbc"):
            self.dbs.append(cantools.db.load_file(dbc_path))

    def decode(self, path: str):
        messages = []
        signals = set()
        failed = set()

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
                    failed.add(msg.arbitration_id)
                    continue

                try:
                    decoded = message.decode(msg.data)
                except (ValueError, cantools.database.DecodeError) as e:
                    print(f'[LOG PARSER] >> Failed to decode {msg.arbitration_id:X}: {e}')
                    continue

                messages.append((
                    msg.timestamp,
                    message.senders[0] if message.senders else "Unknown",
                    f'{msg.arbitration_id:X}',
                    message.name,
                    decoded
                ))

                for signal in message.signals:
                    signals.add(signal.name)

        signals_list = sorted(signals)
        data = []

        for timestamp, source, id, msg_name, decoded in messages:
            msg = {
                "Timestamp [s]": timestamp,
                "Source": source,
                "ID": id,
                "Message": msg_name,
            }
            msg.update(decoded)
            data.append(msg)

        self.data = pd.DataFrame(data, columns = ["Timestamp [s]", "Source", "ID", "Message"] + signals_list)