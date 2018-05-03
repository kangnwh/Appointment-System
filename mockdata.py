from app.manage import db,app
from app.models import *
from app.db_info import Session
import datetime as dt


def mock():
        with app.app_context():
            db.drop_all()
            db.create_all()
            session = Session()
            address = Address("Melbourne","Queen",3000)
            tom = User(email="tom@pet.com", password="pwd", first_name="Tom", last_name="Unimelb", dob=dt.date(1989,9,8), gender="M", phone="000000",home_number="000000",work_number="000000",
                         address=address, active=True, admin=True, register_date=dt.datetime.now())
            user1 = User(email="user1@12.com", password="pwd", first_name="User1", last_name="Unimelb", dob=dt.date(1999,12,8), gender="M", phone="000000",home_number="000000",work_number="000000",
                         address=address, active=True, admin=False, register_date=dt.datetime.now())
            user2 = User(email="user2@12.com", password="pwd", first_name="User2", last_name="Unimelb", dob=dt.date(1988,7,17), gender="F", phone="000000",home_number="000000",work_number="000000",
                         address=address, active=True, admin=False, register_date=dt.datetime.now())

            pet1 = Pet(user1,"Puppy1","breed1","M",dt.date(2017,7,11))
            pet2 = Pet(user1,"Puppy2","breed2","M",dt.date(2017,7,12))
            pet3 = Pet(user1,"Puppy3","breed3","F",dt.date(2017,7,13))

            session.add(address)
            session.add(tom)
            session.add(user1)
            session.add(user2)
            session.add(pet1)
            session.add(pet2)
            session.add(pet3)
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