from threading import Thread, Event
import time

from config import SYMBOLS
ENV_INFO = {}
from dashboard import Dashboard
from commands.terminal import handle_terminal
from strategy import run_strategy
from state import get_symbol_state
from utils.logging import log

# Globales Stop-Event
stop_event = Event()

# Dashboard initialisieren
dashboard = Dashboard(SYMBOLS, stop_event)

def update_dashboard():
    dashboard.set_system_info(ENV_INFO)
    dashboard.set_actions(log.tail(10))
    for symbol in SYMBOLS:
        state = get_symbol_state(symbol)
        dashboard.update_symbol(
            symbol,
            paused=state.get("paused", False),
            order="🟢" if state.get("order_active") else "–",
            signal="–",
            price="–",
            rsi="–"
        )

def strategy_loop():
    while not stop_event.is_set():
        run_strategy()
        update_dashboard()
        time.sleep(5)

def dashboard_loop():
    while not stop_event.is_set():
        dashboard.run(update_dashboard)
        time.sleep(15)

# Starte alle Threads
Thread(target=handle_terminal, args=(stop_event,), daemon=True).start()
Thread(target=dashboard_loop, daemon=True).start()
Thread(target=strategy_loop, daemon=True).start()

# Hauptthread wartet auf Stop
stop_event.wait()
print("✅ Bot wurde beendet.")
