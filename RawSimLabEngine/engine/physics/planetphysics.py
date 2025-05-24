import math


def planetphysicshandler(obj1, obj2, dt):
    """
    Applies mutual Newtonian gravity between obj1 and obj2.

    Assumes each object has:
    - pos: a sequence [x, y] in meters
    - vel: a sequence [vx, vy] in meters/second
    - mass: in kilograms
    """

    G=1
    # Vector from obj1 to obj2
    dx = obj2.pos[0] - obj1.pos[0]
    dy = obj2.pos[1] - obj1.pos[1]
    # Squared distance (add small epsilon to avoid div-by-zero)
    dist_sq = dx*dx + dy*dy + 1e-10
    # Distance
    dist = math.sqrt(dist_sq)

    # Magnitude of the gravitational force
    force_mag = G * obj1.mass * obj2.mass / dist_sq

    # Direction unit vector from obj1 to obj2
    ux = dx / dist
    uy = dy / dist

    # Force components
    fx = force_mag * ux
    fy = force_mag * uy

    # Acceleration on each object: a = F / m
    ax1 = fx / obj1.mass
    ay1 = fy / obj1.mass
    ax2 = -fx / obj2.mass
    ay2 = -fy / obj2.mass

    # Update velocities: v += a * dt
    obj1.vel[0] += ax1 * dt
    obj1.vel[1] += ay1 * dt
    obj2.vel[0] += ax2 * dt
    obj2.vel[1] += ay2 * dt


def planetphysics(*targets):
    def planet_rule(self, dt):
        for other in targets:
            if other is not self:
                planetphysicshandler(self, other, dt)
    return planet_rule

