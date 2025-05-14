import pygame

class Box:
    def __init__(self, pos, vel, size=(10,10), color=(200, 100, 255), mass=1, gravity=9.8 , damping_factor=0.9, friction_coefficient=0.2):
        self.pos = list(pos)
        self.vel = list(vel)
        self.size = list(size)
        self.color = color
        self.mass = mass
        self.gravity = gravity
        self.damping_factor = damping_factor
        self.friction_coefficient = friction_coefficient
        self.rules = []  # List to hold object-specific rules

        # Initialize rect once
        self.rect = pygame.Rect(int(self.pos[0]), int(self.pos[1]), size[0], size[1])
        self.scene = None  # Will be set when added to scene

    def add_rule(self, rule):
        """Add a specific rule (behavior) to the object."""
        self.rules.append(rule)

    def apply_rules(self, dt):
        """Apply all rules (behaviors) to the object."""
        for rule in self.rules:
            rule(self, dt)  # Apply each rule to this object

    def update(self, dt):
        """Update object properties, apply rules, and sync rect."""
        self.apply_rules(dt)  # Apply object-specific rules
        self.rect.topleft = (int(self.pos[0]), int(self.pos[1]))  # Update the rect position

    def draw(self, screen, cam_offset=(0, 0)):
        """Draw the object on the screen, taking camera offset into account."""
        offset_x = self.pos[0] - cam_offset[0]
        offset_y = self.pos[1] - cam_offset[1]
        pygame.draw.rect(screen, self.color, pygame.Rect(offset_x, offset_y, self.size[0], self.size[1]))
