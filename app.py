from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "message": "Lyrics API is healthy"})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
