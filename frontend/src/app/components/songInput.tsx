import type { Song } from '../utils/helpers'

interface SongInputProps {
  index: number
  song: Song
  onChange: (index: number, song: Song) => void
  onRemove?: (index: number) => void
  canRemove?: boolean
}

export default function SongInput({
  index,
  song,
  onChange,
  onRemove,
  canRemove = true,
}: SongInputProps) {
  return (
    <div className="flex flex-col gap-2 md:flex-row md:items-center">
      <div className="flex flex-1 flex-col gap-2 md:flex-row md:items-center">
        <label className="sr-only" htmlFor={`song-title-${index}`}>
          Song title
        </label>
        <input
          id={`song-title-${index}`}
          type="text"
          value={song.title}
          onChange={(e) => onChange(index, { ...song, title: e.target.value })}
          placeholder="Song title"
          className="flex-1 rounded border border-gray-300 px-2 py-1 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-600 dark:text-white"
        />
        <span className="mx-2 hidden md:inline">by</span>
        <label className="sr-only" htmlFor={`song-artist-${index}`}>
          Artist name
        </label>
        <input
          id={`song-artist-${index}`}
          type="text"
          value={song.artist}
          onChange={(e) => onChange(index, { ...song, artist: e.target.value })}
          placeholder="Artist"
          className="flex-1 rounded border border-gray-300 px-2 py-1 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-600 dark:text-white"
        />
      </div>

      {canRemove && onRemove ? (
        <button
          type="button"
          onClick={() => onRemove(index)}
          className="rounded  px-3 py-1 text-sm text-red-500 hover:bg-red-600 hover:text-white border border-red-500 focus:outline-none focus:ring-2 focus:ring-red-500"
        >
          -
        </button>
      ) : null}
    </div>
  )
}
