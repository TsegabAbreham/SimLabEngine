import pygame
import math

class Box:
    def __init__(self, pos=(0,0), vel=(0,0), size=(10,10), color=(200, 100, 255), rotation=0, mass=1, gravity=9.8, damping_factor=0.9, friction_coefficient=0.2, bounciness=0,
                 spring_k=0.1, spring_rest=100, spring_anchor_y=0, angular_velocity=0, swing_anchor=(0,0), pendulum_swing_length=0):
        # Keep Box original style with lists for pos/vel
        self.pos = list(pos)
        self.vel = list(vel)
        self.size = list(size)
        self.color = color
        self.angle = rotation
        self.mass = mass
        self.gravity = gravity * 10  # Same as original Box gravity scaling
        self.damping_factor = damping_factor
        self.friction_coefficient = friction_coefficient
        self.bounciness = bounciness

        # Box-specific physics properties
        self.spring_k = spring_k
        self.spring_rest = spring_rest
        self.spring_anchor_y = spring_anchor_y  
        self.angular_velocity = angular_velocity
        self.swing_anchor = list(swing_anchor)
        self.pendulum_swing_length = pendulum_swing_length

        # From Circle: add trail features (optional, disabled by default)
        self.trail = []
        self.trail_enabled = False

        self.rules = []  # Object-specific rules

        # Rect for collision/drawing
        self.rect = pygame.Rect(int(self.pos[0]), int(self.pos[1]), size[0], size[1])
        self.scene = None

    def add_rule(self, rule):
        self.rules.append(rule)

    def apply_rules(self, dt):
        for rule in self.rules:
            rule(self, dt)

    def add_trail(self, max_length=100):
        if self.trail_enabled:
            self.trail.append(self.pos[:])  # Copy list of position
            if len(self.trail) > max_length:
                self.trail.pop(0)

    def draw_trail(self, screen, cam_offset=(0, 0), color=(200, 200, 255), radius=2):
        for point in self.trail:
            x = int(point[0] - cam_offset[0])
            y = int(point[1] - cam_offset[1])
            pygame.draw.circle(screen, color, (x, y), radius)

    def update(self, dt):
        self.apply_rules(dt)
        self.add_trail()
        self.rect.topleft = (int(self.pos[0]), int(self.pos[1]))

    def rotate(self, angle_delta):
        self.angle = (self.angle + angle_delta) % 360

    def draw(self, screen, cam_offset=(0, 0)):
        offset_x = self.pos[0] - cam_offset[0]
        offset_y = self.pos[1] - cam_offset[1]

        self.draw_trail(screen, cam_offset)  # Draw trail if enabled

        rect = pygame.Rect(0, 0, self.size[0], self.size[1])
        surface = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        pygame.draw.rect(surface, self.color, rect)
        rotated_surface = pygame.transform.rotate(surface, self.angle)
        rotated_rect = rotated_surface.get_rect(center=(offset_x + self.size[0] // 2, offset_y + self.size[1] // 2))
        screen.blit(rotated_surface, rotated_rect)