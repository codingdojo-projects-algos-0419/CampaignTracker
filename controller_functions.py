from flask import render_template, redirect, request, session
from config import db
from models import *

def index():
    if 'userid' in session:
        campaigns = Campaign.query.all()
        print(len(campaigns))
        return render_template('dashboard.html', campaigns=campaigns)
    return render_template('login.html')

def registration():
    if 'userid' in session:
        return redirect('/')
    return render_template('register.html')


def validate_email():
    user = User.query.filter_by(email=request.form['email']).first()
    return str(user.email)

def register():
    new_user = User.register(request.form)
    session['userid'] = new_user.id
    return redirect('/')

def login():
    user = User.query.filter_by(email=request.form['email']).first()

    if user and bcrypt.check_password_hash(user.pw_hash, request.form['password']):
        session['userid'] = user.id
        return redirect('/')
    return ('', 204)

def logout():
    session.pop('userid')
    return redirect('/')

#---------------------CAMPAIGNS---------------------

def new_campaign():
    new_campaign = Campaign.create(request.form, session)
    return redirect('/campaigns/{}'.format(new_campaign.id))

def show_campaign(id):
    if 'userid' not in session:
        return redirect('/')
    campaign = Campaign.query.get(id)
    return render_template('campaign.html', campaign=campaign)