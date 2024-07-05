from application.extensions import db


class BankAccount(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    bank_account_name = db.Column(db.String(255))
    short_name = db.Column(db.String(255))
    account_code = db.Column(db.String(255))

    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'), primary_key=True)
    bank = db.relationship('Bank', backref='bank_accounts', lazy=True)

    priority = db.Column(db.Integer())
    active = db.Column(db.Boolean())

    def __str__(self):
        return self.account_code
    
    @property
    def preparer(self):
        user_prepare = UserBankAccount.query.filter(UserBankAccount.bank_account_id==self.id).first()
        return user_prepare
    
    @property
    def approved(self):
        admin_approve = AdminBankAccount.query.filter(AdminBankAccount.bank_account_id==self.id).first()
        return admin_approve


class UserBankAccount(db.Model):
    bank_account_id = db.Column(db.Integer, db.ForeignKey('bank_account.id'), primary_key=True)
    bank_account = db.relationship('BankAccount', backref='user_prepare', lazy=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', backref='bank_account_prepared', lazy=True)

    def __str__(self):
        return self.user.user_name

    def __repr__(self):
        return self.user.user_name


class AdminBankAccount(db.Model):
    bank_account_id = db.Column(db.Integer, db.ForeignKey('bank_account.id'), primary_key=True)
    bank_account = db.relationship('BankAccount', backref='user_approved', lazy=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', backref='bank_account_approved', lazy=True)
