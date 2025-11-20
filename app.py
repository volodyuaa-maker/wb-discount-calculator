from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/discount', methods=['POST'])
def discount():
    data = request.get_json(silent=True) or {}

    raw_price = data.get("price", 0)

    # Приводим к строке, чистим пробелы и запятые
    price_str = str(raw_price).replace(",", ".").strip()

    # Если строка пустая — возвращаем понятную ошибку,
    # чтобы сервер не падал
    if not price_str:
        return jsonify({
            "error": "empty_price",
            "raw_price": raw_price
        }), 400

    try:
        price = float(price_str)
    except (ValueError, TypeError):
        return jsonify({
            "error": "bad_price_format",
            "raw_price": raw_price
        }), 400

    new_price = round(price * 0.8)

    return jsonify({"new_price": new_price})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
