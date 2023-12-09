from flask import Flask, render_template, flash, redirect, request, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
import secrets
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import InputRequired
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional, ValidationError
import requests, json
from image_query import *
import pickle


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
bootstrap = Bootstrap5(app)
survey_responses = []


class SurveyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    effectiveness_rating = SelectField(
        'Effectiveness Rating',
        choices=[('', ''), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
        validators=[DataRequired()]
    )
    age = SelectField(
        'Age Range',
        choices=[('', ''), ('18-24', '18-24'), ('25-35', '25-35'), ('35-44', '35-44'), ('45-65', '45-65'), ('65+', '65+')],
        validators=[DataRequired()]
    )
    recommend = SelectField(
        'Would you recommend vHarmony to a friend?',
        choices=[('', ''), ('Yes', 'Yes'), ('No', 'No')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit')


def send_query():
    # set this to True before turning it in!!!!!
    first = True
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
            break
        first = False
    return image_url, type, make, color, condition


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
    image_url, type, make, color, condition = send_query()    
    return render_template('match.html', image_url=image_url, car_type=type, \
                           car_make=make, car_color=color, car_cond=condition)


@app.route('/match/like/<type>/<make>/<color>/<cond>', methods=['POST'])
def match_like(type, make, color, cond):
    image_url = request.form['image_url']
    # Process the 'like' action here
    count = like_data(type, make, color, cond)
    print(count)
    # our metric for ending the match process
    print(enough_data())
    if enough_data() and count > 9:
        a,b,c,d = result_data()
        print(f'{a}{b}{c}{d}')
        car = Car('',a,b,c,d)
        first = True

        while True:
            if first:
                tof, car = make_request('google', car)
            else:
                tof, car = make_request('', car)
            if tof:
                break
            first = False
            
        image_url = car.get_url()
        print(image_url)
        return render_template('matched.html', image_url=image_url)
    else:
        return redirect(url_for('match'))  


@app.route('/match/dislike', methods=['POST'])
def match_dislike():
    increment_count()
    image_url = request.form['image_url']
    # Process the 'dislike' action here
    # we essentially don't have to do anything if the user dislikes
    # print(f"Image {image_url} disliked")
    return redirect(url_for('match')) 


@app.route('/survey', methods=['GET', 'POST'])
def survey():
    form = SurveyForm()

    if form.validate_on_submit():
        response = {
            'name': form.name.data,
            'effectiveness_rating': form.effectiveness_rating.data,
            'recommend': form.recommend.data,
            'age': form.age.data
        }
        
        survey_responses.append(response)

        return redirect(url_for('thank_you'))
    return render_template('survey.html', form=form)


@app.route('/matched')
def matched():
    clear_data()
    return render_template('matched.html')


@app.route('/search')
def search():
    clear_data()
    return render_template('search.html')


@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')


@app.route('/match_clear')
def match_clear():
    clear_data()
    return redirect(url_for('match')) 


@app.route('/db', methods = ['POST', 'GET'])
def db():
    return render_template('db.html', survey_responses=survey_responses)


if __name__ == '__main__':
    app.run(debug=True)
