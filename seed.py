from app import create_app
from app.db import db
from app.models.Planet import Planet
from app.models.Moon import Moon

my_app = create_app()
with my_app.app_context():

    db.session.execute(db.text("TRUNCATE TABLE moon, planet RESTART IDENTITY CASCADE"))

    planets = [
        Planet(name="Mercury", description="Smallest rocky planet, closest to the Sun", number_of_moons=0),
        Planet(name="Venus", description="Hot rocky planet with a thick toxic atmosphere", number_of_moons=0),
        Planet(
            name="Earth",
            description="Rocky planet with liquid water and life",
            number_of_moons=1,
            moons=[
                Moon(size="3,474 km", description="The Moon, Earth's only natural satellite", discovered_year=None),
            ],
        ),
        Planet(
            name="Mars",
            description="Red rocky planet with dusty deserts",
            number_of_moons=2,
            moons=[
                Moon(size="22 km", description="Phobos, the larger and closer moon of Mars", discovered_year=1877),
                Moon(size="12 km", description="Deimos, the smaller and farther moon of Mars", discovered_year=1877),
            ],
        ),
        Planet(
            name="Jupiter",
            description="Largest gas giant with a great red spot",
            number_of_moons=95,
            moons=[
                Moon(size="3,643 km", description="Io, the most volcanic body in the solar system", discovered_year=1610),
                Moon(size="3,122 km", description="Europa, an icy moon with an ocean under its surface", discovered_year=1610),
                Moon(size="5,268 km", description="Ganymede, the largest moon in the solar system", discovered_year=1610),
                Moon(size="4,821 km", description="Callisto, a heavily cratered icy moon", discovered_year=1610),
            ],
        ),
        Planet(
            name="Saturn",
            description="Gas giant famous for its bright rings",
            number_of_moons=146,
            moons=[
                Moon(size="5,150 km", description="Titan, a moon with a thick atmosphere and methane lakes", discovered_year=1655),
                Moon(size="1,527 km", description="Rhea, Saturn's second largest moon", discovered_year=1672),
                Moon(size="504 km", description="Enceladus, an icy moon with water geysers", discovered_year=1789),
            ],
        ),
        Planet(
            name="Uranus",
            description="Ice giant that rotates on its side",
            number_of_moons=28,
            moons=[
                Moon(size="1,578 km", description="Titania, the largest moon of Uranus", discovered_year=1787),
                Moon(size="1,523 km", description="Oberon, the outermost major moon of Uranus", discovered_year=1787),
                Moon(size="472 km", description="Miranda, a small moon with huge cliffs", discovered_year=1948),
            ],
        ),
        Planet(
            name="Neptune",
            description="Windy blue ice giant, farthest from the Sun",
            number_of_moons=16,
            moons=[
                Moon(size="2,707 km", description="Triton, a moon that orbits backwards", discovered_year=1846),
            ],
        ),
    ]

    db.session.add_all(planets)
    db.session.commit()
