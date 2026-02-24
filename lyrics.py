import asyncio
import csv
import os
from typing import Dict, List, Optional

import lyricsgenius
from dotenv import load_dotenv
from fpdf import FPDF
from googletrans import Translator
from langdetect import detect
from rapidfuzz import fuzz

load_dotenv()

DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LYRICS_GENIUS_KEY = os.getenv("GENIUS_ACCESS_TOKEN")
if not LYRICS_GENIUS_KEY:
    print(
        "Warning: GENIUS_ACCESS_TOKEN not found in environment variables. Please set it to use the lyrics fetching functionality."
    )
    genius = None
else:
    genius = lyricsgenius.Genius(LYRICS_GENIUS_KEY, timeout=15, retries=3, sleep_time=1)
    genius.verbose = DEBUG


def get_csv_path() -> str:
    """Gets the CSV data from the user via input.

    Returns:
      The path to the CSV file provided by the user, or None if there was an error processing the input.
    """
    csv_path = input(
        "Provide a path to a CSV file (hit Enter to generate using sample data): "
    )
    return csv_path or "sample-data-2.csv"


def read_songs_from_csv(csv_path: str) -> List[Dict[str, str]]:
    """
    Reads songs from a CSV file and returns a list of song dictionaries.

    Args:
      csv_path: The path to the CSV file.

    Returns:
      A list of song dictionaries, where each dictionary contains 'title' and 'artist' keys.
    """
    songs = []
    if not os.path.exists(csv_path):
        print(f"Error: File '{csv_path}' not found.")
        return songs
    try:
        with open(csv_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header row
            for row in reader:
                if len(row) < 2 or not row[0].strip() or not row[1].strip():
                    print(f"Skipping row due to missing data: {row}")
                    continue
                songs.append({"title": row[0].strip(), "artist": row[1].strip()})
    except Exception as e:
        print(f"Error reading CSV file '{csv_path}': {e}")
    return songs


def detect_language(text):
    """Detects the language of the given text.

    Args:
        text: The text to detect the language of.

    Returns:
        The detected language code (ex. "en" for English), or None if detection fails.

    """
    try:
        return detect(text)
    except ImportError:
        print(
            "langdetect library not found. Please install it to enable language detection."
        )
        return None
    except Exception as e:
        print(f"Error detecting language: {e}")
        return None


csv_file = get_csv_path()
songs = read_songs_from_csv(csv_file)

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)


def is_match(requested, actual, threshold=80) -> bool:
    """Determines if the requested and actual strings are a close match based on a similarity threshold.

    Args:
        requested: The requested string (e.g. song title or artist).
        actual: The actual string fetched from Genius.
        threshold: The similarity ratio threshold (0-100) for considering it a match.
    Returns:
        True if the similarity ratio is above the threshold, False otherwise.
    """
    if not requested or not actual:
        return False
    ratio = fuzz.ratio(requested.lower(), actual.lower())
    return ratio >= threshold


def search_song(title: str, artist: str) -> Optional[Dict[str, str]]:
    """Searches for a song on Genius by title and artist.

    Args:
        title: The title of the song to search for.
        artist: The artist of the song to search for.

    Returns:
        A Genius Song object if found, or None if not found or if Genius is not initialized.
    """
    if genius is None:
        print("Genius client not initialized. Cannot search for songs.")
        return None
    try:
        result = genius.search_song(title, artist)
        if not result:
            print(f"Song '{title}' by '{artist}' not found on Genius.")
            return None

        title_match = is_match(title, result.title)
        artist_match = is_match(artist, result.artist)
        if not title_match or not artist_match:
            print(
                f"Warning: The fetched song '{result.title}' by '{result.artist}' does not closely match the requested song '{title}' by '{artist}'."
            )
        else:
            print(f"Found song '{result.title}' by '{result.artist}' on Genius.")
        return {
            "title": result.title,
            "artist": result.artist,
            "lyrics": result.lyrics,
        }
    except Exception as e:
        print(f"Error searching for song '{title}' by '{artist}': {e}")
        return None


def translate_lyrics(lyrics, src_language):
    """Translates the given lyrics to English using Google Translate.

    Args:
        lyrics: The lyrics to translate.
        src_language: The source language code of the lyrics.

    Returns:
        The translated lyrics in English, or the original lyrics if translation fails.
    """
    try:

        async def translate_async():
            translator = Translator()
            translated = await translator.translate(lyrics, src=src_language, dest="en")
            return translated.text

        return asyncio.run(translate_async())
    except Exception as e:
        print(f"Error translating lyrics: {e}")
        return lyrics


for song in songs:
    data = search_song(song["title"], song["artist"])
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    if data:
        title, artist, lyrics = (
            data.get("title"),
            data.get("artist"),
            data.get("lyrics"),
        )
        pdf.multi_cell(0, 10, f"{title} by {artist}\n\n")
        print(f"Detecting language for {title} by {artist}...")
        language = detect_language(lyrics)
        translated_lyrics = None
        if language:
            print(f"Detected language: {language}")
        if language and language != "en":
            print(
                f"Warning: Detected language '{language}' for {title} by {artist} may not be supported by the PDF encoding. Lyrics may not display correctly."
            )
            try:
                translated_lyrics = translate_lyrics(lyrics, language)
                print(
                    f"Translated lyrics for {title} by {artist}:\n{translated_lyrics}"
                )
            except Exception as e:
                print(f"Error translating lyrics for {title} by {artist}: {e}")
                print("Adding original lyrics to PDF with potential encoding issues.")
        pdf.multi_cell(0, 10, lyrics.encode("latin-1", "replace").decode("latin-1"))
        if translated_lyrics:
            print(f"Adding translated lyrics for {title} by {artist} to PDF...")
            pdf.multi_cell(
                0,
                10,
                f"\nTranslated Lyrics:\n{translated_lyrics.encode('latin-1', 'replace').decode('latin-1')}",
            )
    else:
        pdf.multi_cell(
            0,
            10,
            f"Lyrics not found for {song.get('title', 'Unknown Title')} by {song.get('artist', 'Unknown Artist')}.",
        )
    print(data)

pdf_name = "lyrics.pdf"
pdf_name.encode("latin-1", "replace")
try:
    pdf.output(pdf_name).encode("latin-1")
    print(f"PDF generated successfully: {pdf_name}")
except Exception as e:
    print(f"Error generating PDF: {e}")
