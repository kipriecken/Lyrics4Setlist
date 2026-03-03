# Lyrics-to-pdf

Generate a pdf of lyrics (including translation) given song titles and artists.<br/>

### Motivation

> Fever Candlelight concerts are about connecting the musicians and audience in a small concert format. As a Fever Candlelight musician, I study and learn up to 20 different shows a month. A central feature of this audience involvement entails speaking to the audience about the music. As a musician I don't always catch all the lyrics, and rarely have time to write them down or confirm them. I believe it is important, though, to at least have the lyrics for reference. The ideal format is a pdf because we use iPads for the shows and can easily upload the files into ForScore or whatever app we choose to use for music. Googling and copying/pasting lyrics for each song, then creating a PDF from those, can be very time consuming. If the lyrics require translation, even more time is needed. Any level of automation is helpful. LLM's are unable to automate this process because of lyrics licensing. This tool simplifies the process into just a few steps and saves time and helps connect myself as a musician to the audience. Lastly, since Fever Candlelight concerts happen across the globe, this tool can easily be extended to translate lyrics into languages other than English.

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
