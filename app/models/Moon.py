from ..db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional


class Moon(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    size: Mapped[str]
    description: Mapped[str]
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planet.id"))
    planet: Mapped["Planet"] = relationship(back_populates="moons")

    def to_dict(self):
        return {
            "id": self.id,
            "size": self.size,
            "description": self.description,
            "planet_id": self.planet_id,
        }

    @classmethod
    def from_dict(cls, moon_data):
        return cls(size=moon_data["size"], description=moon_data["description"])
