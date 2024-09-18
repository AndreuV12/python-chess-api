from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .opening_model import Opening
from .user_model import User
