from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/discount', methods=['POST'])
def discount():
    # Берём сырое тело запроса как текст
    body = request.get_data(as_text=True) or ""
# Если прилетело Telegram‑обновление, достаём текст сообщения
    payload = request.get_json(silent=True) or {}
    text = body
    if isinstance(payload, dict):
        message = payload.get("message") or {}
        callback_query = payload.get("callback_query") or {}

        if isinstance(message, dict) and isinstance(message.get("text"), str):
            text = message["text"]
        elif isinstance(callback_query, dict):
            if isinstance(callback_query.get("data"), str):
                text = callback_query["data"]
            elif isinstance(callback_query.get("message"), dict) and isinstance(
                callback_query["message"].get("text"), str
            ):
                text = callback_query["message"]["text"]
        elif isinstance(payload.get("text"), str):
            text = payload["text"]

    # Нормализуем возможные разделители групп разрядов: пробелы, неразрывные пробелы и узкие пробелы
    normalized = (
        text.replace(" ", "")
        .replace("\u00a0", "")  # nbsp
        .replace("\u202f", "")  # narrow nbsp, часто приходит из Telegram
    )

    # Пытаемся найти первое число в тексте (1492, 1492.50, 1492,50)
    match = re.search(r'\d+(?:[.,]\d+)?', normalized)
    if not match:
        # Ничего не нашли — но НЕ падаем, возвращаем 200 с диагностикой
        return jsonify({
            "error": "no_number_found",
            "body": body,
            "new_price": None
        }), 200

    price_str = match.group(0).replace(",", ".")
    price = float(price_str)
    return jsonify({
        "price": price,
        "new_price": new_price
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
