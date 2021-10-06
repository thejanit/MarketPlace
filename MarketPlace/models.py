from MarketPlace import db, login_manager
from MarketPlace import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_add = db.Column(db.String(length=50), nullable=False, unique=True)
    passwd_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), default=50000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def pretty_budget(self):
        if len(str(self.budget)) >= 4:
            return f'₹ {str(self.budget)[:-3]},{str(self.budget)[-3:]}'

        else:
            return f'₹ {self.budget}'

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.passwd_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.passwd_hash, attempted_password)

    def can_buy(self, item_obj):
        return self.budget >= item_obj.price

    def can_sell(self, item_obj):
        return item_obj in self.items


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=20), nullable=False, unique=True)
    barcode = db.Column(db.String(length=14), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(length=1000), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'

    def bought_owner(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sold_owner(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()