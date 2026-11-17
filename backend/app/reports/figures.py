import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

class CANFigs:
    def __init__(self, df, log):
        """
        Plotly figures for CAN bus data analysis
        """
        self.df = df
        self.log = log

    def bus_loads(self):
        """
        Plots of CAN bus loads over time
        """
        fig = make_subplots(rows=1, cols=2, subplot_titles=("PCAN Bus Load [%]", "TCAN Bus Load [%]"))

        fig.add_trace(
            go.Scatter(x=[1, 2, 3], y=[4, 5, 6]),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=[20, 30, 40], y=[50, 60, 70]),
            row=1, col=2
        )
        
        fig.update_layout(title_text=f"{self.log}: CAN Bus Loads")

        return fig

    def bus_summary(self):
        """
        Table of CAN bus network data
        """
        fig = go.Figure(data=[
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

        fig.update_layout(title=f"{self.log}: CAN Bus Networks")

        return fig

    def scatter(self):
        """
        Scatter plot
        """
        return px.scatter(
                self.df.dropna(subset=["INV_Motor_Speed"]),
                x=self.df.dropna(subset=["INV_Motor_Speed"])["Timestamp [s]"] - self.df["Timestamp [s]"].min(),
                y="INV_Motor_Speed",
                title=f"{self.log}: Motor Speed",
                labels={"x": "Elapsed Time [s]", "INV_Motor_Speed": "Motor Speed [RPM]"}
            )

    def failed(self):
        """
        Table of CAN IDs that were not recognized or were not formatted properly along with their timestamps
        """
        pass

class RPiFigs:
    def __init__(self, df, log):
        """
        Plotly figures for Raspberry Pi performance analysis
        """
        self.df = df
        self.log = log

    def rpi_table(self):
        """
        Table of Raspberry Pi performance data
        """
        fig = go.Figure(data=[
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
        fig.update_layout(title=f"{self.log}: System Performance", height=600)

        return fig