from sqlalchemy.sql import func
from config import db, bcrypt, ma

players_table = db.Table('players',
                db.Column('player_id', db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False),
                db.Column('campaign_id', db.Integer, db.ForeignKey('campaign.id'), primary_key=True, nullable=False),
                db.Column('created_at', db.DateTime, nullable=False, server_default=func.now()),
                db.Column('updated_at', db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now()))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    user = db.relationship('User', back_populates="played_campaigns")
    campaign = db.relationship('Campaign', back_populates="users")

    @classmethod
    def create(cls, data, ses, id):
        new_message = cls(player_id=ses['userid'], campaign_id=id, message=data['message'])
        db.session.add(new_message)
        db.session.commit()
        return new_message

# class MessageSchema(ma.ModelSchema):
#     class Meta:
#         model = Message

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(45), nullable=False)
    pw_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    campaigns_playing = db.relationship('Campaign', secondary=players_table)
    played_campaigns = db.relationship('Message', back_populates="user")

    @classmethod
    def register(cls, data):
        pw_hash = bcrypt.generate_password_hash(data['password'])
        new_user = cls(email=data['email'],
                       pw_hash=pw_hash
                       )
        db.session.add(new_user)
        db.session.commit()
        return new_user

# class UserSchema(ma.ModelSchema):
#     class Meta:
#         model = User

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    race = db.Column(db.String(45), nullable=False)
    char_class = db.Column(db.String(45), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id], backref="characters", cascade="all")

    @classmethod
    def create(cls, data, ses):
        new_character = cls(name=data['name'], race=data['race'], char_class=data['class'], description=data['description'], user_id=ses['userid'])
        db.session.add(new_character)
        db.session.commit()
        return new_character

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    master_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    master = db.relationship('User', foreign_keys=[master_id], backref="campaigns", cascade="all")
    players = db.relationship('User', secondary=players_table)
    users = db.relationship('Message', back_populates='campaign')

    @classmethod
    def create(cls, data, ses):
        new_campaign = cls(name=data['name'], master_id=ses['userid'])
        db.session.add(new_campaign)
        db.session.commit()
        return new_campaign

# class CampaignSchema(ma.ModelSchema):
#     class Meta:
#         model = Campaign

class Update(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    update = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    campaign = db.relationship('Campaign', foreign_keys=[campaign_id], backref="updates", cascade="all")

    @classmethod
    def create(cls, data, id):
        new_update = cls(update=data['update'], campaign_id=id)
        db.session.add(new_update)
        db.session.commit()
        return new_update