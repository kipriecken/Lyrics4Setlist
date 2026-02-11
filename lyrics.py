import lyricsgenius
import os
import csv

def get_csv_from_input():
  """Gets the CSV data from the user via input."""
  try:
    csv_data = input("Enter the CSV data (use commas to separate fields): ")
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

csv_file = get_csv_from_input()
songs = convert_csv_to_songs(csv_file)

lyrics_genius_key = os.environ.get("LYRICS_GENIUS_KEY")
genius = lyricsgenius.Genius(lyrics_genius_key)

for song in songs:
    data = genius.search_song(song["title"], song["artist"])
    print(data)
