from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from time import sleep

class Dashboard:
    def __init__(self, symbols, stop_event):
        self.symbols = symbols
        self.stop_event = stop_event
        self.data = {s: {"paused": False, "order": False, "signal": "–", "price": "–", "rsi": "–"} for s in symbols}
        self.system_info = {}
        self.actions = []
        self.console = Console()

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
        self.actions = actions[-10:]

    def render(self):
        lines = []
        lines.append("=== SYSTEM ===")
        for k, v in self.system_info.items():
            lines.append(f"{k}: {v}")

        lines.append("\n=== SYMBOLSTATUS ===")
        for s in self.symbols:
            d = self.data[s]
            status = f"{s}: {d['signal']} | Price: {d['price']} | RSI: {d['rsi']} | Order: {'🟢' if d['order'] else '–'} | Paused: {d['paused']}"
            lines.append(status)

        lines.append("\n=== LETZTE AKTIONEN ===")
        if self.actions:
            for a in self.actions:
                lines.append(f"- {a}")
        else:
            lines.append("(Keine Aktionen)")

        lines.append("\n⌨ Befehle: /pause SYMBOL, /resume SYMBOL, /buy SYMBOL, /status, r, exit")
        return Panel(Text("\n".join(lines)))

    def run(self, update_fn):
        with Live(self.render(), refresh_per_second=1, screen=True) as live:
            while not self.stop_event.is_set():
                update_fn()
                live.update(self.render())
                sleep(1)
