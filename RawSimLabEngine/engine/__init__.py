# Expose core objects
# Expose core objects
from .scene.scene import Scene
from .scene.buildvideo import build_as_video


from .objects import Box, Circle, Image, Text, BoundingBox, Cloth
# Expose physics rules
from .physics import gravity, friction, velocity, collision, wind, clothsimualtion, spring, planetphysics, pendulum

# Make them accessible with 'from SimLabEngine import *'
__all__ = [
    "Scene", "build_as_video",
    "Box", "Circle", "Image", "Text", "BoundingBox", "Cloth",
    "gravity", "friction", "velocity", "collision", "wind", "clothsimualtion", "spring", "planetphysics", "pendulum"
]