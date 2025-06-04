# order.py
from utils.logging import log
from state import get_symbol_state, set_symbol_state
from config import DEFAULT_QTY

def submit_order(symbol, side):
    state = get_symbol_state(symbol)
    
    # Prüfen, ob bereits eine Order aktiv ist
    if state.get("order_active"):
        log(f"{symbol} hat bereits eine aktive Order – übersprungen", "ORDER")
        return

    # Beispiel: Simulierte Order-Ausgabe
    log(f"{symbol} {side} {DEFAULT_QTY} @ market submitted", "ORDER")
    
    # Zustand aktualisieren
    state["order_active"] = True
    set_symbol_state(symbol, state)
