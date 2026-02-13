import lyricsgenius
import os
import csv
from fpdf import FPDF

def get_csv_from_input():
  """Gets the CSV data from the user via input."""
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

lyrics_genius_key = os.environ.get("LYRICS_GENIUS_KEY")
genius = lyricsgenius.Genius(lyrics_genius_key)

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

for song in songs:
    data = genius.search_song(song["title"], song["artist"])
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