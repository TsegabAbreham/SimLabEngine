import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from RawSimLabEngine.engine import *
import pygame

scene = Scene(
    width=800,
    height=600,
    background_color=(0, 0, 0),
    title="Cloth Simulation"
)

box =  Box(
    pos=(100, 400),
    size=(100, 20),
    vel=(0, 0),
    color=(255, 0, 0),
    mass=1,
    gravity=0,
    bounciness=0.1
)



box1 =  Box(
    pos=(300, 400),
    size=(100, 100),
    vel=(0, 0),
    color=(255, 0, 0),
    mass=1,
    gravity=0,
    bounciness=0.1
)

box1.add_rule(collision(box1, box))
box.add_rule(collision(box, box1))

box1.add_rule(velocity)
box1.add_rule(gravity)
box.add_rule(gravity)
box1.add_rule(velocity)

box.add_rule(velocity)

def handle_keys(event):
    keys = pygame.key.get_pressed()
    vel_x = 0
    vel_y = 0
    angle = 0
    speed = 100

    if keys[pygame.K_w]:
        vel_y -= speed
    if keys[pygame.K_s]:
        vel_y += speed
    if keys[pygame.K_a]:
        vel_x -= speed
    if keys[pygame.K_d]:
        vel_x += speed
    if keys[pygame.K_r]:
        angle += 10

    box.vel[0] = vel_x
    box.vel[1] = vel_y
    box.rotate(angle)

            
scene.add(box, box1)

scene.simulate(duration=10, fps=60, on_event=handle_keys)