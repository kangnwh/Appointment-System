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

insert into user values(1,"f","l","123@12.com","pwd","2015-03-03","M","12344",1,1,0,"2015-03-03");
insert into user values(2,"Tom","Unimelb","tom@pet.com","pwd","2015-03-03","M","12344",1,1,1,"2015-03-03");


```