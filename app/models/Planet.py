from ..db import db
from sqlalchemy.orm import Mapped, mapped_column


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    number_of_moons: Mapped[int]


