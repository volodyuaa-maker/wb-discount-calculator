from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/discount', methods=['GET', 'POST'])
def discount():
    # 1. Сначала пробуем взять цену из query-параметра ?price=...
    text = request.args.get("price")

    # 2. Если параметра нет – пробуем JSON {"text": "..."} (на будущее, если понадобится)
    if not text:
        data = request.get_json(silent=True) or {}
        if isinstance(data, dict) and "text" in data:
            text = str(data["text"])
        else:
            # 3. В крайнем случае берём сырое тело
            text = request.get_data(as_text=True) or ""

    # 4. Чистим строку от пробелов и неразрывных пробелов
    normalized = (
        text.replace(" ", "")
            .replace("\u00a0", "")
            .replace("\u202f", "")
    )

    # 5. Ищем первое число в строке
    match = re.search(r'\d+(?:[.,]\d+)?', normalized)
    if not match:
        return jsonify({
            "error": "no_number_found",
            "source_text": text,
            "price": None,
            "new_price": None,
            "reply": "Я не нашёл число в сообщении. Напишите, пожалуйста, цену цифрами 🙂"
        }), 200

    price_str = match.group(0).replace(",", ".")
    price = float(price_str)

    # 6. Считаем цену с 20% скидкой
    new_price = round(price * 0.8)

    reply = (
        f"Готово! 🎉\n\n"
        f"Цена без скидки: {int(price)} ₽\n"
        f"Цена со скидкой 20%: {new_price} ₽"
    )

    return jsonify({
        "price": price,
        "new_price": new_price,
        "reply": reply
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
