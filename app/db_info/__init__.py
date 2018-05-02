import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from app.config import SQLALCHEMY_DATABASE_URI

engine = sa.create_engine(SQLALCHEMY_DATABASE_URI)

Session = sessionmaker(bind=engine)