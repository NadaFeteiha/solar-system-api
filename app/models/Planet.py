
class Planet:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description


planets = [
    Planet(1, "Mercury", "Terrestrial"),
    Planet(2, "Venus", "Terrestrial"),
    Planet(3, "Earth", "Terrestrial"),
    Planet(4, "Mars", "Terrestrial"),
    Planet(5, "Jupiter", "Gas Giant"),
    Planet(6, "Saturn", "Gas Giant"),
    Planet(7, "Uranus", "Ice Giant"),
    Planet(8, "Neptune", "Ice Giant"),
]


# planets = [
#     {
#         "id": 1,
#         "name": "Mercury",
#         "description": "The smallest planet in our solar system.",
#     },
#     {"id": 2, "name": "Venus", "description": "The second planet from the Sun."},
#     {"id": 3, "name": "Earth", "description": "Our home planet."},
#     {"id": 4, "name": "Mars", "description": "The Red Planet."},
#     {
#         "id": 5,
#         "name": "Jupiter",
#         "description": "The largest planet in our solar system.",
#     },
#     {"id": 6, "name": "Saturn", "description": "Known for its beautiful rings."},
#     {"id": 7, "name": "Uranus", "description": "The ice giant with a unique tilt."},
#     {"id": 8, "name": "Neptune", "description": "The farthest planet from the Sun."},
# ]
