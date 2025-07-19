from apple_music_scraper import *

result = search('night tapes')
artists = result['artists']

artist_url = artists[0]['url']
artist = artist_scrape(artist_url)

latest_night_tapes_song_url = artist['latest']

song = album_scrape(latest_night_tapes_song_url)
song_name = song['title']
song_cover = song['image']

print(f"\nLatest Night Tapes Song: {song_name}\nCover Art: {song_cover}\n")
