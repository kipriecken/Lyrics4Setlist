'use client'
import { useCallback, useState } from 'react'

import { handleButtonClick, type Song } from './utils/helpers'
import OcrReader from './components/OcrReader'
import SongInput from './components/songInput'

export default function Home() {
  const [songs, setSongs] = useState<Song[]>([
    { title: 'Shape of You', artist: 'Ed Sheeran' },
  ])
  const [fetching, setFetching] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

  const handleGeneratePDF = async () => {
    setSuccess(null)
    setFetching(true)
    await handleButtonClick(songs)
      .then(() => {
        setSuccess(
          'PDF generated and downloaded successfully! Check your downloads.'
        )
        setError(null)
      })
      .catch((err) => {
        setError('Failed to generate PDF. Please try again.')
        console.error('Error generating PDF:', err)
        setSuccess(null)
      })
      .finally(() => {
        setFetching(false)
      })
  }

  const updateSong = useCallback(
    (index: number, updated: Song) => {
      setSongs((current) => {
        const copy = [...current]
        copy[index] = updated
        return copy
      })
    },
    [setSongs]
  )

  const removeSong = useCallback(
    (index: number) => {
      setSongs((current) => {
        const next = [...current]
        next.splice(index, 1)
        return next
      })
    },
    [setSongs]
  )

  const handleExtractedSongs = useCallback(
    (extracted: Song[]) => {
      if (extracted.length > 0) {
        setSongs(extracted)
      }
    },
    [setSongs]
  )

  const flipSongsAndArtists = useCallback(() => {
    setSongs((current) =>
      current.map((song) => ({
        title: song.artist,
        artist: song.title,
      }))
    )
  }, [setSongs])

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex min-h-screen w-full max-w-3xl flex-col items-center justify-between py-32 px-16 bg-white dark:bg-black sm:items-start">
        <header className="w-full">
          <h1 className="text-2xl font-bold">Lyrics4Setlist</h1>
          <p className="mt-4 text-lg">
            Generate a PDF of setlist lyrics with English translations.
          </p>
          <OcrReader onSongsExtracted={handleExtractedSongs} />
          <div className="mt-4 w-full">
            <div className="flex justify-between items-center">
              <div className="text-sm font-semibold">Fetch lyrics for:</div>
              <button
                onClick={flipSongsAndArtists}
                className="rounded bg-gray-500 px-3 py-2 text-white hover:bg-blue-600"
              >
                Flip title/artist
              </button>
            </div>
            <div className="mt-2 space-y-4">
              {songs.map((song, index) => (
                <SongInput
                  key={index}
                  index={index}
                  song={song}
                  onChange={updateSong}
                  onRemove={removeSong}
                  canRemove={songs.length > 1}
                />
              ))}
            </div>
            <div className="mt-3 flex justify-between">
              <button
                onClick={() => setSongs([{ title: '', artist: '' }])}
                className="rounded bg-gray-500 px-3 py-2 text-white hover:bg-red-600"
              >
                Clear
              </button>
              <button
                onClick={() =>
                  setSongs((prev) => [...prev, { title: '', artist: '' }])
                }
                className="rounded bg-gray-500 px-3 py-2 text-white hover:bg-green-600"
              >
                +
              </button>
            </div>
          </div>
          <button
            className="mt-6 rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
            onClick={handleGeneratePDF}
            disabled={fetching}
          >
            Generate and download PDF
          </button>
          {fetching && (
            <div className="mt-4">
              Generating PDF...{' '}
              <div className="flex items-center justify-center">
                <div className="w-8 h-8 border-4 border-blue-200 rounded-full animate-spin border-t-blue-600"></div>
              </div>
            </div>
          )}
          {error && <p className="mt-4 text-red-500">{error}</p>}
          {success && (
            <p className="mt-4 bg-green-100 text-green-700 rounded px-4 py-2">
              {success}
            </p>
          )}
          <br />
        </header>
      </main>
    </div>
  )
}
