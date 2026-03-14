'use client'

import { useEffect, useMemo, useState } from 'react'
import { createWorker } from 'tesseract.js'
import type { Song } from '../utils/helpers'

interface OcrReaderProps {
  onSongsExtracted?: (songs: Song[]) => void
}

const extractSongsFromText = (inputText: string, artist: string): Song[] => {
  // remove all starting text ending in "setlist"
  const lines = inputText
    .split('\n')
    .map((l) => l.trim())
    .filter((line) => line && !line.toLowerCase().includes('setlist'))

  const songs: Song[] = []

  lines.forEach((line) => {
    // remove leading numbers if numbers are followed by a dot (e.g., "1. Song Title")
    if (/^\d+\./.test(line)) {
      line = line.split(/\d+\./)[1] ?? ''
    }

    // remove leading 1-2 characters or ® followed by whitespace
    line = line.replace(/^[a-zA-Z®]{1,2}\s+/, '').trim()

    // remove any text starting with "("
    line = line.replace(/\(.*$/, '').trim()

    // Remove "Encore:" if it exists
    line = line.replace(/^Encore:\s+/, '').trim()

    if (!line) return

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

export default function OcrReader({ onSongsExtracted }: OcrReaderProps) {
  const [artist, setArtist] = useState<string>('')
  const [text, setText] = useState<string>('')
  const [error, setError] = useState<string | null>(null)

  const readImage = async (file: File | null) => {
    if (!file) return

    try {
      const worker = await createWorker('eng')
      const {
        data: { text },
      } = await worker.recognize(file)
      console.log('Extracted text:', text)
      setText(text)
      await worker.terminate()
    } catch (err) {
      console.error('Error recognizing image:', err)
      setError('Failed to recognize image. Please try another image.')
    }
  }

  const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setError(null)
    const file = e.target.files?.[0] || null
    readImage(file)
  }

  const extractedSongs = useMemo(
    () => extractSongsFromText(text, artist),
    [text, artist]
  )

  useEffect(() => {
    if (onSongsExtracted) {
      onSongsExtracted(extractedSongs)
    }
  }, [extractedSongs, onSongsExtracted])

  return (
    <div className="flex items-center my-4 justify-center min-w-full bg-transparent font-sans">
      <div className="flex max-w-3xl flex-col items-center justify-between py-8 px-8 bg-white dark:bg-black border-dashed border-gray-300 border-2 rounded-2xl sm:items-start">
        <div className="py-3">Select an image (JPG, JPEG, PNG, TIFF)</div>
        <input
          type="file"
          // readIMage on change and reset artist name on click to encourage users to input artist name for better extraction
          onChange={onFileChange}
          onClick={() => setArtist('')}
          className="block w-full text-sm text-gray-500
  file:mr-4 file:py-2 file:px-4
  file:rounded-full file:border-0
  file:text-sm file:font-semibold
  file:bg-violet-50 file:text-violet-700
  hover:file:bg-violet-100"
        />
        <input
          type="text"
          value={artist}
          onChange={(e) => setArtist(e.target.value)}
          className="mt-4 rounded border border-gray-300 min-w-full px-2 py-1 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-600 dark:text-white"
          placeholder="Artist name (if not on image)"
        />
        {error && <p className="mt-4 text-red-500">{error}</p>}
      </div>
    </div>
  )
}
