import pygame
from ..physics import *
from ..scene.scene import Scene
from ..objects import *

class Image:
    def __init__(self, path, pos, vel, mass=1, gravity=9.8, damping_factor=0.99, friction_coefficient = 0.2):
        self.path = path
        self.pos = list(pos)
        self.vel = list(vel)
        self.mass = mass
        self.gravity = gravity
        self.damping_factor = damping_factor
        self.friction_coefficient = friction_coefficient
        self.rules = []  # List to hold object-specific rules

        # Load the image and get its dimensions
        self.image = pygame.image.load(path).convert_alpha()
        self.width, self.height = self.image.get_width(), self.image.get_height()

        # Initialize rect based on the image size for collision handling
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.scene = None  # Will be set when added to the scene

    def add_rule(self, rule):
        """Add a specific rule (behavior) to the object."""
        self.rules.append(rule)

    def apply_rules(self, dt):
        """Apply all rules (behaviors) to the object."""
        for rule in self.rules:
            rule(self, dt)  # Apply each rule to this object

    def update(self, dt):
        """Update object properties, apply rules, and sync rect."""
        self.vel[1] += self.gravity * dt  # Apply gravity to the vertical velocity (y-component)
        self.pos[0] += self.vel[0] * dt  # Update horizontal position
        self.pos[1] += self.vel[1] * dt  # Update vertical position

        self.apply_rules(dt)  # Apply object-specific rules
        self.rect.topleft = (self.pos[0], self.pos[1])  # Update the rect position

    def draw(self, screen, cam_offset=(0, 0)):
        """Draw the object (image) on the screen, considering camera offset."""
        offset_x = self.pos[0] - cam_offset[0]
        offset_y = self.pos[1] - cam_offset[1]
        screen.blit(self.image, (int(offset_x), int(offset_y)))  # Draw the image without scaling