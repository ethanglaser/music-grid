'''
ideas:
1. set up spotify API call for item search with artists for song
2. input 2 3-element lists of artist names, display board and take in song title and grid location
'''
import requests
import spotipy
import json
from math import floor, ceil

def spotify_artists_query(auth, artist1, artist2):
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + auth,
    }
    url='https://api.spotify.com/v1/search?q=' + '+'.join(artist1.split()) + '+' + '+'.join(artist2.split()) + '&type=track&limit=50&offset=0'
    response = requests.get(url=url, headers=headers)
    results = json.loads(response.content)
    songss = []
    for song in results['tracks']['items']:
        song_artists = []
        for artist in song['artists']:
            song_artists.append(artist['name'].lower())
        if artist1 in song_artists and artist2 in song_artists:
            songss.append(song['name'].lower())
    return songss

def generate_grid(artists1, artists2, songs, guess):
    print("Guesses remaining: " + str(9 - guess) + "/9")
    first_row = ' ' * 20
    for i in range(len(artists1)):
        first_row += ((10 - floor(len(artists1[i]) / 2)) * ' ' + artists1[i] + (10 - ceil(len(artists1[i]) / 2)) * ' ')
    print(first_row)
    for i2, a in enumerate(artists2):
        row = (10 - floor(len(a) / 2)) * ' ' + a + (10 - ceil(len(a) / 2)) * ' '
        for i in range(len(artists1)):
            row += (10 - floor(len(songs[i2][i]) / 2)) * ' ' + songs[i2][i] + ' ' * (10 - ceil(len(songs[i2][i]) / 2))
        print(row)

auth = spotipy.util.prompt_for_user_token()

artists1 = []
artists2 = []
songs_inner = []
songs = []
for i in range(3):
    artists1.append(input("Enter list of first 3 artists: "))
    songs_inner.append('')
for i in range(3):
    artists2.append(input("Enter list of second 3 artists: "))
    songs.append(songs_inner.copy())

for guess in range(9):
    generate_grid(artists1, artists2, songs, guess)
    index1 = int(input("Enter column index: "))
    index2 = int(input("Enter row index: "))
    artist1 = artists1[index1]
    artist2 = artists2[index2]
    guess = input("Enter song name: ")
    songss = spotify_artists_query(auth, artist1, artist2)
    if guess in songss:
        songs[index2][index1] = guess



# spotify_artists_query(spotipy.util.prompt_for_user_token(), 'drake', 'rihanna')