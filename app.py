from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/discount', methods=['POST'])
def discount():
    # 1) Пытаемся разобрать JSON
    data = request.get_json(silent=True)

    # 2) Если JSON нет — пробуем form-data / x-www-form-urlencoded
    if not data:
        if request.form:
            data = request.form.to_dict()
        else:
            data = {}

    # 3) Пытаемся взять price прямо из словаря
    raw_price = data.get("price")

    # 4) Если price нет — пытаемся вытащить число из сырого тела запроса
    if not raw_price:
        body_text = request.get_data(as_text=True) or str(data)
        match = re.search(r'\d+([.,]\d+)?', body_text)
        raw_price = match.group(0) if match else None

    if not raw_price:
        # Ничего не нашли – возвращаем ошибку, но без падения сервера
        return jsonify({
            "error": "empty_price",
            "debug": {
                "data": data
            }
        }), 400

    # 5) Нормализуем строку и конвертируем в число
    price_str = str(raw_price).replace(",", ".").strip()

    try:
        price = float(price_str)
    except (ValueError, TypeError):
        return jsonify({
            "error": "bad_price_format",
            "debug": {
                "raw_price": raw_price
            }
        }), 400

    # 6) Считаем скидку 20%
    new_price = round(price * 0.8)

    return jsonify({
        "price": price,
        "new_price": new_price
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
