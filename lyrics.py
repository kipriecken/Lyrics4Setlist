import asyncio
import os
import csv
from typing import List, Dict

import lyricsgenius
from fpdf import FPDF
from dotenv import load_dotenv
from rapidfuzz import fuzz
from langdetect import detect
from googletrans import Translator

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

translator = Translator()


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


async def async_translate_lyrics(lyrics, src_language):
    """Translates the given lyrics to English using Google Translate.

    Args:
        lyrics: The lyrics to translate.
        src_language: The source language code of the lyrics.

    Returns:
        The translated lyrics in English, or the original lyrics if translation fails.
    """
    try:
        translated = await translator.translate(lyrics, src=src_language, dest="en")
        return translated
    except Exception as e:
        print(f"Error translating lyrics: {e}")
        return lyrics


for song in songs:
    data = genius.search_song(song["title"], song["artist"])
    if (
        data
        and fuzz.ratio(song["title"].lower(), data.title.lower()) < 80
        or data
        and data.artist
        and fuzz.ratio(song["artist"].lower(), data.artist.lower()) < 80
    ):
        print(
            f"Warning: The fetched song '{data.title}' by '{data.artist}' does not closely match the requested song '{song['title']}' by '{song['artist']}'."
        )
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    if data:
        pdf.multi_cell(0, 10, f"{song['title']} by {song['artist']}\n\n")
        print(f"Detecting language for {song['title']} by {song['artist']}...")
        language = detect_language(data.lyrics)
        translated_lyrics = None
        if language:
            print(f"Detected language: {language}")
        if language and language != "en":
            print(
                f"Warning: Detected language '{language}' for {song['title']} by {song['artist']} may not be supported by the PDF encoding. Lyrics may not display correctly."
            )
            try:
                translated_lyrics = str(
                    asyncio.run(async_translate_lyrics(data.lyrics, language))
                )
                print(
                    f"Translated lyrics for {song['title']} by {song['artist']}:\n{translated_lyrics}"
                )
            except Exception as e:
                print(
                    f"Error translating lyrics for {song['title']} by {song['artist']}: {e}"
                )
                print("Adding original lyrics to PDF with potential encoding issues.")
        pdf.multi_cell(
            0, 10, data.lyrics.encode("latin-1", "replace").decode("latin-1")
        )
        if translated_lyrics:
            print(
                f"Adding translated lyrics for {song['title']} by {song['artist']} to PDF..."
            )
            pdf.multi_cell(
                0,
                10,
                f"\nTranslated Lyrics:\n{translated_lyrics.encode('latin-1', 'replace').decode('latin-1')}",
            )
    else:
        pdf.multi_cell(
            0, 10, f"Lyrics not found for {song['title']} by {song['artist']}."
        )
    print(data)

pdf_name = "lyrics.pdf"
pdf_name.encode("latin-1", "replace")
try:
    pdf.output(pdf_name).encode("latin-1")
    print(f"PDF generated successfully: {pdf_name}")
except Exception as e:
    print(f"Error generating PDF: {e}")
