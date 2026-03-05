# Lyrics-to-pdf

Generate a pdf of lyrics (including translation) given song titles and artists.<br/>

### Motivation

> I play viola in string quartet concerts where part of the mission is connecting the musicians and audience in a small concert format. I study and learn up to 20 different shows a month. A central part of the performances is speaking to the audience about the music. I find it helpful to have the lyrics for reference. When listening to the songs, however, I rarely catch all the lyrics; the main focus of my practicing is on the notes and rhythms. Googling and copying/pasting lyrics for each song, then creating a PDF from those, is very time consuming and repetitive. If the lyrics require translation, yet another step is needed. The process is ripe for automation. LLM's are unable to automate this process because of lyrics licensing. This tool simplifies the process into just a few steps, producing a PDF which is the perfect format for sheet music iPad apps such as ForScore. Further, this tool can easily be extended to translate lyrics into languages other than English, which is helpful considering that these concerts happen across the globe.

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
      {"title": "Shape of You", "artist": "Ed Sheeran"}
    ]
  }' \
  --output lyrics.pdf
```

## Frontend

In new terminal window:

```
cd ../frontend && pnpm install
```

Run Next JS app:

```
pnpm run dev
```

Navigate to `localhost:3000` in browser. If the backend is running locally, you will be able to generate and download a sample PDF.

---

---

Packages:

- [lyricsgenius](https://lyricsgenius.readthedocs.io/en/master/) for fetching lyrics
- [Googletrans](https://pypi.org/project/googletrans/) for translation
- [FPDF2](https://py-pdf.github.io/fpdf2/index.html]) for PDF generation
