import shutil
import can
import cantools
import os
from pathlib import Path
from .settings import settings

import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from jinja2 import Environment, FileSystemLoader

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
        Generate an interactive HTML report
        """
        report_path = Path(settings.can_reports_path)
        report_path.mkdir(parents=True, exist_ok=True)

        template_dir = Path(__file__).resolve().parent / "templates"
        env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)
        template = env.get_template("report.html")

        # CALCULATE CAN BUS LOADS, FREQUENCIES, COUNT, JITTER

        busPlots = make_subplots(rows=1, cols=2, subplot_titles=("PCAN Bus Load [%]", "TCAN Bus Load [%]"))
        busPlots.add_trace(
            go.Scatter(x=[1, 2, 3], y=[4, 5, 6]),
            row=1, col=1
        )
        busPlots.add_trace(
            go.Scatter(x=[20, 30, 40], y=[50, 60, 70]),
            row=1, col=2
        )
        busPlots.update_layout(title_text=f"{log}: CAN Bus Loads")

        canTable = go.Figure(data=[
            go.Table(
                header=dict(values=["ID", "Source", "Frequency [Hz]", "Count", "Jitter [s]"]),
                cells=dict(values=[
                    [hex(0x766), hex(0x381)],
                    ["VCU", "PEI"],
                    ["Not yet available"] * 2,
                    ["Not yet available"] * 2,
                    ["Not yet available"] * 2,
                ])
            )
        ])
        canTable.update_layout(title=f"{log}: CAN Bus Networks")

        # LOG RASPBERRY PI SYSTEM PERFORMANCE DATA AND LOAD INTO PANDAS DATAFRAME

        sysTable = go.Figure(data=[
            go.Table(
                header=dict(values=["Metric", "Value"]),
                cells=dict(values=[
                    [
                        "CPU Utilization [%]",
                        "CPU Load Average (1 min)",
                        "Memory Utilization [%]",
                        "Available Memory [MB]",
                        "Swap Utilization [%]",
                        "Disk Read Throughput [KB/s]",
                        "Disk Write Throughput [KB/s]",
                        "Disk I/O Latency [ms]",
                        "Network RX [KB/s]",
                        "Network TX [KB/s]",
                        "Network Errors",
                        "SoC Temperature [°C]",
                        "ARM Clock Frequency [MHz]",
                        "Core Voltage [V]",
                        "Undervoltage Events",
                        "Thermal Throttling Events"
                    ],
                    ["Not yet available"] * 16
                ])
            )
        ])
        sysTable.update_layout(title=f"{log}: System Performance", height=600)

        figs = [
            busPlots,
            canTable,
            px.scatter(
                df.dropna(subset=["INV_Motor_Speed"]),
                x=df.dropna(subset=["INV_Motor_Speed"])["Timestamp [s]"] - df["Timestamp [s]"].min(),
                y="INV_Motor_Speed",
                title=f"{log}: Motor Speed",
                labels={"x": "Elapsed Time [s]", "INV_Motor_Speed": "Motor Speed [RPM]"}
            ),
            sysTable
        ]

        plots = []
        for i, fig in enumerate(figs):
            plots.append(
                fig.to_html(
                    full_html=False,
                    include_plotlyjs=(i == 0),
                    config={
                        "responsive": True,
                        "toImageButtonOptions": {
                            "format": "png",
                            "scale": 2
                        }
                    }
                )
            )

        html = template.render(title=log, plots=plots)
        output = report_path / f"{log}.html"
        output.write_text(html, encoding="utf-8")