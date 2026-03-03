# Lyrics-to-pdf

Generate a pdf of lyrics (including translation) given song titles and artists.<br/>

### Motivation

> As a Fever Candlelight musician, I study and learn lots of music (potentially 20 different shows a month). A central part of the performances is talking to the audience and I believe it is important to know the lyrics. Googling and copying/pasting lyrics for each song is very time consuming, much less translating. I would use an LLM but they are unable to get past licensing to search for lyrics. Further, since we use iPads for the shows, A PDF is the perfect format. Lastly, since Fever Candlelight concerts happen across the globe, this tool can easily be extended to translate lyrics into languages other than English.

## Setup

Generate an access token for free at [genius.com/api-clients](genius.com/api-clients) and store it as an environment variable (see `.env.example`).

```
export GENIUS_ACCESS_TOKEN="your-token-here"
```

<br/>

Navigate to backend and create virtual environment:

```
cd backend && python3 -m venv .venv && source .venv/bin/activate
```

### Option 1: Run in Terminal with CSV file as input

Install dependencies:

```
pip install -r requirements.txt
```

<br/>

Run:

```
python3 lyrics.py
```

### Option 2: Run as web API with JSON input

Install dependencies:

```bash
pip install -r requirements-web.txt
```

<br/>
Run:

```
flask run -p 8000
```

And send a JSON request:

```
curl -X POST http://localhost:8000/generate-pdf \
  -H "Content-Type: application/json" \
  -d '{
    "songs": [
      {"title": "Hello", "artist": "Adele"}
    ]
  }' \
  --output lyrics.pdf
```

---

Packages:

- [lyricsgenius](https://lyricsgenius.readthedocs.io/en/master/) for fetching lyrics
- [Googletrans](https://pypi.org/project/googletrans/) for translation
- [FPDF2](https://py-pdf.github.io/fpdf2/index.html]) for PDF generation
