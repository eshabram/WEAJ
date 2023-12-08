from flask import Flask, render_template, flash, redirect, request, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
import secrets
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import InputRequired
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests, json
from image_query import *


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
bootstrap = Bootstrap5(app)
survey_responses = []

class SurveyForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    car_choice = SelectField('Choose Your Dream Car', choices=[('tesla', 'Tesla'), ('ferrari', 'Ferrari'), ('bmw', 'BMW')], validators=[InputRequired()])
    effectiveness_rating = IntegerField('How effective was vHarmony for you? (1-10)', validators=[InputRequired()])
    recommend = SelectField('Would you recommend vHarmony to a friend?', validators=[InputRequired()])
    age = SelectField('What is your age range?', choices=[('-', '-'), ('18-24', '18-24'), ('25-35', '25-35'), ('35-44', '35-44'), ('45-65', '45-65'), ('65+', '65+')])
    

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

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    form = SurveyForm()

    if request.method == 'POST' and form.validate_on_submit():
        response = {
            'name': form.name.data,
            'effectiveness_rating': form.effectiveness_rating.data,
            'recommend': form.recommend.data,
            'age': form.age.data
        }
        survey_responses.append(response)
        return redirect(url_for('thank_you'))

    return render_template('survey.html', form=form)


@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')


if __name__ == '__main__':
    app.run(debug=True)
