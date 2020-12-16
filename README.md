# Lyricer
Lyricer is a PoC AI with solo goal to generate new song lyrics based on short sequences.

# Installation

### Dependencies
* xlrd `pip install xlrd`
* openpyxl `pip install openpyxl`
* pandas `pip install pandas`
* tensorflow `pip install tensorflow`
_or alternatively..._
`pip install xlrd openpyxl pandas tensorflow`

### Environment
To download lyrics via Genius you need to have a [Genius Access Token](https://docs.genius.com/), and then create a system environment variable with the name `GENIUS_TOKEN`.
`set GENIUS_TOKEN your_token_here` 

### Usage
Currently you need to run `lyricsDownloader.py` with the necessary arguments, then run `LyricsFilter.js` to filter the raw results from genius.
I highly recommend for you to clean the result even more as it usually have parts like _[Chorus: Pharell Williams]_ and that doesn't work very well with our AI as it's word-based and not line-based.
