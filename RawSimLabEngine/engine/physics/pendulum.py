import math

def pendulum(obj, dt):
    """
    Simulates a more realistic pendulum step with:
      - damping
      - tension check (string slack)
      - tension computation
    """

    # Unpack parameters (with fallbacks)
    L       = getattr(obj, "pendulum_swing_length", 100)   # length
    theta   = getattr(obj, "angle", 0.0)                  # current angle (rad)
    omega   = getattr(obj, "angular_velocity")       # angular velocity (rad/s)
    m       = getattr(obj, "mass")                   # bob mass
    g       = getattr(obj, "gravity")               # gravity
    damping = getattr(obj, "damping_factor")               # small damping coefficient

    # 1) compute angular acceleration from gravity
    alpha = -(g / L) * math.sin(theta)

    # 2) update omega & theta
    omega += alpha * dt
    theta += omega * dt

    # 3) apply simple damping
    omega *= (1.0 - damping)

    # 4) compute instantaneous bob speed and tension
    #    v = L * omega
    v = L * omega
    #    T = m*(v^2/L + g*cos(theta))
    tension = m * (v*v / L + g * math.cos(theta))

    # 5) check for slack: if tension < 0, the bob is in free-fall
    if tension < 0:
        # temporarily treat it as a free-falling point mass
        # accelerate downward in world coords
        # convert polar to cartesian for acceleration:
        ax = -g * math.sin(theta) * math.cos(theta)  # approximate
        ay = -g * math.sin(theta) * math.sin(theta)  # approximate

        # you might instead choose to reset theta/omega once it falls back.
        # here, we’ll just zero tension and let it swing wildly:
        tension = 0 

    # 6) store back into the object
    obj.angle            = theta
    obj.angular_velocity = omega
    obj.tension          = tension

    # 7) compute pos for rendering
    if hasattr(obj, "swing_anchor"):
        x0, y0 = obj.swing_anchor
        obj.pos[0] = x0 + L * math.sin(theta)
        obj.pos[1] = y0 + L * math.cos(theta)
