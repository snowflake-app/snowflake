from snowflake.db import db


class OneOnOneActionItem(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    state = db.Column(db.Boolean)
    content = db.Column(db.String)

    one_on_one_id = db.Column(db.BigInteger, db.ForeignKey('one_on_one.id'), nullable=False)
    one_on_one = db.relationship('OneOnOne', backref=db.backref('action_items', lazy=True))

    created_by_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    created_by = db.relationship('User')

    @staticmethod
    def create(action_item):
        db.session.add(action_item)
        db.session.commit()

    def update(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get(_id):
        return OneOnOneActionItem.query.get(_id)
