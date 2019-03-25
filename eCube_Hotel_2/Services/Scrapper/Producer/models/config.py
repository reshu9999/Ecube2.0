from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

Base=automap_base()

engine=create_engine('mysql://root:Eclerx#123@192.168.131.23/eCube_Centralized_DB')

Base.prepare(engine,reflect=True)
session=Session(engine)
