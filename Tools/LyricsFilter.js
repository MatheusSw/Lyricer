//Change this to a python script, just so everything is normalized..
const {readFileSync, writeFileSync} = require('fs')

const input_file = 'Lyrics_KanyeWest.json'
const output_file = 'Lyrics/KanyeWest_filtered.json'

const raw = readFileSync(input_file)

const json = JSON.parse(raw)

const modified = json.songs.map(({ title, release_date_for_display: release, lyrics, album }) => ({
    title,
    release,
    lyrics,
    "album": album ? album.name : null,
}))

writeFileSync(output_file, JSON.stringify(modified))