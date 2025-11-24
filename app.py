from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/discount', methods=['POST'])
def discount():
    data = request.get_json(silent=True)
    body = request.get_data(as_text=True)

    return jsonify({
        "json_received": data,
        "raw_body": body
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
