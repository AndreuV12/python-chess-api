from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .opening import Opening
from .user import User
