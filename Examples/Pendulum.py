import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import math
from RawSimLabEngine.engine import *

scene = Scene(width=800,height=600,title= "Pendulum Simulation", background_color=(255, 255, 255))

box = Box(pos=(400, 300), vel=(0, 0), size=(10, 10), color=(200, 100, 255), mass=5, 
          gravity=9.8, angular_velocity=1, swing_anchor=(400,300), pendulum_swing_length=100, rotation=0, damping_factor=0.01)

circle = Box(pos=(200, 400), vel=(70, 0), size=(70,70) , color=(255, 100, 100), mass=1, gravity=9.8)

box.add_rule(pendulum)
box.add_rule(gravity)
box.add_rule(velocity)

box.add_rule(collision(circle))
circle.add_rule(collision(box))

circle.add_rule(gravity)
circle.add_rule(velocity)

scene.add(box)
scene.simulate(math.inf, fps=60)
