from pybit.unified_trading import HTTP, WebSocket

# Установка API ключей и секретов
api_key = "your_api_key"
api_secret = "your_api_secret"

# Создание HTTP сессии для аутентификации
http_session = HTTP(
    api_key=api_key,
    api_secret=api_secret,
    testnet=False  # или True для тестовой сети
)

# Создание WebSocket сессии
ws = WebSocket(
    "wss://stream.bybit.com/realtime",
    api_key=api_key,
    api_secret=api_secret,
    testnet=False
)


# Функция обработки сообщений от WebSocket
def handle_message(msg):
    # Фильтрация по ценовому диапазону и объёму
    min_price = 30000
    max_price = 40000
    min_volume = 0.1
    max_volume = 10

    bids = msg['data']['bids']
    asks = msg['data']['asks']

    filtered_bids = [bid for bid in bids if
                     min_price <= float(bid) <= max_price and min_volume <= float(bid[1]) <= max_volume]
    filtered_asks = [ask for ask in asks if
                     min_price <= float(ask) <= max_price and min_volume <= float(ask[1]) <= max_volume]

    # Дополнительная обработка для получения детальной информации о заявках
    for bid in filtered_bids:
        # Использование HTTP API для получения дополнительных данных
        order_info = http_session.get_orderbook(category="linear", symbol="BTCUSDT", limit=50)
        # Обработка дополнительной информации
        print("Detailed Bid Info:")
        print(order_info)

    for ask in filtered_asks:
        # Использование HTTP API для получения дополнительных данных
        order_info = http_session.get_orderbook(category="linear", symbol="BTCUSDT", limit=50)
        # Обработка дополнительной информации
        print("Detailed Ask Info:")
        print(order_info)


# Подключение к WebSocket и обработка сообщений
ws.connect()
ws.subscribe("orderbook.100ms.BTCUSDT") # Подписка происходит после подключения
ws.on("orderbook.100ms.BTCUSDT", handle_message)

# Ожидание сообщений
while True:
    pass
