import pygame
import math

class Circle:
    def __init__(self, pos, vel, radius, color=(200, 100, 255), rotation=0, mass=1, gravity=9.8, bounciness=0,
                 damping_factor=0.9, friction_coefficient=0.2,
                 spring_k=0.1, spring_rest=100, spring_anchor_y=0,
                 angular_velocity=0, swing_anchor=(0,0), pendulum_swing_length=0):
        # Keep Circle using pygame.Vector2 for pos/vel
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.radius = radius
        self.color = color
        self.mass = mass
        self.gravity = gravity * 10  # Matching Box scaling for consistency
        self.bounciness = bounciness
        self.damping_factor = damping_factor
        self.friction_coefficient = friction_coefficient

        # Box features added to Circle:
        self.spring_k = spring_k
        self.spring_rest = spring_rest
        self.spring_anchor_y = spring_anchor_y
        self.angular_velocity = angular_velocity
        self.swing_anchor = pygame.Vector2(swing_anchor)
        self.pendulum_swing_length = pendulum_swing_length

        self.angle = rotation
        self.rules = []
        self.trail = []
        self.trail_enabled = False

        self.rect = pygame.Rect(self.pos.x - radius, self.pos.y - radius, radius * 2, radius * 2)
        self.scene = None

    def add_trail(self, max_length=100):
        if self.trail_enabled:
            self.trail.append(self.pos.copy())
            if len(self.trail) > max_length:
                self.trail.pop(0)

    def draw_trail(self, screen, cam_offset=(0, 0), color=(200, 200, 255), radius=2):
        for point in self.trail:
            x = int(point.x - cam_offset[0])
            y = int(point.y - cam_offset[1])
            pygame.draw.circle(screen, color, (x, y), radius)

    def add_rule(self, rule):
        self.rules.append(rule)

    def apply_rules(self, dt):
        for rule in self.rules:
            rule(self, dt)

    def update(self, dt):
        self.apply_rules(dt)
        self.add_trail()
        self.rect.topleft = (self.pos.x - self.radius, self.pos.y - self.radius)

    def rotate(self, angle_delta):
        self.angle = (self.angle + angle_delta) % 360

    def draw(self, screen, cam_offset=(0, 0)):
        offset_x = self.pos.x - cam_offset[0]
        offset_y = self.pos.y - cam_offset[1]

        self.draw_trail(screen, cam_offset)

        diameter = self.radius * 2
        temp = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        pygame.draw.circle(temp, self.color, (self.radius, self.radius), self.radius)
        pygame.draw.line(temp, (0, 0, 0), (self.radius, self.radius), (self.radius, 0), 2)

        rotated = pygame.transform.rotate(temp, self.angle)
        rect = rotated.get_rect(center=(offset_x, offset_y))
        screen.blit(rotated, rect)