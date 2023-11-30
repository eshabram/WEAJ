from flask import Flask, render_template, flash, redirect, request, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
import secrets
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import InputRequired
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests, json


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
bootstrap = Bootstrap5(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/match')
def match():
    return render_template('match.html')


class SurveyForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    car_choice = SelectField('Choose Your Dream Car', choices=[('tesla', 'Tesla'), ('ferrari', 'Ferrari'), ('bmw', 'BMW')], validators=[InputRequired()])
    effectiveness_rating = IntegerField('How effective was vHarmony for you? (1-10)', validators=[InputRequired()])
    
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
