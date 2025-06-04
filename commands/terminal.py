from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from state import get_symbol_state, set_symbol_state
from order import submit_order

# Liste erlaubter Befehle
COMMANDS = ["/buy", "/pause", "/resume", "/status", "/clear", "/help", "exit"]

def help_text():
    return """📋 Verfügbare Terminal-Befehle:
  /status SYMBOL      → Zeigt Status eines Symbols (z. B. /status AAPL)
  /pause SYMBOL       → Pausiert ein Symbol (z. B. /pause TSLA)
  /resume SYMBOL      → Reaktiviert ein Symbol
  /clear SYMBOL       → Setzt Orderstatus zurück
  /buy SYMBOL         → Manuelle Kauforder
  /help               → Zeigt diese Hilfe erneut
  exit                → Beendet das Programm"""

def process_command(cmd_input: str) -> str:
    parts = cmd_input.split()
    if not parts:
        return ""

    cmd = parts[0].lower()
    args = parts[1:]

    if cmd not in COMMANDS:
        return f"❌ Unbekannter Befehl: {cmd}"

    if cmd == "/help":
        return help_text()

    if cmd == "exit":
        return "🔚 Programm wird beendet. STRG+C drücken."

    if len(args) != 1:
        return "⚠️ Bitte genau ein Symbol angeben. Beispiel: /pause AAPL"

    symbol = args[0].upper()
    state = get_symbol_state(symbol)

    if cmd == "/status":
        return f"{symbol} – Paused: {state.get('paused')}, Order aktiv: {state.get('order_active')}"

    elif cmd == "/pause":
        state["paused"] = True
        set_symbol_state(symbol, state)
        return f"{symbol} wurde pausiert."

    elif cmd == "/resume":
        state["paused"] = False
        set_symbol_state(symbol, state)
        return f"{symbol} wurde reaktiviert."

    elif cmd == "/clear":
        state["order_active"] = False
        set_symbol_state(symbol, state)
        return f"{symbol} Orderstatus wurde zurückgesetzt."

    elif cmd == "/buy":
        submit_order(symbol, "BUY")
        return f"{symbol} → Manuelle BUY-Order ausgeführt."

    return ""

def handle_terminal(stop_event):
    session = PromptSession()

    while not stop_event.is_set():
        try:
            with patch_stdout():
                cmd_input = session.prompt("[🟢 Terminal] > ").strip()
                if not cmd_input:
                    continue
                response = process_command(cmd_input)
                if response:
                    print(response)
                if cmd_input.lower() == "exit":
                    stop_event.set()
        except (KeyboardInterrupt, EOFError):
            stop_event.set()
