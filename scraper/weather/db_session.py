from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
environment = os.environ.get('DJANGO_ENV') or 'development'
if environment == 'development':
    from db_details import *
else:
    from db_details import *

engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

# create a configured "Session" class
Session = sessionmaker(bind=engine)
