from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/discount', methods=['POST'])
def discount():
    # 1. Пытаемся прочитать JSON вида {"text": "..."}
    data = request.get_json(silent=True) or {}

    if isinstance(data, dict) and "text" in data:
        text = str(data["text"])
    else:
        # Если почему-то не JSON — берём сырое тело как текст
        text = request.get_data(as_text=True) or ""

    # 2. Убираем пробелы и экзотические пробелы (из браузеров/телеги)
    normalized = (
        text.replace(" ", "")
            .replace("\u00a0", "")   # обычный неразрывный пробел
            .replace("\u202f", "")   # узкий неразрывный пробел
    )

    # 3. Ищем первое число (1492, 1492.50, 1492,50)
    match = re.search(r'\d+(?:[.,]\d+)?', normalized)
    if not match:
        return jsonify({
            "error": "no_number_found",
            "body": text,
            "price": None,
            "new_price": None,
            "reply": "Я не нашёл число в сообщении. Напишите, пожалуйста, цену цифрами 🙂"
        }), 200

    # 4. Конвертируем найденное число в float
    price_str = match.group(0).replace(",", ".")
    price = float(price_str)

    # 5. Считаем цену с 20% скидкой
    new_price = round(price * 0.8)

    # 6. Готовим текст, который бот покажет пользователю
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
