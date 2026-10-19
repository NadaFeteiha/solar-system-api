from app import create_app
from app.db import db
from app.models.Planet import Planet

my_app = create_app()
with my_app.app_context():
    planets = [
        Planet(name="Mercury", description="Smallest rocky planet, closest to the Sun", number_of_moons=0),
        Planet(name="Venus", description="Hot rocky planet with a thick toxic atmosphere", number_of_moons=0),
        Planet(name="Earth", description="Rocky planet with liquid water and life", number_of_moons=1),
        Planet(name="Mars", description="Red rocky planet with dusty deserts", number_of_moons=2),
        Planet(name="Jupiter", description="Largest gas giant with a great red spot", number_of_moons=95),
        Planet(name="Saturn", description="Gas giant famous for its bright rings", number_of_moons=146),
        Planet(name="Uranus", description="Ice giant that rotates on its side", number_of_moons=28),
        Planet(name="Neptune", description="Windy blue ice giant, farthest from the Sun", number_of_moons=16),
    ]

    db.session.add_all(planets)
    db.session.commit()
