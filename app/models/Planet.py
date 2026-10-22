from app.models.Moon import Moon

from ..db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    number_of_moons: Mapped[int]
    moons: Mapped[list["Moon"]] = relationship(back_populates="planet")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "num_moons": self.number_of_moons,
        }

    @classmethod
    def from_dict(cls, planet_data):
        return cls(
            name=planet_data["name"],
            description=planet_data["description"],
            number_of_moons=int(planet_data["num_moons"]),
        )
