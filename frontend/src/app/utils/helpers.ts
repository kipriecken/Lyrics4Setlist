interface Song {
  title: string
  artist: string
}

export async function handleButtonClick(songs: Song[]) {
  const res = fetch('http://localhost:8000/generate-pdf', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      songs: songs.map((song) => {
        return {
          title: song.title,
          artist: song.artist,
        }
      }),
    }),
  })
    .then((response) => response.blob())
    .then((blob) => {
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'lyrics.pdf'
      document.body.appendChild(a)
      a.click()
      a.remove()
    })
    .catch((error) => {
      console.error('Error generating PDF:', error)
    })

  await res
}
