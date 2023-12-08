from flask import Flask, render_template, flash, redirect, request, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests, json
from image_query import *

app = Flask(__name__)
bootstrap = Bootstrap5(app)

@app.route('/')
def index():
    clear_data()
    return render_template('index.html')

@app.route('/about')
def about():
    clear_data()
    return render_template('about.html')

@app.route('/match')
def match():
    # keep this false until before we turn it in.
    first = False
    while True:
        # query until we find a match. Google once, and then fall back on pixabay
        if first:
            tof, car_image = query('google')
        else:
            tof, car_image = query('')
        if tof:
            # car info
            image_url = car_image.get_url()
            type = car_image.get_type()
            make = car_image.get_make()
            color = car_image.get_color()
            condition = car_image.get_condition()
            print(f'{type_likes} {make_likes} {color_likes} {condition_likes}')
            print(f'{color.upper()} {make.upper()} {type.upper()} in {condition.upper()}" condition')
            break
        first = False

    return render_template('match.html', image_url=image_url, car_type=type, \
                           car_make=make, car_color=color, car_cond=condition)

@app.route('/match/like/<type>/<make>/<color>/<cond>', methods=['POST'])
def match_like(type, make, color, cond):
    image_url = request.form['image_url']
    # Process the 'like' action here
    like_data(type, make, color, cond)
    print(f"Image {image_url} liked")
    return redirect(url_for('match'))  # Redirect to the match page or another page

@app.route('/match/dislike', methods=['POST'])
def match_dislike():
    image_url = request.form['image_url']
    # Process the 'dislike' action here
    # we essentially don't have to do anything if the user dislikes
    print(f"Image {image_url} disliked")
    return redirect(url_for('match'))  # Redirect to the match page or another page

@app.route('/search')
def search():
    clear_data()
    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)
