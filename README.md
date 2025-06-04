# Trading Bot

This project contains a minimal trading bot used for experimenting with different interfaces. The bot simulates market data and places dummy orders. It persists its state to disk so the session can be restored when restarted.

## Features

- Simulated strategy generating `BUY`, `SELL` or `HOLD` signals for each configured symbol.
- Rich powered dashboard showing status information and last log entries.
- Terminal command interface with commands like `/pause`, `/resume`, `/status` and `/buy`.
- Optional Telegram bot that sends signal notifications and offers inline buttons to control the bot.
- Persistence of symbol state in `data/recovery.json`.

## Setup

1. Install **Python 3.11** or newer.
2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install the dependencies:

   ```bash
   pip install python-dotenv rich pyTelegramBotAPI
   ```

   *(The file `requirements.txt` is empty; install the packages above manually.)*
4. Copy `.env.example` to `.env` and fill in your Telegram credentials (see below).

## Running the bot

Start the application with:

```bash
python main.py
```

A dashboard appears in the terminal showing the configured symbols. Another thread waits for commands; type `"/help"` to see available commands. Use `exit` or press `Ctrl+C` to stop the bot.

If Telegram credentials are provided, the bot will also send notifications for each signal with buttons to pause/resume a symbol or submit an order.

## Environment variables

Place the following variables in a `.env` file in the project root:

```ini
TELEGRAM_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-chat-id
```

Both are optional but required if you want to use the Telegram integration. When not set, signals are only printed to the console.
