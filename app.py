from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/discount', methods=['POST'])
def discount():
    # Берём сырое тело запроса как текст
    body = request.get_data(as_text=True) or ""

    # Пытаемся найти первое число в тексте (1492, 1 492, 1492.50, 1492,50)
    # Регулярка ищет цифры с возможной запятой/точкой
    match = re.search(r'\d+([.,]\d+)?', body.replace(" ", ""))

    if not match:
        # Ничего не нашли — но НЕ падаем, возвращаем 200 с диагностикой
        return jsonify({
            "error": "no_number_found",
            "body": body,
            "new_price": None
        }), 200

    price_str = match.group(0).replace(",", ".")
    price = float(price_str)

    new_price = round(price * 0.8)

    return jsonify({
        "price": price,
        "new_price": new_price
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
