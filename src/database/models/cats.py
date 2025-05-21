from sqlalchemy import Integer, Column, String, Float, Numeric
from sqlalchemy.orm import relationship

from src.database.models import Base


class SpyCat(Base):
    __tablename__ = "spy_cats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    experience = Column(Integer, nullable=False)
    breed = Column(String, nullable=False)
    salary = Column(Numeric(precision=12, scale=2), nullable=False)

    mission = relationship("Mission", back_populates="cat", uselist=False)