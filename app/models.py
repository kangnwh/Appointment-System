from datetime import datetime
from app.manage import db


class Address(db.Model):
    __tablename__ = 'Address'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(20))
    street = db.Column(db.String(50))
    post_code = db.Column(db.INTEGER)

    def __init__(self, city, street, post_code):
        self.city = city
        self.street = street
        self.post_code = post_code


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    dob = db.Column(db.DATE, default=datetime.now)
    gender = db.Column(db.CHAR(1))
    phone = db.Column(db.String(10))
    home_number = db.Column(db.String(10))
    work_number = db.Column(db.String(10))
    address_id = db.Column(db.Integer, db.ForeignKey('Address.id'),
                           nullable=False)
    address = db.relationship('Address')

    active = db.Column(db.BOOLEAN)
    admin = db.Column(db.BOOLEAN)

    register_date = db.Column(db.DATETIME, default=datetime.now)

    def __init__(self, email, password, first_name="first", last_name="last", dob=None, gender=None, phone="000000",home_number="000000",work_number="000000",
                 address=None, active=True, admin=False, register_date=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.dob = dob
        self.gender = gender
        self.phone = phone
        self.home_number = home_number
        self.work_number = work_number
        self.address = address
        self.active = active
        self.admin = admin
        self.register_date = register_date

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def is_admin(self):
        return self.admin

    def __repr__(self):
        return '<User %r,%r>' % (self.first_name, self.last_name)


class Pet(db.Model):
    __tablename__ = "Pet"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('User.id'),
                         nullable=False)
    owner = db.relationship('User',
                            backref=db.backref('pets', lazy=True), foreign_keys=[owner_id])

    name = db.Column(db.String(20))
    breed = db.Column(db.String(20))
    gender = db.Column(db.CHAR(1))
    dob = db.Column(db.DATE, default=datetime.now)

    def __init__(self, owner,name,breed,gender,dob):
        self.owner = owner
        self.name = name
        self.breed = breed
        self.gender = gender
        self.dob = dob


class Card(db.Model):
    __tablename__ = "Card"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('User.id'),
                         nullable=False)
    owner = db.relationship('User',
                            backref=db.backref('cards', lazy=True), foreign_keys=[owner_id])
    card_num = db.Column(db.String(16))
    bank = db.Column(db.String(5))

    def __init__(self,owner,card_num,bank):
        self.owner = owner
        self.card_num = card_num
        self.bank = bank


class Service(db.Model):
    __tablename__ = "Service"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    desc = db.Column(db.String(50))
    fee = db.Column(db.FLOAT)

    def __init__(self,type,desc,fee):
        self.type = type
        self.desc = desc
        self.fee = fee



class ApptTimeSlot(db.Model):
    __tablename__ = "ApptTimeSlot"
    id = db.Column(db.Integer, primary_key=True)
    slot = db.Column(db.String(5))

    def __init__(self,slot):
        self.slot = slot


class Appt(db.Model):
    __tablename__ = "Appt"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('User.id'),
                         nullable=False)
    owner = db.relationship('User',
                            backref=db.backref('appts', lazy=True), foreign_keys=[owner_id])
    appt_date = db.Column(db.DATE)
    appt_timeslot_id = db.Column(db.Integer, db.ForeignKey('ApptTimeSlot.id'),
                         nullable=False)
    appt_timeslot = db.relationship('ApptTimeSlot',
                            backref=db.backref('appt', lazy=True), foreign_keys=[appt_timeslot_id])
    update_date = db.Column(db.DATE,default=datetime.now)

    def __init__(self,owner_id,appt_date,appt_timeslot_id):
        self.owner_id = owner_id
        self.appt_date = appt_date
        self.appt_timeslot_id = appt_timeslot_id



class Appt2Ser(db.Model):
    __tablename__ = "Appt2Ser"
    id = db.Column(db.Integer, primary_key=True)
    appt_id = db.Column(db.Integer, db.ForeignKey('Appt.id'),
                         nullable=False)
    appt = db.relationship('Appt',
                            backref=db.backref('appt_service', lazy=True), foreign_keys=[appt_id])

    service_id = db.Column(db.Integer, db.ForeignKey('Service.id'),
                        nullable=False)
    service = db.relationship('Service',foreign_keys=[service_id])

    def __init__(self,appt,service_id):
        self.appt = appt
        self.service_id = service_id


class Bill(db.Model):
    __tablename__ = "bill"
    id = db.Column(db.Integer, primary_key=True)

    owner_id = db.Column(db.Integer, db.ForeignKey('User.id'),
                         nullable=False)
    owner = db.relationship('User',
                            backref=db.backref('bill', lazy=True), foreign_keys=[owner_id])

    appt_id = db.Column(db.Integer, db.ForeignKey('Appt.id'),
                        nullable=False)
    appt = db.relationship('Appt',
                           backref=db.backref('bill', lazy=True), foreign_keys=[appt_id])
    total_fee = db.Column(db.FLOAT)
    is_credited = db.Column(db.CHAR(1),default=False)
    is_paid = db.Column(db.CHAR(1),default=False)


    def __init__(self,appt,owner_id,total_fee):
        self.appt = appt
        self.owner_id = owner_id
        self.total_fee = total_fee
