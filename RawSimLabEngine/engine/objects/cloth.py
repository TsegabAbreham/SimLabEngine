import pygame
import math



"""
To Add physics to the cloth, you can use the following code snippet:
cloth.colliders.append(target[0])  # Add the projectile as a collider
cloth.add_rule(clothsimualtion)
"""


class Particle:
    def __init__(self, pos, pinned=False):
        self.pos = pygame.Vector2(pos)
        self.prev = pygame.Vector2(pos)
        self.acc = pygame.Vector2(0, 0)
        self.pinned = pinned

    def apply_force(self, force):
        self.acc += force

    def verlet(self, dt):
        if self.pinned:
            return
        temp = self.pos.copy()
        self.pos += (self.pos - self.prev) + self.acc * (dt * dt)
        self.prev = temp
        self.acc.update(0, 0)

class Constraint:
    def __init__(self, a, b, rest_length):
        self.a = a
        self.b = b
        self.rest = rest_length

    def satisfy(self):
        delta = self.b.pos - self.a.pos
        dist = delta.length()
        if dist == 0:
            return
        diff = (dist - self.rest) / dist * 0.5
        offset = delta * diff
        if not self.a.pinned:
            self.a.pos += offset
        if not self.b.pinned:
            self.b.pos -= offset

class Cloth:
    def __init__(self, rows, cols, spacing, vel=(0,0), pos=(0,0), gravity=9.8, mass=1, pin_top=False):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.gravity = gravity
        self.mass = mass
        self.pin_top = pin_top

        self.spacing = spacing
        self.particles = []
        self.constraints = []
        self.rules = []

        self.colliders = []
        self.constraint_iterations = 5

        self.rect = pygame.Rect(pos[0], pos[1], cols*spacing, rows*spacing)

        # build grid of particles relative to cloth.pos
        for y in range(rows):
            for x in range(cols):
                world_pos = self.pos + pygame.Vector2(x * spacing, y * spacing)
                pinned = (y == 0 and self.pin_top)
                p = Particle(world_pos, pinned)
                p.prev -= self.vel
                self.particles.append(p)

        # structural constraints
        for y in range(rows):
            for x in range(cols):
                idx = y * cols + x
                if x < cols - 1:
                    self.constraints.append(
                        Constraint(self.particles[idx], self.particles[idx + 1], spacing)
                    )
                if y < rows - 1:
                    self.constraints.append(
                        Constraint(self.particles[idx], self.particles[idx + cols], spacing)
                    )

    def add_rule(self, rule):
        self.rules.append(rule)

    def apply_rules(self, dt):
        for rule in self.rules:
            rule(self, dt)

    def update(self, dt):
        # apply optional cloth movement
        self.vel.y += self.gravity * self.mass * dt
        self.pos += self.vel * dt

        # apply global gravity & verlet
        gravity_force = pygame.Vector2(0, self.gravity * self.mass)
        for p in self.particles:
            p.apply_force(gravity_force)
        for p in self.particles:
            p.verlet(dt)

        # satisfy constraints
        for _ in range(self.constraint_iterations):
            for c in self.constraints:
                c.satisfy()

        # run any additional rules
        self.apply_rules(dt)

    def draw(self, screen, cam_offset=(0, 0)):
        for c in self.constraints:
            a = c.a.pos - pygame.Vector2(cam_offset)
            b = c.b.pos - pygame.Vector2(cam_offset)
            pygame.draw.line(screen, (255, 255, 255), a, b, 1)
        for p in self.particles:
            pos = p.pos - pygame.Vector2(cam_offset)
            if p.pinned:
                color = (255, 100, 100)  # red for pinned
            else:
                color = (200, 100, 255)
            pygame.draw.circle(screen, color, (int(pos.x), int(pos.y)), 3)