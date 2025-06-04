import threading
import time
from config import SYMBOLS  # Removed ENV_INFO as it is not present in config

# If ENV_INFO is defined elsewhere, import it from the correct module or define it here.
# For example, if ENV_INFO should be a dictionary with environment info, you can define:
ENV_INFO = {}
from strategy import run_strategy, set_dashboard
from dashboard import Dashboard
from commands.terminal import handle_terminal
from state import get_symbol_state, load_state, save_state
from utils.logging import log

stop_event = threading.Event()

def update_dashboard():
    dashboard.set_system_info(ENV_INFO)
    dashboard.set_actions(log.tail(10))
    for symbol in SYMBOLS:
        state = get_symbol_state(symbol)
        dashboard.update_symbol(
            symbol,
            paused=state.get("paused"),
            order=state.get("order_active"),
            signal=state.get("signal", "–"),
            price=state.get("price", "–"),
            rsi=state.get("rsi", "–")
        )

def strategy_loop():
    while not stop_event.is_set():
        run_strategy()
        update_dashboard()
        time.sleep(5)

def dashboard_loop():
    dashboard.run(update_dashboard)

if __name__ == "__main__":
    print(".env vorhanden:", ENV_INFO.get(".env vorhanden"))
    print("Telegram aktiv:", ENV_INFO.get("Telegram aktiv"), "Token geladen:", ENV_INFO.get("Token geladen"), "Chat-ID geladen:", ENV_INFO.get("Chat-ID geladen"))

    load_state()

    dashboard = Dashboard(SYMBOLS, stop_event)
    set_dashboard(dashboard)

    t1 = threading.Thread(target=strategy_loop)
    t2 = threading.Thread(target=dashboard_loop)
    t3 = threading.Thread(target=handle_terminal, args=(stop_event,))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    save_state()
    print("\nBot wurde beendet.")
