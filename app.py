from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "message": "Lyrics API is healthy"})


@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    data = request.get_json()

    if not data or "songs" not in data:
        return jsonify({"error": "Invalid request, 'songs' key is required"}), 400

    songs_data = data["songs"]
    if not isinstance(songs_data, list):
        return jsonify({"error": "'songs' should be a list of song data"}), 400

    return jsonify(
        {
            "message": "PDF generation logic would be called here",
            "songs": songs_data,
        }
    )


if __name__ == "__main__":
    app.run(port=8000, debug=True)
