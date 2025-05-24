import sys
import os
import math
import pygame

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from RawSimLabEngine.engine.scene.scene import Scene
from RawSimLabEngine.engine.objects.box import Box
from RawSimLabEngine.engine import *
from SimLabUI.GUI import SimLabUI

pygame.init()

# A custom rule to simulate constant acceleration (e.g., gravity-like acceleration).
def acceleration_rule(obj, dt):
    # Constant acceleration downward (200 pixels/s^2)
    acceleration = 200  
    obj.vel[1] += acceleration * dt
    # Update the object's position using its velocity.
    obj.pos[0] += obj.vel[0] * dt
    obj.pos[1] += obj.vel[1] * dt

def main():
    # Create the simulation scene.
    scene = Scene(
        width=800,
        height=600,
        background_color=(255, 255, 255),
        title="Kinematics: Velocity vs Time"
    )
    scene.set_time_scale(1.0)
    
    # Create the UI system.
    ui = SimLabUI((800, 600))
    
    # Create an object (Box) that moves under constant acceleration.
    # Gravity is disabled in the object's parameters because our rule applies acceleration.
    box = Box(pos=[100, 100], vel=[0, 0], size=(30, 30), color=(0, 0, 255), mass=1, gravity=9.8, bounciness=0.5)
    ground = Box(pos=[0, 580], vel=[0, 0], size=(800, 20), color=(0, 255, 0), mass=1000000, gravity=0, bounciness=0.5)
    box.add_rule(velocity)
    box.add_rule(gravity)  

    ground.add_rule(collision(ground, box))
    box.add_rule(collision(box, ground))
    scene.add(box, ground)
    
    # Add a realtime graph to visualize the object's velocity magnitude.
    # The graph is placed at the bottom of the window.
    graph = ui.add_realtime_graph("velocity_graph", pygame.Rect(10, 100, 780, 70),
                                  max_points=200, background_color=(230, 230, 230), line_color=(255, 0, 0))
    
    # Simulation time accumulator.
    sim_time = 0
    
    def simulation_update(dt):
        nonlocal sim_time
        sim_time += dt
        
        # Update physics.
        box.apply_rules(dt)
        box.update(dt)
        
        # Calculate the instantaneous velocity magnitude.
        vel_magnitude = math.hypot(box.vel[0], box.vel[1])
        
        # Feed the velocity magnitude value into the realtime graph.
        graph.add_data(vel_magnitude)
        
        # Draw the scene.
        scene.screen.fill(scene.background_color)
        box.draw(scene.screen, cam_offset=(0, 0))
    
    # Start the simulation with UI overlay.
    ui.run(scene, simulation_update)

if __name__ == '__main__':
    main()