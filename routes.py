from config import app
from controller_functions import *

app.add_url_rule('/', view_func=index)
app.add_url_rule('/registration', view_func=registration)
app.add_url_rule('/register', view_func=register, methods=['POST'])
app.add_url_rule('/validate_email', view_func=validate_email, methods=['POST'])
app.add_url_rule('/login', view_func=login, methods=['POST'])
app.add_url_rule('/logout', view_func=logout)
app.add_url_rule('/campaigns/create', view_func=new_campaign, methods=['POST'])
app.add_url_rule('/campaigns/<id>', view_func=show_campaign)
app.add_url_rule('/getuserid', view_func=get_user_id)

#search and add player
app.add_url_rule('/validate/<id>/user', view_func=validate_user)
app.add_url_rule('/campaign/<id>/addplayer', view_func=add_player, methods=['POST'])

#adds character
app.add_url_rule('/addcharacter', view_func=add_character, methods=['POST'])

#adds update to log
app.add_url_rule('/campaign/<id>/update', view_func=add_update, methods=['POST'])

#chat
app.add_url_rule('/campaign/<id>/message', view_func=message, methods=['POST'])
app.add_url_rule('/refresh/<id>', view_func=refresh)