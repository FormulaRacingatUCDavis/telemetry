import shutil
import can
import cantools
import os
from pathlib import Path
from .settings import settings

import pandas as pd
from fpdf import FPDF

class CANHelper:
    """
    Handles any analysis or retrieval relating to CAN data
    """
    def __init__(self):
        dbc_dir = Path(settings.dbc_dir)

        self.dbs = []
        for dbc_path in dbc_dir.glob("*.dbc"):
            self.dbs.append(cantools.db.load_file(dbc_path))

    def process_candump(self, path: str):
        """
        Processes vehicle CAN bus data to generate a human-readable CSV and PDF report
        """
        decoded_msgs = []
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
                    decoded = message.decode(msg.data)
                except (ValueError, cantools.database.DecodeError) as e:
                    print(f'[LOG PARSER] >> Failed to decode {msg.arbitration_id:X}: {e}')
                    f_count += 1
                    continue

                decoded_msgs.append((
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

        for timestamp, source, id, msg_name, decoded in decoded_msgs:
            msg = {
                "Timestamp [s]": timestamp,
                "Source": source,
                "ID": id,
                "Message": msg_name,
            }
            msg.update(decoded)
            data.append(msg)

        log_name = Path(log.replace('candump', 'FE14')).stem
        df = pd.DataFrame(
            data,
            columns = ["Timestamp [s]", "Source", "ID", "Message"] + signals_list
        )

        df.to_csv(os.path.join(settings.can_processed_path, log_name + '.csv'), index=False)
        self.generate_report(df, log_name)
        
        print(f'[LOG PARSER] >> Total failed rows: {f_count}')
        shutil.move(path, os.path.join(settings.can_raw_path, log))

    def generate_report(self, df, log):
        """
        Generate post-run PDF report
        """
        report_path = Path(settings.can_reports_path)
        report_path.mkdir(parents=True, exist_ok=True)
        pdf = FPDF()
        pdf.add_page()
        
        pdf.set_font('Helvetica', style='B')
        pdf.cell(0, 15, f"FRUCD Track Day Report: {log}", align='C', new_x='LMARGIN', new_y='NEXT')

        pdf.cell(0, 15, text='Run Summary', new_x='LMARGIN', new_y='NEXT')
        # Table with CAN bus health metrics

        pdf.cell(0, 15, text='CAN Bus Health', new_x='LMARGIN', new_y='NEXT')
        # Table with CAN bus health metrics

        pdf.cell(0, 15, text='Vehicle Performance', new_x='LMARGIN', new_y='NEXT')
        # Table with CAN bus health metrics

        pdf.cell(0, 15, text='Raspberry Pi Performance', new_x='LMARGIN', new_y='NEXT')
        # Table with CAN bus health metrics

        pdf.output(str(report_path / f'{log}.pdf'))