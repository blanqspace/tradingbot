# state.py
import json
import os
from utils.logging import log

STATE_FILE = "data/recovery.json"
_state = {}

def get_symbol_state(symbol):
    if symbol not in _state:
        _state[symbol] = {
            "paused": False,
            "order_active": False,
            "last_signal": None,
            "last_price": None,
            "last_rsi": None,
        }
    return _state[symbol]

def set_symbol_state(symbol, state):
    _state[symbol] = state

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                loaded_state = json.load(f)
                _state.clear()
                _state.update(loaded_state)
            log("State aus recovery.json geladen", "STATE")
        except (OSError, json.JSONDecodeError) as e:
            log(f"Fehler beim Laden von {STATE_FILE}: {e}", "ERROR")
    else:
        log("Keine bestehende recovery.json gefunden – neuer Zustand wird erstellt", "STATE")

def save_state():
    try:
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(_state, f, indent=2)
        log("State in recovery.json gespeichert", "STATE")
    except (OSError, TypeError) as e:
        log(f"Fehler beim Speichern von {STATE_FILE}: {e}", "ERROR")

# Wichtig: Damit recovery.py den Zustand sehen kann
state_data = _state
