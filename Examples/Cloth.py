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

cloth = Cloth(
    rows=20,
    cols=20,
    spacing=5,
    vel=[0, 0],
    pos=(400, 300),
    gravity=9.8,
    mass=1,
    pin_top=True
)

box =  Box(
    pos=(100, 400),
    size=(100, 20),
    vel=(50, 0),
    color=(255, 0, 0),
    mass=1,
    gravity=0,
)

def handle_event(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_e:
            box.add_rule(velocity)
            box.add_rule(gravity)



cloth.add_rule(gravity)
cloth.add_rule(velocity)

cloth.colliders.append(box)  # Add the projectile as a collider
cloth.add_rule(clothsimualtion)

scene.add(cloth, box)


scene.simulate(duration=10, fps=60, on_event=handle_event)