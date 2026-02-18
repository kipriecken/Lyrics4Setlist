import lyricsgenius
import os
import csv
from fpdf import FPDF
from dotenv import load_dotenv
from rapidfuzz import fuzz

load_dotenv()

debug = os.getenv("DEBUG", "False").lower() == "true"
lyrics_genius_key = os.getenv("GENIUS_ACCESS_TOKEN")
if not lyrics_genius_key:
    print("Warning: GENIUS_ACCESS_TOKEN not found in environment variables. Please set it to use the lyrics fetching functionality.")
genius = lyricsgenius.Genius(lyrics_genius_key)

def get_csv_from_input():
  """Gets the CSV data from the user via input.
  
  Returns:
    The path to the CSV file provided by the user, or None if there was an error processing the input.
  """
  try:
    csv_data = input("Provide a path to a CSV file (hit Enter to generate using sample data): ")
    return csv_data
  except Exception as e:
    print(f"Error processing input: {e}")
    return None

def convert_csv_to_songs(csv_file):
  """
  Converts a CSV file to a list of song dictionaries.

  Args:
    csv_file: The path to the CSV file.

  Returns:
    A list of song dictionaries.
  """
  songs = []
  with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    next(reader, None)  # Skip the header row
    for row in reader:
      try:
        title = row[0]
        artist = row[1]
        songs.append({"title": title, "artist": artist})
      except IndexError:
        print(f"Skipping row due to missing data: {row}") 
  return songs

csv_file = "sample-data.csv"
csv_file = get_csv_from_input() or csv_file
songs = convert_csv_to_songs(csv_file)

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

for song in songs:
    data = genius.search_song(song["title"], song["artist"])
    if data and fuzz.ratio(song["title"].lower(), data.title.lower()) < 80 or data and data.artist and fuzz.ratio(song["artist"].lower(), data.artist.lower()) < 80:
        print(f"Warning: The fetched song '{data.title}' by '{data.artist}' does not closely match the requested song '{song['title']}' by '{song['artist']}'.")
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    if data:
        pdf.multi_cell(0, 10, f"{song['title']} by {song['artist']}\n\n")
        pdf.multi_cell(0, 10, data.lyrics.encode("latin-1", "replace").decode("latin-1"))
    else:
        pdf.multi_cell(0, 10, f"Lyrics not found for {song['title']} by {song['artist']}.")
    print(data)

pdf_name = "lyrics.pdf"
pdf_name.encode("latin-1", "replace")
try:
    pdf.output(pdf_name).encode("latin-1")
    print(f"PDF generated successfully: {pdf_name}")
except Exception as e:
    print(f"Error generating PDF: {e}")