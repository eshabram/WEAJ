from flask import Flask, render_template, flash, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
import requests, json
import random
import static.image_info as info

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap5(app)

my_key = 'D8FJrAVDcE5RHJ29uwD5lRftLXMDO6Tw3iGnj19V'
print(info)
payload = {
    'api_key': my_key,
    'start_date': '2023-03-09',
    'end_date': '2023-03-11'
}
endpoint = 'https://api.nasa.gov/planetary/apod'

class Playlist(FlaskForm):
    song_title = StringField(
        'Song Title',  
        validators=[DataRequired()]
    )
    artist = StringField(
        'Artist',  
        validators=[DataRequired()]
    )

playlist = []

def store_song(my_song, this_artist):
    playlist.append(dict(
        song = my_song,
        artist = this_artist,
        date = datetime.today()
    ))

@app.route('/', methods=('GET', 'POST'))
def index():
    try:
        r = requests.get(endpoint, params=payload)
        data = r.json()
        print(data)
    except:
        print('please try again')
    
    form = Playlist()
    if form.validate_on_submit():
        store_song(form.song_title.data, form.artist.data)
        return redirect('/view_playlist')
    return render_template('playlist.html', form=form, name='Elliot', data=data)

@app.route('/view_playlist')
def vp():
    return render_template('vp.html', playlist=playlist)