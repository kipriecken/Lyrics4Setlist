# Lyrics-to-pdf

A tool for creating a pdf of lyrics and translated lyrics based on a csv of song titles and artists, using the [lyricsgenius](https://lyricsgenius.readthedocs.io/en/master/) api, a wrapper for the genius api.<br/><br/>

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

---------------------------------------------

Other packages used:

- [Googletrans](https://pypi.org/project/googletrans/) for translation
- [FPDF2](https://py-pdf.github.io/fpdf2/index.html]) for PDF generation
