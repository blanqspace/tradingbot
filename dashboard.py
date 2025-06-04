# dashboard.py
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from utils.logging import log
from time import sleep

class Dashboard:
    def __init__(self, symbols, stop_event):
        self.symbols = symbols
        self.stop_event = stop_event
        self.data = {s: {"paused": False, "order": "–", "signal": "–", "price": "–", "rsi": "–"} for s in symbols}
        self.system_info = {}
        self.actions = []

    def update_symbol(self, symbol, paused=None, order=None, signal=None, price=None, rsi=None):
        if symbol not in self.data:
            return
        if paused is not None:
            self.data[symbol]["paused"] = paused
        if order is not None:
            self.data[symbol]["order"] = order
        if signal is not None:
            self.data[symbol]["signal"] = signal
        if price is not None:
            self.data[symbol]["price"] = price
        if rsi is not None:
            self.data[symbol]["rsi"] = rsi

    def set_system_info(self, info_dict):
        self.system_info = info_dict

    def set_actions(self, actions):
        self.actions = actions[-5:]

    def log_action(self, text):
        self.actions.append(text)
        self.actions = self.actions[-5:]

    def render_system_info(self):
        table = Table.grid(expand=True)
        table.add_column()
        table.add_column(justify="right")
        for key, value in self.system_info.items():
            if isinstance(value, bool):
                value = "✅" if value else "❌"
            table.add_row(key, str(value))
        return Panel(table, title="🧐 Systeminformationen", border_style="cyan")

    def render_table(self):
        table = Table(title="📊 TradingBot Status", expand=True)
        table.add_column("Symbol")
        table.add_column("Paused")
        table.add_column("Order")
        table.add_column("Signal")
        table.add_column("Price")
        table.add_column("RSI")
        for s in self.symbols:
            d = self.data[s]
            table.add_row(
                s,
                "✅" if d["paused"] else "❌",
                d["order"],
                d["signal"],
                str(d["price"]),
                str(d["rsi"]),
            )
        return table

    def render_actions(self):
        actions_text = "\n".join(self.actions or ["Keine Aktionen bisher."])
        return Panel(actions_text, title="📝 Letzte Aktionen")

    def render(self):
        layout = Layout()
        layout.split_column(
            Layout(name="top", size=5),
            Layout(name="middle", ratio=2),
            Layout(name="bottom", size=10)
        )
        layout["top"].update(self.render_system_info())
        layout["middle"].update(self.render_table())
        layout["bottom"].update(self.render_actions())
        return layout

    def run(self, update_fn):
        with Live(self.render(), refresh_per_second=1, screen=True, console=log.console) as live:
            try:
                while not self.stop_event.is_set():
                    update_fn()
                    live.update(self.render())
                    sleep(1)
            except KeyboardInterrupt:
                self.stop_event.set()
