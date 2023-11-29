from flask import Flask, render_template, flash, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests, json
from image_query import query, make_request, Car

app = Flask(__name__)
bootstrap = Bootstrap5(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
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
            print(f'{color.upper()}   {make.upper()} - {type.upper()} in   "{condition.upper()}"   condition')
            break
        first = False

    return render_template('match.html', image_url=image_url)

@app.route('/search')
def search():
    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)
