"""
Course: CST205 Multimedia Programming and Design
Title: vHarmony
Abstract: A matching making website, matching users with the car of their dreams

Authors:
- Elliot Shabram - Project Lead, Backend/Frontend Developer
- Joshua Rivera - Backend/Frontend Developer
- Angel Medina - Backend/Frontend Developer
- Wessal Aman - Backend/Frontend Developer

Date: 12/11/2023

Description:
A Flask web application for matching users with the vehicle of their dreams using user preference data collected through our custom matching process. The website queries both Google and Pixabay with randomized search parameters and presents a vehicle fitting those specifications to the user. The user then likes or dislikes the presented vehicle, and a new search query is made. Our algorithm determines when enough data has been collected by checking that at least two categories show significant preference, which then prompts the final query with the parameters determined by the algorithm and presents the results to the user. There is also a final survey asking the user how successful our matching process was, and puts those surveys in our little database /db. 
"""
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

# set up main app, secret token, and boostrap
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
bootstrap = Bootstrap5(app)
survey_responses = []


class SurveyForm(FlaskForm):
    """
    By Angel Medina
    A class for storing the data for our survey forms.
    """
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
    """
    By Elliot Shabram
    This function initiates the random query to the image_query.py script
    """
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
    """
    By Elliot Shabram
    This function handles the rendering of the home page.
    """
    clear_data()
    return render_template('index.html')


@app.route('/about')
def about():
    """
    By Elliot Shabram
    This function handles the rendering of the about me page.
    """
    clear_data()
    return render_template('about.html')


@app.route('/match')
def match():
    """
    By Elliot Shabram, Joshua Rivera
    sends initiates the random query and then renders template with the results
    """
    image_url, type, make, color, condition = send_query()    
    return render_template('match.html', image_url=image_url, car_type=type, \
                           car_make=make, car_color=color, car_cond=condition)


@app.route('/match/like/<type>/<make>/<color>/<cond>', methods=['POST'])
def match_like(type, make, color, cond):
    """
    By Wessal Aman and Elliot Shabram
    This functino takes paramaters, checks if we have collected enough data, and 
    initiates the final request if we have enough. If we haven't collected enough
    data, then we route back to match, and if we have, we route to the matched page
    
    """
    image_url = request.form['image_url']

    # Process the 'like' action here
    count = like_data(type, make, color, cond)

    # our metric for ending the match process
    if enough_data() and count > 9:
        a,b,c,d = result_data()
        # print(f'{a}{b}{c}{d}')
        car = Car('',a,b,c,d)
        first = True

        # Google has limited queries (100 per DAY!)
        while True:
            if first:
                tof, car = make_request('google', car)
            else:
                tof, car = make_request('', car)
            if tof:
                break
            first = False
            
        image_url = car.get_url()
        return render_template('matched.html', image_url=image_url)
    else:
        return redirect(url_for('match'))  


@app.route('/match/dislike', methods=['POST'])
def match_dislike():
    """
    By Wessal Aman
    Process the 'dislike' action here we essentially don't have to do anything if the user dislikes.
    """
    increment_count()
    image_url = request.form['image_url']
    return redirect(url_for('match')) 


@app.route('/survey', methods=['GET', 'POST'])
def survey():
    """
    By Angel Medina
    This function handles the survey route and rendering. It also validates the form that is created
    upon user submission, and appends them to the list (our little fake database)
    """
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
    """
    By Elliot Shabram
    This function handles the matched route for presenting the results.
    """
    clear_data()
    return render_template('matched.html')


@app.route('/search')
def search():
    """
    By Elliot Shabram
    This function handles the google search page.
    """
    clear_data()
    return render_template('search.html')


@app.route('/thank_you')
def thank_you():
    """
    By Angel Medina
    This function handles the thank you page for completion of the survey.
    """
    return render_template('thank_you.html')


@app.route('/match_clear')
def match_clear():
    """
    By Elliot Shabram
    This page is routed to when menu item is hit, which clears the data. This is so we can use
    the rerouting method to present the match page without losing data, but erase the data when 
    we purposefully navigate away from the page.
    """
    clear_data()
    return redirect(url_for('match')) 


@app.route('/db', methods = ['POST', 'GET'])
def db():
    """
    By Elliot Shabram
    This function handles the page that prints the survey database.
    """
    return render_template('db.html', survey_responses=survey_responses)


if __name__ == '__main__':
    app.run(debug=True)
