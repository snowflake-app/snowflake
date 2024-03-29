from sqlalchemy import func

from ..db import db


class OneOnOne(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    created_by_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    created_by = db.relationship('User', foreign_keys=[created_by_id])

    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id])

    @staticmethod
    def get(one_on_one_id):
        return OneOnOne.query.get(one_on_one_id)

    @staticmethod
    def get_by_user(user):
        return OneOnOne.query.filter(
            (OneOnOne.user_id == user.id) | (OneOnOne.created_by_id == user.id)).all()

    def get_action_items(self):
        return self.action_items
