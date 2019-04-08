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