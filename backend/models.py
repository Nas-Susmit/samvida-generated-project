import uuid
from sqlalchemy import Column, String, DateTime, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Calculation(Base):
    __tablename__ = "calculations"

    # Using String for UUID in SQLite as it doesn't have a native UUID type.
    # The default generates a new UUID string when a new record is created.
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    expression = Column(String, nullable=False, index=True)
    result = Column(String, nullable=False)
    # unit_mode is stored as a string, e.g., 'degrees' or 'radians'
    unit_mode = Column(String(10), nullable=False, default="degrees")
    # timestamp with timezone for better universal time representation.
    # server_default=text("CURRENT_TIMESTAMP") uses the database's current timestamp function.
    timestamp = Column(DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    def __repr__(self):
        return (
            f"<Calculation(id='{self.id}', expression='{self.expression}', "
            f"result='{self.result}', unit_mode='{self.unit_mode}', timestamp='{self.timestamp}')>"
        )

