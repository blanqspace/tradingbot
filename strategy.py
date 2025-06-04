# strategy.py
import time
import random
from config import SYMBOLS
from state import get_symbol_state, set_symbol_state
from order import submit_order
from commands.telegram import send_signal_notification
from dashboard import Dashboard

dashboard: Dashboard | None = None  # wird im main.py gesetzt

def set_dashboard(instance: Dashboard):
    global dashboard
    dashboard = instance

# Zufälliger Signalgenerator
def check_signal(_symbol):
    signal = random.choice(["BUY", "SELL", "HOLD"])
    price = round(random.uniform(100, 200), 2)
    rsi = round(random.uniform(30, 80), 2)
    return signal, price, rsi

# Hauptstrategie
def run_strategy():
    for symbol in SYMBOLS:
        state = get_symbol_state(symbol)
        if state.get("paused"):
            if dashboard:
                dashboard.update_symbol(symbol, paused=True)
            continue

        signal, price, rsi = check_signal(symbol)

        if dashboard:
            dashboard.update_symbol(symbol, paused=False, signal=signal, price=price, rsi=rsi)

        if state.get("order_active"):
            continue

        # Order auslösen
        submit_order(symbol, signal)
        state["order_active"] = True
        state["last_signal"] = signal
        set_symbol_state(symbol, state)

        # Telegram & Konsole
        send_signal_notification(symbol, signal, price, rsi)
        if dashboard:
            dashboard.log_action(f"{symbol} → {signal} {price} (RSI: {rsi})")

        time.sleep(1)
