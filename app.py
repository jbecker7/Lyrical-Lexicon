from flask import Flask, render_template, request
import lyricsgenius as genius
import lyricsgenius
import re
import string
key = ""

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    artist = request.form['artist']
    common_words = get_common_words(artist)
    return render_template('results.html', common_words=common_words)

@app.route('/results')
def results():
    return render_template('results.html', common_words=common_words)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        artist = request.form['artist']
        # get the most common words used in the artist's songs
        common_words = get_common_words(artist)
        # render the results template and pass the common words as a variable
        return render_template('results.html', common_words=common_words)
    return render_template('index.html')

def get_common_words(artist):
    genius_api = lyricsgenius.Genius(key)
    artist_songs = genius_api.search_artist(artist, max_songs=20)
    lyrics = ""
    for song in artist_songs.songs:
        lyrics +=song.lyrics + " "
    lyrics=lyrics.lower()
    words = lyrics.split()
    # remove special characters or punctuations... this is a work in progress
    words = [re.sub(r'[^\w\s]', '', word) for word in words]
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    most_common = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:30]
    return most_common


if __name__ == '__main__':
    app.run(debug=True)
