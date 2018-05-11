from app.manage import db, app
from app.models import *
from app.db_info import Session
import datetime as dt

SERVICES = [
    ["Grooming", "Description for this service", 15],
    ["Wash", "Description for this service", 15],
    ["Skin Treatment", "Description for this service", 15],
    ["other type 1", "Description for this service", 15],
    ["other type 2", "Description for this service", 15]
]

def mock():
    with app.app_context():
        recreate_db()
        mock_user_pet()
        mock_appt_slot()
        mock_service()
        mock_appt_bill()

def recreate_db():
    db.drop_all()
    db.create_all()

def mock_user_pet():
    with app.app_context():
        session = Session()
        address = Address("Melbourne", "Queen", 3000)
        tom = User(email="tom@pet.com", password="pwd", first_name="Tom", last_name="Unimelb", dob=dt.date(1989, 9, 8),
                   gender="M", phone="000000", home_number="000000", work_number="000000",
                   address=address, active=True, admin=True, register_date=dt.datetime.now())
        user1 = User(email="user1@12.com", password="pwd", first_name="User1", last_name="Unimelb",
                     dob=dt.date(1999, 12, 8), gender="M", phone="000000", home_number="000000", work_number="000000",
                     address=address, active=True, admin=False, register_date=dt.datetime.now())
        user2 = User(email="user2@12.com", password="pwd", first_name="User2", last_name="Unimelb",
                     dob=dt.date(1988, 7, 17), gender="F", phone="000000", home_number="000000", work_number="000000",
                     address=address, active=True, admin=False, register_date=dt.datetime.now())

        pet1 = Pet(user1, "Puppy1", "breed1", "M", dt.date(2017, 7, 11))
        pet2 = Pet(user1, "Puppy2", "breed2", "M", dt.date(2017, 7, 12))
        pet3 = Pet(user1, "Puppy3", "breed3", "F", dt.date(2017, 7, 13))

        card1 = Card(user1, "1234567890123456", "ANZ")
        card2 = Card(user1, "2234567890123456", "ANZ")

        session.add(address)
        session.add(tom)
        session.add(user1)
        session.add(user2)
        session.add(pet1)
        session.add(pet2)
        session.add(pet3)
        session.add(card1)
        session.add(card2)
        session.commit()

def mock_appt_slot():
    with app.app_context():
        session = Session()
        slots = ["9:30 - 10:00", "10:00 - 11:30", "12:30 - 14:00", "14:00 - 15:30", "15:30 - 17:00",
                 "17:00 - 18:30"]
        for s in slots:
            time_slot = ApptTimeSlot(s)
            session.add(time_slot)
        session.commit()


def mock_service():
    with app.app_context():
        session = Session()

        for s in SERVICES:
            service = Service(s[0], s[1], s[2])
            session.add(service)

        session.commit()


def mock_appt_bill():
    with app.app_context():
        session = Session()
        appts = [
            [2,dt.date(2018, 7, 17),2, [1,2]],
            [2, dt.date(2018, 7, 18), 3,[2,3]],
            [2, dt.date(2018, 7, 19), 1,[1,4]],
        ]
        for a in appts:
            appt = Appt(a[0],a[1],a[2])
            session.add(appt)
            total_fee = 0
            for s in a[3]:
                appt_service = Appt2Ser(appt, s)
                total_fee += SERVICES[s][2]
                session.add(appt_service)
            bill = Bill(appt,2,total_fee)
            session.add(bill)
        session.commit()


"""
```sql
insert into address values(1,"mel","la",3000);

insert into user(id,first_name,last_name,email,password,dob,gender,address_id,phone,active,admin,register_date) values(1,"f","l","123@12.com","pwd","2015-03-03","M",1,"12344",1,0,"2015-03-03");
insert into user(id,first_name,last_name,email,password,dob,gender,address_id,phone,active,admin,register_date) values(2,"Tom","Unimelb","tom@pet.com","pwd","2015-03-03","M",1,"12344",1,1,"2015-03-03");

insert into pet(id,owner_id,name,breed,gender,dob) values(1,1,"Puppy1","breed1","M","2018-05-01");
insert into pet(id,owner_id,name,breed,gender,dob) values(2,1,"Puppy2","breed2","F","2018-05-01");
insert into pet(id,owner_id,name,breed,gender,dob) values(3,1,"Puppy3","breed3","M","2018-05-01");


```
"""
