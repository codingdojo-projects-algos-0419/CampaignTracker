from flask import render_template, redirect, request, session, jsonify
from config import db
from models import *

def index():
    if 'userid' in session:
        current_user = User.query.get(session['userid'])
        user_campaigns = current_user.campaigns
        player_campaigns = current_user.campaigns_playing
        return render_template('dashboard.html', user_campaigns=user_campaigns, player_campaigns=player_campaigns)
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
    master = campaign.master
    players = campaign.players
    updates = Update.query.all()
    messages = Message.query.filter_by(campaign_id=id)
    return render_template('campaign.html', campaign=campaign, master=master, players=players, updates=updates, messages=messages)

#-----PLAYERS-----

def get_user_id():
    return str(session['userid'])

def validate_user(id):
    campaign = Campaign.query.get(id)
    players = campaign.players
    user = User.query.filter_by(email=request.args.get('search')).first()
    master = User.query.get(session['userid'])
    if master.email == user.email:
        return False
    for player in players:
        if player.email ==  user.email:
            return False
    return str(user.email)

def add_player(id):
    print('*'*80)
    user = User.query.filter_by(email=request.form['search']).first()
    campaign = Campaign.query.get(id)
    campaign.players.append(user)
    db.session.commit()
    return str(user.email)

def add_character():
    character = Character.create(request.form, session)
    return str(session['userid'])

#-----UPDATES-----

def add_update(id):
    update = Update.create(request.form, id)
    date = update.created_at.strftime('%B %d %Y')
    return date

#-----CHAT-----

def message(id):
    message = Message.create(request.form, session, id)
    user = User.query.get(session['userid'])
    return str(user.email)

def refresh(id):
    pass
#     length = Message.query.filter_by(campaign_id=id).count()
#     old_length = length
#     while old_length == length:
#         length = Message.query.filter_by(campaign_id=id).count()
#     message = Message.query.filter_by(campaign_id=id).order_by(Message.created_at.desc()).first()
#     if message.player_id == session['userid']:
#         return False
#     message_schema = MessageSchema()
#     output = message_schema.dump(message).data
#     return jsonify({'message': 'output'})