from ..db import db
from sqlalchemy.orm import Mapped, mapped_column


class Moon(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    size: Mapped[str]
    description: Mapped[str]

    def to_dict(self):
        return {
            "id": self.id,
            "size": self.size,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, moon_data):
        return cls(size=moon_data["size"], description=moon_data["description"])
