"use client";
import { useState } from "react";

export default function Home() {
  const [song, setSong] = useState("Shape of You");
  const [artist, setArtist] = useState("Ed Sheeran");

  async function handleButtonClick() {
    const res = fetch("http://localhost:8000/generate-pdf", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        songs: [
          {
            title: song,
            artist: artist,
          },
        ],
      }),
    })
      .then((response) => response.blob())
      .then((blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "lyrics.pdf";
        document.body.appendChild(a);
        a.click();
        a.remove();
      })
      .catch((error) => {
        console.error("Error generating PDF:", error);
      });

    await res;
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex min-h-screen w-full max-w-3xl flex-col items-center justify-between py-32 px-16 bg-white dark:bg-black sm:items-start">
        <header>
          <h1 className="text-2xl font-bold">Lyrics-to-pdf</h1>
          <p className="mt-4 text-lg">
            A simple tool to convert song lyrics into a PDF format. Just enter
            the song title and artist, and get a beautifully formatted PDF of
            the lyrics.
          </p>
          <p className="mt-4">
            Fetch lyrics for:
            <input
              type="text"
              value={song}
              onChange={(e) => setSong(e.target.value)}
              className="mx-2 rounded border border-gray-300 px-2 py-1 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-600 dark:text-white"
            />{" "}
            by
            <input
              type="text"
              value={artist}
              onChange={(e) => setArtist(e.target.value)}
              className="mx-2 rounded border border-gray-300 px-2 py-1 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-600 dark:text-white"
            />
          </p>
          <button
            className="mt-6 rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600"
            onClick={handleButtonClick}
          >
            Generate and download PDF
          </button>
          <br />
        </header>
      </main>
    </div>
  );
}
