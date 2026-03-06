'use client'

import { useState } from 'react'
import { createWorker } from 'tesseract.js'

const OcrReader = () => {
  const [image, setImage] = useState<File | null>(null)
  const [artist, setArtist] = useState<string>('')
  const [text, setText] = useState<string>('')

  const readImage = async () => {
    if (!image) return

    const worker = await createWorker('eng')
    const {
      data: { text },
    } = await worker.recognize(image)
    setText(text)
    await worker.terminate()
  }

  const extractSongsFromText = (text: string) => {
    // remove all starting text ending in "setlist"
    const lines = text
      .split('\n')
      .filter((line) => !line.toLowerCase().includes('setlist'))
      .filter((line) => line.trim() !== '')

    const songs: { title: string; artist: string }[] = []

    lines.forEach((line) => {
      // remove leading numbers if numbers are followed by a dot (e.g., "1. Song Title")
      if (/^\d+\./.test(line)) {
        line = line.split(/\d+\./)[1]?.trim() // Remove leading numbers and dots
      }
      if (line === undefined) return

      // remove leading 1-2 characters or ® followed by whitespace
      line = line.replace(/^[a-zA-Z®]{1,2}\s+/, '').trim()

      // remove any text starting with "("
      line = line.replace(/\(.*$/, '').trim()

      // Remove "Encore:" if it exists
      line = line.replace(/^Encore:\s+/, '').trim()

      // if line contains "—" or "-", split into title and artist
      if (line.includes('—') || line.includes('-')) {
        const parts = line.split(/[-—]/).map((part) => part.trim())
        // if there are more than 2 parts, assume the last part is the title and the rest is the artist
        if (parts.length > 2) {
          const title = parts.pop() || ''
          const artist = parts.join(' - ')
          songs.push({ title, artist })
        } else if (parts.length === 2) {
          songs.push({ title: parts[1], artist: parts[0] })
        }
      } else {
        // if there is no separator, assume the whole line is the title and use the provided artist
        songs.push({ title: line, artist })
      }
    })

    return songs
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <div className="flex min-h-screen max-w-3xl flex-col items-center justify-between py-32 px-16 bg-white dark:bg-black sm:items-start">
        <input
          type="file"
          onChange={(e) => setImage(e.target.files?.[0] || null)}
          onClick={() => setArtist('')}
          className="block w-full text-sm text-gray-500
  file:mr-4 file:py-2 file:px-4
  file:rounded-full file:border-0
  file:text-sm file:font-semibold
  file:bg-violet-50 file:text-violet-700
  hover:file:bg-violet-100"
        />
        <button
          onClick={readImage}
          className="mt-6 rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          Read Image
        </button>
        <input
          type="text"
          value={artist}
          onChange={(e) => setArtist(e.target.value)}
          className="mt-4 rounded border border-gray-300 px-2 py-1 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-600 dark:text-white"
          placeholder="Enter artist name"
        />
        <button
          onClick={() => setText('')}
          className="mt-4 rounded bg-red-500 px-4 py-2 text-white hover:bg-red-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          Clear Songs
        </button>
        <ul className="mt-4">
          {extractSongsFromText(text).map((song, index) => (
            <li key={index} className="mb-2">
              <strong>{song.title}</strong> by {song.artist}
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}

export default OcrReader
