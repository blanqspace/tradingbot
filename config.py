# config.py

import os
from pathlib import Path
from dotenv import load_dotenv  # <<< NEU

# ✅ .env laden
load_dotenv()

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

# Anzeige: Ist Telegram aktiviert?
print(f"Telegram aktiv: {USE_TELEGRAM}, Token geladen: {bool(TELEGRAM_TOKEN)}, Chat-ID geladen: {bool(TELEGRAM_CHAT_ID)}")


# Lade Umgebungsvariablen aus einer .env-Datei (falls vorhanden)
print("Lade Umgebungsvariablen...")
load_dotenv()

# === Betriebsmodi ===
SIMULATION = False        # True = Testmodus ohne echte Verbindung
print(f"SIMULATION gesetzt auf: {SIMULATION}")

USE_LOGGING = True        # Aktiviert Logging in Datei
print(f"USE_LOGGING gesetzt auf: {USE_LOGGING}")

# === IBKR API-Verbindung ===
TWS_HOST = "127.0.0.1"    # Standard für lokalen IB Gateway oder TWS
TWS_PORT = 4001           # IB Gateway = 4002, TWS Paper = 7497, TWS Live = 7496
CLIENT_ID = 124           # Beliebige ID, muss eindeutig sein
print(f"IBKR-Verbindung: HOST={TWS_HOST}, PORT={TWS_PORT}, CLIENT_ID={CLIENT_ID}")

# === Standard-Dateien ===
DEFAULT_CSV_FILENAME = os.path.join("logs", "signals.csv")
DEFAULT_LOG_FILE = os.path.join("logs", "bot.log")
print(f"Pfad für CSV: {DEFAULT_CSV_FILENAME}")
print(f"Pfad für Logfile: {DEFAULT_LOG_FILE}")

# === Schwellenwerte für Strategie ===
RSI_THRESHOLD_HIGH_VOL = 35
RSI_THRESHOLD_LOW_VOL  = 25
MA_SHORT = 10
MA_LONG = 30
print(f"Strategie-Schwellen: RSI hoch={RSI_THRESHOLD_HIGH_VOL}, niedrig={RSI_THRESHOLD_LOW_VOL}, MA kurz={MA_SHORT}, MA lang={MA_LONG}")

# === Telegram-Integration ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # sicher aus Umgebungsvariablen
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
USE_TELEGRAM = False  # Aktiviert/Deaktiviert Telegram-Nachrichten
print(f"Telegram aktiv: {USE_TELEGRAM}, Token geladen: {bool(TELEGRAM_TOKEN)}, Chat-ID geladen: {bool(TELEGRAM_CHAT_ID)}")

# === Watchdog-Konfiguration ===
USE_WATCHDOG = False  # Aktiviert die Hintergrundüberwachung
print(f"Watchdog aktiv: {USE_WATCHDOG}")

# === Markt- und Zeitkonfiguration ===
USE_RTH = True  # True = Nur reguläre Handelszeiten (RTH), False = Alle Daten
SKIP_MARKET_TIME_CHECK = False  # True = Überspringt die Marktzeitprüfung
print(f"Marktkonfiguration: RTH={USE_RTH}, Market-Check überspringen={SKIP_MARKET_TIME_CHECK}")
