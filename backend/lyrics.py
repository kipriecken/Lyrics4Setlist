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
import requests

load_dotenv()

DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LYRICS_GENIUS_KEY = os.getenv("GENIUS_ACCESS_TOKEN")
if not LYRICS_GENIUS_KEY:
    print(
        "Warning: GENIUS_ACCESS_TOKEN not found in environment variables. Please set it to use the lyrics fetching functionality."
    )
    genius = None
else:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://genius.com/",
            "Origin": "https://genius.com",
            "Connection": "keep-alive",
        }
    )

    genius = lyricsgenius.Genius(
        LYRICS_GENIUS_KEY,
        timeout=15,
        retries=3,
        sleep_time=1,
        remove_section_headers=True,
        skip_non_songs=True,
        excluded_terms=["(Remix)", "(Live)", "(Acoustic)"],
    )

    genius._session = session

    genius.verbose = DEBUG


def get_csv_path() -> str:
    """Gets the CSV data from the user via input.

    Returns:
      The path to the CSV file provided by the user, or None if there was an error processing the input.
    """
    csv_path = input(
        "Provide a path to a CSV file (hit Enter to generate using sample data): "
    )
    return csv_path or "data/samples/sample-data-2.csv"


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


def detect_language(text: str) -> Optional[str]:
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


def is_match(requested: str, actual: str, threshold=60) -> bool:
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


def translate_lyrics(lyrics: str, src_language: str) -> str:
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


def generate_pdf(
    songs_data: List[Dict[str, str]], pdf_name: str = "lyrics.pdf"
) -> None:
    """Generates a PDF file with the song lyrics.

    Args:
        songs_data: A list of dictionaries containing song data (title, artist, lyrics, translated_lyrics).
        pdf_name: The name of the PDF file to generate.
    """

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for song in songs_data:
        title = song.get("title", "Unknown Title")
        artist = song.get("artist", "Unknown Artist")
        lyrics = song.get("lyrics", "No lyrics found")
        translated_lyrics = song.get("translated_lyrics")

        if lyrics == "No lyrics found":
            pdf.multi_cell(
                0,
                10,
                f"Lyrics not found for {title} by {artist}.",
            )
            continue
        # There is an issue with encoding certain characters in the lyrics (e.g. curly apostrophes)
        # that causes the PDF generation to fail. To work around this, I add a unicode font and
        # replace the known problematic character with its closest ASCII equivalent.
        arialttf_path = os.path.join(
            os.path.dirname(__file__), "fonts/Arial-Unicode-Bold.ttf"
        )
        if os.path.exists(arialttf_path):
            print(f"Adding unicode font for lyrics: {arialttf_path}")
            pdf.add_font("ArialUnicode", "", arialttf_path, uni=True)
            pdf.add_font("ArialUnicode", "B", arialttf_path, uni=True)
            font_family = "ArialUnicode"
        else:
            font_family = "Arial"

        pdf.add_page()
        pdf.set_font(font_family, "B", size=14)
        pdf.cell(0, 10, f"{title} by {artist}", ln=True)
        pdf.set_font(font_family, size=12)
        lyrics = lyrics.replace("’", "'").replace("\u2019", "'")
        pdf.multi_cell(
            0, 10, lyrics.encode("utf-8", "replace").decode("utf-8", "replace")
        )

        if translated_lyrics:
            pdf.add_page()  # Start translated lyrics on a new page
            arialttf_path = os.path.join(
                os.path.dirname(__file__), "fonts/Arial-Unicode-Bold.ttf"
            )
            if os.path.exists(arialttf_path):
                try:
                    pdf.add_font("ArialUnicode", "I", arialttf_path, uni=True)
                except Exception:
                    # some font files don't include an italic variant; ignore
                    pass
            pdf.set_font(font_family, "B", size=14)
            pdf.cell(0, 10, f"{title} by {artist} (translated)", ln=True)
            pdf.set_font(font_family, size=12)
            translated_lyrics = translated_lyrics.replace("’", "'").replace(
                "\u2019", "'"
            )
            pdf.multi_cell(
                0,
                10,
                translated_lyrics.encode("utf-8", "replace").decode("utf-8", "replace"),
            )

        pdf.ln(10)  # Add some space between songs

    try:
        pdf.output(pdf_name)
    except Exception as e:
        print(f"Error generating PDF: {e}")

    print(f"PDF generated successfully: {pdf_name}")


def main():
    # handle CSV input
    csv_path = get_csv_path()
    songs = read_songs_from_csv(csv_path)
    if not songs:
        print("No valid songs found in the CSV file. Exiting.")
        return

    # fetch lyrics, detect language, translate if needed, and prepare data for PDF generation
    songs_data = []
    for song in songs:
        data = search_song(song["title"], song["artist"])
        if data:
            title, artist, lyrics = (
                data.get("title"),
                data.get("artist"),
                data.get("lyrics"),
            )
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
                    print(
                        "Adding original lyrics to PDF with potential encoding issues."
                    )
            songs_data.append(
                {
                    "title": title,
                    "artist": artist,
                    "lyrics": lyrics,
                    "translated_lyrics": translated_lyrics,
                }
            )
        print(data.get("lyrics", "No lyrics found") if data else "No data found")

    # create PDF
    generate_pdf(songs_data)


if __name__ == "__main__":
    main()
