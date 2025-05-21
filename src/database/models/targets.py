from sqlalchemy import Integer, Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.database.models.base import Base


class Target(Base):
    __tablename__ = "targets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    notes = Column(String, default="")
    complete = Column(Boolean, default=False)
    mission_id = Column(Integer, ForeignKey("missions.id"))

    mission = relationship("Mission", back_populates="targets")