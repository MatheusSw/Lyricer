import lyricsgenius
import os
import sys

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print(
            "Wrong usage, correct use: lyricsDownloader.py artist max_songs [,excluded_terms]")
        quit()

    # You can also use dotenv, as you wish.
    genius_token = os.getenv('GENIUS_TOKEN')

    # Genius comes back with a bunch of unwanted results, like Live shows and/or remixes, you may want to exclude that
    excluded_terms = ["Live", "Remix", "Inspired",
                      "Cape"] if sys.argv == 2 else sys.argv[3:]

    genius = lyricsgenius.Genius(genius_token)
    genius.skip_non_songs = True
    genius.excluded_terms = excluded_terms

    # Just hope to god they have entered the right parameters
    # Kidding
    artist = genius.search_artist(sys.argv[1], max_songs=int(sys.argv[2]))
    artist.save_lyrics()
