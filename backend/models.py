# SQLAlchemy models definition
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class HighScore(Base):
    __tablename__ = 'high_scores'
    id = Column(Integer, primary_key=True)
    player_name = Column(String)
    score = Column(Integer)
