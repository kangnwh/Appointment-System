```python
from app.manage import db,app
from app.models import *
from app.db_info import Session
with app.app_context():
    db.drop_all()
    db.create_all()
    session = Session()
    session.query(User).all()
```

```sql
insert into address values(1,"mel","la",3000);

insert into user(id,first_name,last_name,email,password,dob,gender,address_id,active,admin,register_date) values(1,"f","l","123@12.com","pwd","2015-03-03","M","12344",1,1,0,"2015-03-03");
insert into user(id,first_name,last_name,email,password,dob,gender,address_id,active,admin,register_date) values(2,"Tom","Unimelb","tom@pet.com","pwd","2015-03-03","M","12344",1,1,1,"2015-03-03");

insert into pet(id,owner_id,name,breed,gender,dob) values(1,1,"Puppy1","breed1","M","2015-03-03");
insert into pet(id,owner_id,name,breed,gender,dob) values(2,1,"Puppy2","breed2","F","2015-03-03");
insert into pet(id,owner_id,name,breed,gender,dob) values(3,1,"Puppy3","breed3","M","2015-03-03");


```