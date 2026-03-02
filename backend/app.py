from flask import Flask, jsonify, request, send_file
import os
import uuid
import lyrics

app = Flask(__name__)

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "message": "Lyrics API is healthy"})


@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    data = request.get_json()

    if not data or "songs" not in data:
        return jsonify({"error": "Invalid request, 'songs' key is required"}), 400

    songs = data["songs"]
    if not isinstance(songs, list):
        return jsonify({"error": "'songs' should be a list of song data"}), 400

    songs_data = []
    for song in songs:
        title = song.get("title")
        artist = song.get("artist")

        if not title or not artist:
            continue

        result = lyrics.search_song(title, artist)
        if not result:
            result = {"title": title, "artist": artist, "lyrics": "No lyrics found"}
            continue

        language = lyrics.detect_language(result["lyrics"])
        result["language"] = language
        result["translated_lyrics"] = None

        if language and language != "en":
            try:
                translated_lyrics = lyrics.translate_lyrics(result["lyrics"], language)
                result["translated_lyrics"] = translated_lyrics
            except Exception as e:
                print(f"Error translating lyrics for {title} by {artist}: {e}")
                result["translated_lyrics"] = None

        songs_data.append(result)

    filename = f"lyrics_{uuid.uuid4().hex[:8]}.pdf"
    output_path = os.path.join(OUTPUT_DIR, filename)

    try:
        lyrics.generate_pdf(songs_data, output_path)
        print(f"PDF generated successfully: {output_path}")
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return jsonify({"error": "Failed to generate PDF", "details": str(e)}), 500

    return send_file(
        output_path,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf",
    )


if __name__ == "__main__":
    app.run(port=8000, debug=True)
