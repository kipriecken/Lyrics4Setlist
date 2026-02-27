# Lyrics-to-pdf

A tool for creating a pdf of lyrics and translated lyrics based on a csv of song titles and artists, using the api, a wrapper for the genius api.<br/>

> Why? <br/> As a Fever Candlelight musician, I study the music (potentially 20 different shows a month) but seeing as we talk about the music, I am curious about the lyrics. I do not have time to Google and copy/paste lyrics for each song as I am focused on the music. Then, if the lyrics are in another language, I have to LLMs are unable to get past licensing to produce a PDF. A PDF is the perfect format to load onto my iPad for shows. I play up to 20 shows a month with potentially all different setlists. This saves immense time.

Fever Candlelight concerts are about bringing audiences and musicians closer together. They happen across the globe. This tool can easily be used to translate lyrics into any language.

Generate an access token for free at [genius.com/api-clients](genius.com/api-clients) and store it as an environment variable (see `.env.example`).

```
export GENIUS_ACCESS_TOKEN="your-token-here"
```

Example:

```
export GENIUS_ACCESS_TOKEN="aslkfj34o1u2-309834234okj"
```

<br/>

Setup:

```
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

<br/>

Run:

```
python3 lyrics.py
```

## Run as web API

(Using virtual environment)

```bash
pip install -r requirements-web.txt
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

Main packages used:

- [lyricsgenius](https://lyricsgenius.readthedocs.io/en/master/) for fetching lyrics
- [Googletrans](https://pypi.org/project/googletrans/) for translation
- [FPDF2](https://py-pdf.github.io/fpdf2/index.html]) for PDF generation
