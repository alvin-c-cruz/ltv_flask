from application.extensions import db


class Bank(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    bank_name = db.Column(db.String(255))
    short_name = db.Column(db.String(255))
    bank_code = db.Column(db.String(255))
    priority = db.Column(db.Integer())
    active = db.Column(db.Boolean())

    def __str__(self):
        return self.bank_code
    
    @property
    def preparer(self):
        user_prepare = UserBank.query.filter(UserBank.bank_id==self.id).first()
        return user_prepare
    
    @property
    def approved(self):
        admin_approve = AdminBank.query.filter(AdminBank.bank_id==self.id).first()
        return admin_approve


class UserBank(db.Model):
    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'), primary_key=True)
    bank = db.relationship('Bank', backref='user_prepare', lazy=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', backref='bank_prepared', lazy=True)

    def __str__(self):
        return self.user.user_name

    def __repr__(self):
        return self.user.user_name


class AdminBank(db.Model):
    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'), primary_key=True)
    bank = db.relationship('Bank', backref='user_approved', lazy=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', backref='bank_approved', lazy=True)
