'use client'
import { useState } from 'react'

import { handleButtonClick } from './utils/helpers'

export default function Home() {
  const [songs, setSongs] = useState([
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

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex min-h-screen w-full max-w-3xl flex-col items-center justify-between py-32 px-16 bg-white dark:bg-black sm:items-start">
        <header>
          <h1 className="text-2xl font-bold">Lyrics4Setlist</h1>
          <p className="mt-4 text-lg">
            A simple tool to convert song lyrics into a PDF format. Just enter
            song titles and artists below and receive a beautifully formatted
            PDF of the lyrics with translations if in a different language.
            Perfect for musicians, setlists, or just fans who want to keep their
            favorite lyrics handy!
          </p>
          <div className="mt-4">
            Fetch lyrics for:
            {songs.map((song, i) => (
              <div key={i} className="flex items-center mt-2">
                <input
                  type="text"
                  value={song.title}
                  onChange={(e) => {
                    const newSongs = [...songs]
                    newSongs[i].title = e.target.value
                    setSongs(newSongs)
                  }}
                  className="mx-2 rounded border border-gray-300 px-2 py-1 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-600 dark:text-white"
                />
                {'by'}
                <input
                  type="text"
                  value={song.artist}
                  onChange={(e) => {
                    const newSongs = [...songs]
                    newSongs[i].artist = e.target.value
                    setSongs(newSongs)
                  }}
                  className="mx-2 rounded border border-gray-300 px-2 py-1 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-600 dark:text-white"
                />
              </div>
            ))}
            <button
              onClick={() => setSongs([...songs, { title: '', artist: '' }])}
              className="m-2 rounded bg-gray-500 px-2 py-1 text-white hover:bg-green-600"
            >
              + Add another song
            </button>
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
