'''
Local CLI Dashboard
~~~~~~~~~~~~~~~~~~

Terminal-based real-time monitoring of LordRequests operations.
'''

import time
import threading
from typing import List, Dict, Any
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

class DashboardStats:
    total_requests = 0
    successful_requests = 0
    failed_requests = 0
    active_sessions = 0
    avg_latency = 0
    recent_logs: List[str] = []

    @classmethod
    def log(cls, message: str):
        cls.recent_logs.append(f"[{time.strftime('%H:%M:%S')}] {message}")
        if len(cls.recent_logs) > 10:
            cls.recent_logs.pop(0)

class CLIDashboard:
    def __init__(self):
        self.console = Console()
        self.layout = Layout()
        self.is_running = False

    def create_layout(self) -> Layout:
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        self.layout["main"].split_row(
            Layout(name="stats", ratio=1),
            Layout(name="logs", ratio=2)
        )
        return self.layout

    def get_stats_panel(self) -> Panel:
        table = Table.grid(expand=True)
        table.add_column(style="cyan", justify="left")
        table.add_column(style="magenta", justify="right")
        
        table.add_row("Total Requests", str(DashboardStats.total_requests))
        table.add_row("Success Ratio", f"{(DashboardStats.successful_requests / (DashboardStats.total_requests or 1)) * 100:.1f}%")
        table.add_row("Active Sessions", str(DashboardStats.active_sessions))
        table.add_row("Avg Latency", f"{DashboardStats.avg_latency}ms")
        
        return Panel(table, title="Operational Stats", border_style="blue")

    def get_logs_panel(self) -> Panel:
        log_text = "\n".join(DashboardStats.recent_logs)
        return Panel(log_text, title="Live Activity Logs", border_style="green")

    def run(self):
        self.is_running = True
        layout = self.create_layout()
        self.layout["header"].update(Panel("LordRequests Operational Dashboard", style="bold white on blue"))
        self.layout["footer"].update(Panel("Press Ctrl+C to exit", style="dim"))

        with Live(self.layout, refresh_per_second=4, console=self.console):
            try:
                while self.is_running:
                    self.layout["stats"].update(self.get_stats_panel())
                    self.layout["logs"].update(self.get_logs_panel())
                    time.sleep(0.25)
            except KeyboardInterrupt:
                self.is_running = False

    def start_in_background(self):
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
        return thread
