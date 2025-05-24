import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from RawSimLabEngine.engine import *
import math

G = 1  # Scaled gravitational constant for visual simulation

scene = Scene(1920, 1080, (0, 0, 0), "Simulated Solar System")

# Central star (Sun)
sun = Circle((960, 540), (0, -200), 50, mass=1e9, gravity=0, bounciness=0)
scene.add(sun)

# Planets data: (distance from sun, radius, mass, color)
planet_data = [
    (150, 10, 1e6, (200, 100, 255)),  # Mercury-like
    (250, 12, 2e6, (100, 200, 255)),  # Venus-like
    (350, 14, 3e6, (50, 255, 50)),    # Earth-like
    (450, 10, 1e6, (255, 100, 100)),  # Mars-like
]


# Function to create planet with orbital velocity
def create_orbiting_planet(distance, radius, mass, color):
    angle = 0  # Could be randomized for spread
    x = sun.pos[0] + math.cos(angle) * distance
    y = sun.pos[1] + math.sin(angle) * distance

    # Orbital speed for circular orbit: v = sqrt(GM / r)
    v = math.sqrt(G * sun.mass / distance)

    # Velocity vector perpendicular to radius vector
    vx = -math.sin(angle) * v
    vy = math.cos(angle) * v

    planet = Circle((x, y), (vx, vy), radius, mass=mass, gravity=0, bounciness=0, color=color)
    planet.add_rule(planetphysics(sun, planet))  # Attracted to sun
    planet.add_rule(velocity)
    return planet

# Create and add planets
for dist, radius, mass, color in planet_data:
    planet = create_orbiting_planet(dist, radius, mass, color)
    planet.trail_enabled = True
    scene.add(planet)

sun.add_rule(velocity)  # Optional, in case sun reacts

scene.set_time_scale(0.1)  # Slow motion for better visualization

scene.simulate(30, fps=60)
