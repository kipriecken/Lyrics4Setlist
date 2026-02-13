# Lyrics-to-pdf

A tool for creating a pdf based on a csv of song titles and artists, using the [lyricsgenius](https://lyricsgenius.readthedocs.io/en/master/) api, a wrapper for the genius api.

Create your own token at [genius.com/api-clients](genius.com/api-clients) and store it as an environment variable.

```
export LYRICS_GENIUS_TOKEN="your-token-here"
```

example:

```
export LYRICS_GENIUS_TOKEN="aslkfj34o1u2-309834234okj"
```

To run:

```
python3 lyrics.py
```
