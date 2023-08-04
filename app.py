from flask import Flask, render_template, request, jsonify
import spotipy
import requests
import json

app = Flask(__name__)

@app.route('/')
def index(artists1=['drake', 'kanye west', 'eminem'], artists2=['lil wayne', 'rihanna', 'rick ross']):
    return render_template('home.html', row1_label=artists1[0], row2_label=artists1[1], row3_label=artists1[2], col1_label=artists2[0], col2_label=artists2[1], col3_label=artists2[2])

@app.route('/process_input', methods=['POST'])
def process_input(artists1=['drake', 'kanye west', 'eminem'], artists2=['lil wayne', 'rihanna', 'rick ross']):
    data = request.get_json()
    position = data['position']  # This will be a string like "1,1"
    row_index, col_index = map(int, position.split(','))  # Extract the row and column indices
    text_input = data['textInput']

    
    auth = spotipy.util.prompt_for_user_token()
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + auth,
    }
    url='https://api.spotify.com/v1/search?q=' + '+'.join(artists1[row_index].split()) + '+' + '+'.join(artists2[col_index].split()) + '&type=track&limit=50&offset=0'
    response = requests.get(url=url, headers=headers)
    results = json.loads(response.content)
    songss = []
    for song in results['tracks']['items']:
        song_artists = []
        for artist in song['artists']:
            song_artists.append(artist['name'].lower())
        if artists1[row_index] in song_artists and artists2[col_index] in song_artists:
            songss.append(song['name'].lower())
    if text_input in songss:
        print(row_index, col_index, text_input)
    else:
        print("INCORRECt")
        print(songss)


    
    # Now you can pass the row index, column index, and text input to your Python function
    # For example, let's just return the received data as a response
    return jsonify({
        'row_index': row_index,
        'col_index': col_index,
        'text_input': text_input
    })

if __name__ == '__main__':
    app.run(debug=True)
