
from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder="static")

TOKENS_FILE = "data/tokens_left.txt"
OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "")

def read_tokens():
    with open(TOKENS_FILE, "r") as f:
        return int(f.read().strip())

def write_tokens(v):
    with open(TOKENS_FILE, "w") as f:
        f.write(str(v))

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/tokens")
def tokens():
    return jsonify({"tokens": read_tokens()})

@app.route("/send", methods=["POST"])
def send():
    msg = request.json.get("message", "")
    used = len(msg) // 2 + 50
    left = read_tokens()
    if left - used < 0:
        return jsonify({"error": "token 부족"}), 400
    write_tokens(left - used)
    return jsonify({
        "reply": "(GPT 응답 자리)",
        "used": used,
        "left": left - used
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
