# Lyrics-to-pdf

A tool for creating a pdf based on a csv of song titles and artists, using the [lyricsgenius](https://lyricsgenius.readthedocs.io/en/master/) api, a wrapper for the genius api.

Create your own token at [genius.com/api-clients](genius.com/api-clients) and store it as an environment variable (see `.env.example`).

```
export GENIUS_ACCESS_TOKEN="your-token-here"
```

example:

```
export GENIUS_ACCESS_TOKEN="aslkfj34o1u2-309834234okj"
```

To run:

```
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```
```
python3 lyrics.py
```
