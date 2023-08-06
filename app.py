from flask import Flask, render_template, request, jsonify
import spotipy
import requests
import json

app = Flask(__name__)

count = 9
auth = spotipy.util.prompt_for_user_token()

@app.route('/')
def index(artists1=['drake', 'kanye west', 'eminem'], artists2=['lil wayne', 'rihanna', 'rick ross']):
# def index(artists1=['elton john', 'drake', 'lil wayne'], artists2=['dua lipa', 'britney spears', 'nicki minaj']):
    return render_template('home.html', row1_label=artists1[0], row2_label=artists1[1], row3_label=artists1[2], col1_label=artists2[0], col2_label=artists2[1], col3_label=artists2[2])

@app.route('/process_input', methods=['POST'])
def process_input(artists1=['drake', 'kanye west', 'eminem'], artists2=['lil wayne', 'rihanna', 'rick ross']):
# def process_input(artists1=['elton john', 'drake', 'lil wayne'], artists2=['dua lipa', 'britney spears', 'nicki minaj']):
    data = request.get_json()
    position = data['position']  # This will be a string like "1,1"
    row_index, col_index = map(int, position.split(','))  # Extract the row and column indices
    text_input = data['textInput']
    row_index = row_index - 1
    col_index = col_index - 1

    global count
    global auth
    count -= 1
    
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + auth,
    }
    url='https://api.spotify.com/v1/search?q=' + '+'.join(artists1[row_index].split()) + '+' + '+'.join(artists2[col_index].split()) + '&type=track&limit=50&offset=0'
    response = requests.get(url=url, headers=headers)
    results = json.loads(response.content)
    songss = {}
    for song in results['tracks']['items']:
        song_artists = []
        for artist in song['artists']:
            song_artists.append(artist['name'].lower())
        if artists1[row_index] in song_artists and artists2[col_index] in song_artists:
            if song['name'] not in songss.keys():
                songss[song['name']] = song['album']['images'][0]['url']
    if text_input in songss.keys():
        return jsonify({
            'row_index': row_index,
            'col_index': col_index,
            'correct': text_input,
            'count': count,
            'url': songss[text_input]
        })
    else:
        return jsonify({
            'row_index': row_index,
            'col_index': col_index,
            'correct': '',
            'count': count
        })# New endpoint to get options based on input text

@app.route('/get_options', methods=['POST'])
def get_options():
    data = request.get_json()
    current_input = data['current_input']

    # Call the Python function to get the options based on the current input
    options = get_options_based_on_input(current_input)
    return jsonify(options=options)

# Example Python function to get options based on input (you should implement this according to your requirements)
def get_options_based_on_input(current_input):
    # Implement your logic here to generate the options based on the current input
    # For example, you can return a list of options as follows:
    global auth
    
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + auth,
    }
    url='https://api.spotify.com/v1/search?q=' + current_input + '&type=track&limit=5&offset=0'
    response = requests.get(url=url, headers=headers)
    results = json.loads(response.content)

    songss = []
    try:
        for song in results['tracks']['items']:
            current = {}
            current['text'] = song['name']
            current['imageUrl'] = song['album']['images'][0]['url']
            songss.append(current)
        return songss
    except:
        return []

if __name__ == '__main__':
    app.run(debug=True)
