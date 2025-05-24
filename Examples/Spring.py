import sys
import os
import math
import pygame

# Ensure the library modules are in the path.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from RawSimLabEngine.engine.scene.scene import Scene
from RawSimLabEngine.engine.objects.box import Box
from RawSimLabEngine.engine.physics import velocity, collision
from SimLabUI.GUI import SimLabUI

pygame.init()

# Global spring parameters.
spring_k = 1      # Spring constant.
spring_rest = 50    # Rest length (in pixels).

# Custom spring rule (no gravity is applied).
def spring_rule(obj, dt):
    # Fixed anchor for the spring (e.g. scene center).
    anchor = (400, 300)
    dx = obj.pos[0] - anchor[0]
    dy = obj.pos[1] - anchor[1]
    dist = math.hypot(dx, dy)
    # Hooke's law: F = -k * (dist - rest)
    force = -spring_k * (dist - spring_rest)
    if dist != 0:
        fx = force * dx / dist
        fy = force * dy / dist
        obj.vel[0] += (fx / obj.mass) * dt
        obj.vel[1] += (fy / obj.mass) * dt

def main():
    # Create the simulation scene.
    scene = Scene(
        width=800,
        height=600,
        background_color=(240, 240, 240),
        title="Spring & Collision Demo"
    )
    scene.set_time_scale(1.0)
    
    # Create the UI system.
    ui = SimLabUI((800, 600))
    
    # Create the spring-attached object.
    # Gravity is set to 0 so only spring forces and collisions act.
    spring_obj = Box(
        pos=[300, 300], 
        vel=[0, 0], 
        size=(50, 50), 
        color=(0, 0, 255), 
        mass=5, 
        gravity=0, 
        bounciness=0
    )
    spring_obj.add_rule(velocity)   # Updates its position.
    spring_obj.add_rule(spring_rule)  # Applies the spring force pulling it toward the fixed anchor.
    
    # Create an object that will push the spring object.
    # This pusher has an initial velocity toward the spring object.
    pusher_obj = Box(
        pos=[500, 300], 
        vel=[-100, 0], 
        size=(50, 50), 
        color=(255, 0, 0), 
        mass=10, 
        gravity=0, 
        bounciness=0
    )
    pusher_obj.add_rule(velocity)
    
    # Add collision rules between the two objects.
    spring_obj.add_rule(collision(spring_obj, pusher_obj))
    pusher_obj.add_rule(collision(pusher_obj, spring_obj))
    
    # Add the objects to the scene.
    scene.add(spring_obj, pusher_obj)
    
    # Simulation update callback.
    def simulation_update(dt):
        # Update both objects.
        spring_obj.apply_rules(dt)
        spring_obj.update(dt)
        pusher_obj.apply_rules(dt)
        pusher_obj.update(dt)
        
        # Render the scene.
        scene.screen.fill(scene.background_color)
        spring_obj.draw(scene.screen, cam_offset=(0, 0))
        pusher_obj.draw(scene.screen, cam_offset=(0, 0))
    
    # Run the simulation with the UI overlay.
    ui.run(scene, simulation_update)

if __name__ == '__main__':
    main()