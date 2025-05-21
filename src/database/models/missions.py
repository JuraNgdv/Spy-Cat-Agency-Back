from sqlalchemy import Integer, Column, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.database.models.base import Base


class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)
    complete = Column(Boolean, default=False)
    cat_id = Column(Integer, ForeignKey("spy_cats.id"), nullable=True)

    cat = relationship("SpyCat", back_populates="mission")
    targets = relationship("Target", back_populates="mission", cascade="all, delete")