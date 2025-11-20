from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/discount', methods=['POST'])
def discount():
    data = request.json
    price = float(data.get("price", 0))
    new_price = round(price * 0.8)
    return jsonify({"new_price": new_price})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
