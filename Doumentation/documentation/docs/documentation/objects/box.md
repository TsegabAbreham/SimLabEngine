# Box and Circle

The `Box` and `Circle` class represents a 2D physics-enabled objects for SimLabEngine.  
It supports position, velocity, rotation, custom physics rules, trails, and spring/pendulum physics.

---

### Initialization

Creates a new instance with the following parameters:

For a Box:

    box = Box(self, pos=(0,0), vel=(0,0), size=(10,10), color=(200, 100, 255), rotation=0, mass=1, gravity=9.8, damping_factor=0.9, friction_coefficient=0.2, bounciness=0,
                 spring_k=0.1, spring_rest=100, spring_anchor_y=0, angular_velocity=0, swing_anchor=(0,0), pendulum_swing_length=0):

For a Circle:

    circle = Circle(self, pos=(0,0), vel=(0,0), radius=10, color=(200, 100, 255), rotation=0, mass=1, gravity=9.8, damping_factor=0.9, friction_coefficient=0.2, bounciness=0,
                 spring_k=0.1, spring_rest=100, spring_anchor_y=0, angular_velocity=0, swing_anchor=(0,0), pendulum_swing_length=0):


- **pos** (tuple): Initial position `[x, y]`.
- **vel** (tuple): Initial velocity `[vx, vy]`.
- **size** (tuple): Width and height of the box. Default `(10, 10)`. (For Boxes only)
- **radius**(float): The Radius of the circle. (For Circles only)
- **color** (tuple): RGB color for rendering. Default `(200, 100, 255)`.
- **rotation** (float): Initial rotation angle in degrees. Default `0`.
- **mass** (float): Mass of the box. Default `1`.
- **gravity** (float): Gravity acceleration, internally multiplied by 10. Default `9.8`.
- **damping_factor** (float): Velocity damping factor. Default `0.9`.
- **friction_coefficient** (float): Friction coefficient. Default `0.2`.
- **bounciness** (float): Elasticity of collisions. Default `0`.
- **spring_k** (float): Spring constant for spring physics. Default `0.1`.
- **spring_rest** (float): Rest length of spring. Default `100`.
- **spring_anchor_y** (float): Y coordinate of spring anchor. Default `0`.
- **angular_velocity** (float): Initial angular velocity (degrees per second). Default `0`.
- **swing_anchor** (tuple): Anchor point for pendulum swing. Default `(0, 0)`.
- **pendulum_swing_length** (float): Length of pendulum swing. Default `0`.

Note: not everything shall be used, use only needed and required. 

---


### Physics

Allows adding a custom function that applies additional physics behavior to the box.

Example:

    box.add_rule(rule)

- **Input:** A function that takes a physics rule function as argument.

---

### Trails

If trail drawing is enabled, appends the current position to the trail list.

Example:

    box.add_trail(max_length)

- **Parameter:** Maximum length of the trail before it starts to fade.

Note: if you want to enable trail add:
    
    box.trail_enabled = True

---


### Rotation

Changes the rotation angle of the box by a given amount.

Example:

    box.rotate(angle)


- **Parameter:** `angle` — rotation amount in degrees.
- Keeps rotation normalized between 0 and 360 degrees.


