from ..db import db
from sqlalchemy.orm import Mapped, mapped_column


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]



planets = [
#     Planet(1, "Mercury", "Terrestrial"),
#     Planet(2, "Venus", "Terrestrial"),
#     Planet(3, "Earth", "Terrestrial"),
#     Planet(4, "Mars", "Terrestrial"),
#     Planet(5, "Jupiter", "Gas Giant"),
#     Planet(6, "Saturn", "Gas Giant"),
#     Planet(7, "Uranus", "Ice Giant"),
#     Planet(8, "Neptune", "Ice Giant"),
]

