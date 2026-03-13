# Database connection using SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///high_scores.db')
Session = sessionmaker(bind=engine)
db = Session()
