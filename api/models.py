from api import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), unique=True)
    items = db.relationship('Item', backref='user', lazy='dynamic')

    def get_item(self, item_id):
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def __repr__(self):
        return f'<User {self.id}>'


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def user_authorized(self, token):
        user = User.query.filter_by(id=self.user_id).first()
        return user.token == token

    def to_dict(self):
        return {
              'id': self.id
            , 'email': self.email
            , 'name': self.name
        }

    def __repr__(self):
        return f'<Item {self.id}>'



#Add to initial insert, need some random token corresponding to existing email
#change the item insert