
from datetime import datetime
from app.manage import db

class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(20))
    street = db.Column(db.String(50))
    post_code = db.Column(db.INTEGER)
    
    def __init__(self,city,street,post_code):
        self.city = city
        self.street = street
        self.post_code = post_code



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    dob = db.Column(db.DATETIME,default=datetime.now)
    gender = db.Column(db.CHAR(1))
    phone = db.Column(db.String(10))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'),
                           nullable=False)
    address = db.relationship('Address',
                              backref=db.backref('address', lazy=True))

    active = db.Column(db.BOOLEAN)
    admin = db.Column(db.BOOLEAN)

    register_date = db.Column(db.DATETIME,default=datetime.now)

    def __init__(self,email, password ,first_name="first", last_name="last", dob=None,gender=None,phone="000000",address=None,active=True,admin=False,register_date=None):
        self.frist_name=first_name
        self.last_name=last_name
        self.email=email
        self.password=password
        self.dob=dob
        self.gender=gender
        self.phone=phone
        self.address=address
        self.active = active
        self.admin = admin
        self.register_date=register_date
        
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
        return '<User %r,%r>' % (self.first_name ,self.last_name)


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                           nullable=False)
    owner = db.relationship('User',
                              backref=db.backref('pets', lazy=True),foreign_keys=[owner_id])

    name = db.Column(db.String(20))
    gender = db.Column(db.CHAR(1))

#
# class Appointment(models.Model):
#     question = db.ForeignKey(User, on_delete=models.CASCADE)
#     choice_text = db.VARCHAR(max_length=200)
#     votes = models.IntegerField(default=0)
#
#
# class TimeSlot(models.Model):
#     question = db.ForeignKey(User, on_delete=models.CASCADE)
#     choice_text = db.VARCHAR(max_length=200)
#     votes = models.IntegerField(default=0)