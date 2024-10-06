# models/bmi_entry.py
from flask_login import UserMixin

from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey
from . import db

class BMIEntry(db.Model):
    __tablename__ = 'BMIEntries'
    id: Mapped[int] = mapped_column(primary_key=True)
    bmi: Mapped[float] = mapped_column(nullable=False)
    classification: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(nullable=False)

    # Foreign Key referencing UserDetails.id
    user_id: Mapped[int] = mapped_column(ForeignKey("UserDetails.id"), nullable=False)
    user = relationship("User", back_populates="bmi_entries")

    def __repr__(self):
        return f'<BMIEntry {self.bmi} - {self.classification}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
