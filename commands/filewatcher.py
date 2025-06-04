# commands/filewatcher.py

import json
import os
from state import get_symbol_state, set_symbol_state
from order import submit_order
from utils.logging import log
from config import DEFAULT_QTY

COMMAND_FILE = "commands.json"

def handle_command(cmd):
    symbol = cmd.get("symbol")
    action = cmd.get("action")

    if not symbol or not action:
        log("Invalid command format", "COMMAND")
        return

    state = get_symbol_state(symbol)

    if action == "pause":
        state["paused"] = True
        log(f"{symbol} paused – No further signals processed", "ACTION")

    elif action == "buy":
        qty = cmd.get("qty", DEFAULT_QTY)
        submit_order(symbol, "BUY")  # optional: submit_order(symbol, "BUY", qty)
        log(f"{symbol} manual BUY {qty} submitted", "COMMAND")

    elif action == "resume":
        state["paused"] = False
        log(f"{symbol} resumed – Signal processing active", "ACTION")

    set_symbol_state(symbol, state)

def watch_command_file():
    if not os.path.exists(COMMAND_FILE):
        return

    try:
        with open(COMMAND_FILE, "r", encoding="utf-8") as f:
            commands = json.load(f)
            for cmd in commands:
                handle_command(cmd)

        os.remove(COMMAND_FILE)
        log("commands.json verarbeitet und gelöscht", "CLEANUP")

    except (json.JSONDecodeError, OSError) as e:
        log(f"Error processing commands.json: {e}", "COMMAND")
