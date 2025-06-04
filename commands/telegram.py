import telebot
import telebot.types
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from utils.logging import log, Logger
log: Logger  # ← Das sagt dem Linter, dass `log()` korrekt ist
from state import get_symbol_state, set_symbol_state
from order import submit_order

if TELEGRAM_TOKEN is None:
    raise RuntimeError("❌ TELEGRAM_TOKEN fehlt – bitte in .env definieren!")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# === Benutzerbefehl: /start /help ===
@bot.message_handler(commands=["start", "help"])
def help_message(message):
    chat_id = message.chat.id
    bot.reply_to(message, (
        f"✅ Deine Chat-ID ist: {chat_id}\n"
        "Verfügbare Befehle:\n"
        "/menu AAPL – Steuerung per Button"
    ))
    log(f"Telegram Chat-ID erkannt: {chat_id}", "TELEGRAM")

# === Benutzerbefehl: /menu SYMBOL ===
@bot.message_handler(commands=["menu"])
def send_menu(message):
    try:
        parts = message.text.strip().split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Bitte Symbol angeben, z. B. /menu AAPL")
            return

        symbol = parts[1].upper()
        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(
            telebot.types.InlineKeyboardButton("📈 Status", callback_data=f"status:{symbol}"),
            telebot.types.InlineKeyboardButton("⏸ Pause", callback_data=f"pause:{symbol}")
        )
        markup.row(
            telebot.types.InlineKeyboardButton("▶️ Resume", callback_data=f"resume:{symbol}"),
            telebot.types.InlineKeyboardButton("🧹 Clear Order", callback_data=f"clear:{symbol}")
        )
        bot.send_message(message.chat.id, f"Was möchtest du mit {symbol} tun?", reply_markup=markup)

    except telebot.apihelper.ApiException as e:
        bot.reply_to(message, f"❌ Telegram API Fehler: {e}")
        log(f"Telegram Menu API Error: {e}", "ERROR")
    except ValueError as e:
        bot.reply_to(message, f"❌ Ungültiger Wert: {e}")
        log(f"Telegram Menu ValueError: {e}", "ERROR")
    except AttributeError as e:
        bot.reply_to(message, f"❌ Attributfehler: {e}")
        log(f"Telegram Menu AttributeError: {e}", "ERROR")

# === Inline-Antwort auf Button-Events ===
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    try:
        action, symbol = call.data.split(":")
        state = get_symbol_state(symbol)

        if action == "status":
            paused = state.get("paused", False)
            active = state.get("order_active", False)
            msg = f"🔍 {symbol} Status → Paused: {paused}, Order aktiv: {active}"

        elif action == "pause":
            state["paused"] = True
            msg = f"⏸ {symbol} pausiert"

        elif action == "resume":
            state["paused"] = False
            msg = f"▶️ {symbol} wieder aktiv"

        elif action == "clear":
            state["order_active"] = False
            msg = f"🧹 {symbol} Orderstatus zurückgesetzt"

        else:
            msg = "❌ Unbekannter Button"

        set_symbol_state(symbol, state)
        bot.answer_callback_query(call.id, msg)
        bot.send_message(call.message.chat.id, msg)
        log(f"[telegram] {action}:{symbol}", "COMMAND")

    except telebot.apihelper.ApiException as e:
        log(f"Callback API Error: {e}", "ERROR")
        bot.send_message(call.message.chat.id, f"❌ Fehler beim Ausführen: {e}")
    except AttributeError as e:
        log(f"Callback AttributeError: {e}", "ERROR")
        bot.send_message(call.message.chat.id, f"❌ Attributfehler beim Ausführen: {e}")
    except ValueError as e:
        log(f"Callback ValueError: {e}", "ERROR")
        bot.send_message(call.message.chat.id, f"❌ Ungültiger Wert beim Ausführen: {e}")

# === Funktion: Aktives Signal senden + Buttons ===
def send_signal_notification(symbol, signal, price, rsi):
    if TELEGRAM_CHAT_ID is None:
        return

    text = (
        f"📢 Neues Signal erkannt: {symbol}\n"
        f"➡️ Signal: *{signal}*\n"
        f"💵 Preis: {price}\n"
        f"📐 RSI: {rsi}"
    )
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton("✅ Order senden", callback_data=f"submit:{symbol}"),
        telebot.types.InlineKeyboardButton("⏸ Pausieren", callback_data=f"pause:{symbol}"),
        telebot.types.InlineKeyboardButton("🧹 Clear", callback_data=f"clear:{symbol}")
    )
    bot.send_message(TELEGRAM_CHAT_ID, text, reply_markup=markup, parse_mode="Markdown")
    log(f"Telegram Signal für {symbol} gesendet", "TELEGRAM")

# === Spezial: Callback für submit-Button ===
@bot.callback_query_handler(func=lambda call: call.data.startswith("submit:"))
def handle_submit_order(call):
    try:
        symbol = call.data.split(":")[1]
        state = get_symbol_state(symbol)
        if state.get("order_active"):
            msg = f"⚠️ {symbol} hat bereits aktive Order – übersprungen"
        else:
            submit_order(symbol, "BUY")
            msg = f"✅ {symbol}: Order wurde gesendet"
        bot.answer_callback_query(call.id, msg)
        bot.send_message(call.message.chat.id, msg)
        log(f"[telegram] submit:{symbol}", "COMMAND")
    except telebot.apihelper.ApiException as e:
        log(f"Submit Order API Error: {e}", "ERROR")
        bot.send_message(call.message.chat.id, f"❌ Telegram API Fehler beim Senden der Order: {e}")
    except AttributeError as e:
        log(f"Submit Order AttributeError: {e}", "ERROR")
        bot.send_message(call.message.chat.id, f"❌ Attributfehler beim Senden der Order: {e}")
    except ValueError as e:
        log(f"Submit Order ValueError: {e}", "ERROR")
        bot.send_message(call.message.chat.id, f"❌ Ungültiger Wert beim Senden der Order: {e}")

# === Startfunktion für main.py ===
def start_telegram_bot():
    log("Telegram-Bot gestartet", "COMMAND")
    bot.infinity_polling()
