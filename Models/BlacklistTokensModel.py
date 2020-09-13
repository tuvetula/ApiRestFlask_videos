import datetime
from flask import abort
from config import db , ma


class BlacklistToken(db.Model):
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)
    
    @staticmethod
    def addTokenInBlacklist(auth_token):
        blacklist_token = BlacklistToken(token=auth_token)
        try:
            # insert the token
            db.session.add(blacklist_token)
            db.session.commit()
        except Exception as e:
            abort(400,e)
    
    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True  
        else:
            return False

class BlacklistTokenSchema(ma.SQLAlchemySchema):

    class Meta:

        model = BlacklistToken
        sqla_session = db.session