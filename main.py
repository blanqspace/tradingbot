import os
import platform
import threading
import time
from dotenv import load_dotenv
from config import SYMBOLS
from recovery import load_state, save_state
from state import get_symbol_state
import strategy
from utils.logging import log
from dashboard import Dashboard
from commands.terminal import handle_terminal

# Stopp-Signal für alle Threads
stop_event = threading.Event()

# 1. Systeminfos laden
load_dotenv()

ENV_INFO = {
    ".env vorhanden": os.path.exists(".env"),
    "Telegram aktiv": bool(os.getenv("TELEGRAM_TOKEN")),
    "Chat-ID geladen": bool(os.getenv("TELEGRAM_CHAT_ID")),
    "Python": platform.python_version(),
    "OS": f"{platform.system()} {platform.release()}"
}

# 2. Bot-Initialisierung
load_state()

dashboard = Dashboard(SYMBOLS, stop_event)
strategy.set_dashboard(dashboard)

def update_dashboard():
    for symbol in SYMBOLS:
        state = get_symbol_state(symbol)
        dashboard.update_symbol(
            symbol,
            paused=state.get("paused"),
            order="🟢" if state.get("order_active") else "⚪",
            signal=state.get("last_signal") or "–",
            price=state.get("last_price") or "–",
            rsi=state.get("last_rsi") or "–",
        )

    dashboard.set_system_info(ENV_INFO)
    dashboard.set_actions(log.tail(5))
    save_state()

def strategy_loop():
    while not stop_event.is_set():
        strategy.run_strategy()
        update_dashboard()
        time.sleep(5)

def run():
    t1 = threading.Thread(target=strategy_loop)
    t2 = threading.Thread(target= handle_terminal, args=(stop_event,))

    t1.start()
    t2.start()

    try:
        dashboard.run(update_dashboard)
    except KeyboardInterrupt:
        stop_event.set()
        print("\n🔚 Programm durch STRG+C beendet.")

    t1.join()
    t2.join()

if __name__ == "__main__":
    run()
