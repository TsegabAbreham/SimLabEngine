import pygame
import random
import math

def wind(obj, dt, strength=0.1, direction=None):
    """
    Wind force rule that applies a force to the object's velocity based on its position.
    Mass is used as resistance, so larger masses have less acceleration.

    :param obj: The object to apply the wind force to.
    :param dt: Delta time to scale the force properly.
    :param strength: The strength of the wind force.
    :param direction: A tuple (x, y) that specifies the wind direction. 
                      If None, it generates a random direction.

    Example: box.add_rule(lambda obj, dt: wind(obj, dt, strength=100, direction=(1,1))) 
    """
    if direction is None:
        # Random wind direction with strength variations
        angle = random.uniform(0, 2 * math.pi)  # Random angle for gust
        wind_vector = pygame.Vector2(strength * math.cos(angle), strength * math.sin(angle))
    else:
        # Wind vector direction specified by (x, y)
        wind_vector = pygame.Vector2(direction[0], direction[1]) * strength

    # Use mass as resistance by dividing wind force by mass
    resistance_factor = 1 / obj.mass  # More mass = less effect from wind

    # Apply wind force to the object's velocity (scaled by resistance factor)
    obj.vel += wind_vector * resistance_factor * dt
