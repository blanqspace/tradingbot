# recovery.py
import json
import os
from utils.logging import log
from state import state_data  # ← wichtig!

RECOVERY_FILE = "data/recovery.json"  # Passe den Pfad an, falls nötig

def save_state():
    with open(RECOVERY_FILE, "w", encoding="utf-8") as f:
        json.dump(state_data, f, indent=2)
    log("State saved to recovery.json", "RECOVERY")

def load_state():
    if os.path.exists(RECOVERY_FILE):
        with open(RECOVERY_FILE, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        state_data.update(loaded_data)
        log("State loaded from recovery.json", "RECOVERY")
