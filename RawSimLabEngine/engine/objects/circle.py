import pygame

class Circle:
    def __init__(self, pos, vel, radius, color=(200, 100, 255), mass=1, gravity=9.8, damping_factor=0.9, friction_coefficient=0.2):
        self.pos = pygame.Vector2(pos)  # Position as Vector2
        self.vel = pygame.Vector2(vel)  # Velocity as Vector2
        self.radius = radius
        self.color = color
        self.mass = mass
        self.gravity = gravity
        self.damping_factor = damping_factor
        self.friction_coefficient = friction_coefficient
        self.rules = []  # List to hold object-specific rules

        # Initialize a rect for collision handling (using radius for width and height)
        self.rect = pygame.Rect(self.pos.x - radius, self.pos.y - radius, radius * 2, radius * 2)
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
        self.apply_rules(dt)  # Apply object-specific rules
        self.rect.topleft = (self.pos.x - self.radius, self.pos.y - self.radius)  # Update rect to match position

    def draw(self, screen, cam_offset=(0, 0)):
        """Draw the object on the screen, considering camera offset."""
        offset_x = self.pos.x - cam_offset[0]
        offset_y = self.pos.y - cam_offset[1]
        pygame.draw.circle(screen, self.color, (int(offset_x), int(offset_y)), self.radius)
