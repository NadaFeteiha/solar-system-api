from ..db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional


class Moon(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    size: Mapped[str]
    description: Mapped[str]
    discovered_year: Mapped[Optional[int]]
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planet.id"))
    planet: Mapped["Planet"] = relationship(back_populates="moons")

    def to_dict(self):
        return {
            "id": self.id,
            "size": self.size,
            "description": self.description,
            "discovered_year": self.discovered_year,
            "planet_id": self.planet_id,
        }

    @classmethod
    def from_dict(cls, moon_data):
        discovered_year = moon_data.get("discovered_year")
        if discovered_year is not None:
            discovered_year = int(discovered_year)

        return cls(
            size=moon_data["size"],
            description=moon_data["description"],
            discovered_year=discovered_year,
            planet_id=moon_data.get("planet_id"),
        )
