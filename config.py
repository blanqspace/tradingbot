# config.py

import os
from pathlib import Path
from dotenv import load_dotenv  # <<< NEU

# ✅ .env laden
load_dotenv()

if __name__ == "__main__":
    # ✅ Test: Ist .env vorhanden?
    print(".env vorhanden:", Path(".env").exists())

# Symbole & Basisparameter
SYMBOLS = ["AAPL", "TSLA", "MSFT"]
INTERVAL = 5
SIMULATION = True
DEFAULT_QTY = 50

# === Telegram-Integration ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
USE_TELEGRAM = TELEGRAM_TOKEN is not None and TELEGRAM_CHAT_ID is not None

if __name__ == "__main__":
    # Anzeige: Ist Telegram aktiviert?
    print(
        f"Telegram aktiv: {USE_TELEGRAM}, Token geladen: {bool(TELEGRAM_TOKEN)}, Chat-ID geladen: {bool(TELEGRAM_CHAT_ID)}"
    )
