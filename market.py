# market.py
import random

# In einem echten System würde man hier Live-Daten abrufen.
# In Iteration 1 simulieren wir einfach Kursdaten.

_price_history = {
    "AAPL": [random.uniform(170, 180) for _ in range(60)]
}

def get_price_data(symbol, length=60):
    """Gibt die letzten `length` Preise zurück."""
    if symbol not in _price_history:
        _price_history[symbol] = [random.uniform(170, 180) for _ in range(length)]

    # Neue zufällige Preisbewegung hinzufügen
    last_price = _price_history[symbol][-1]
    new_price = round(last_price + random.uniform(-0.3, 0.3), 2)
    _price_history[symbol].append(new_price)
    _price_history[symbol] = _price_history[symbol][-length:]

    return _price_history[symbol]
