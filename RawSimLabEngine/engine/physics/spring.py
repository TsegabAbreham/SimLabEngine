import math

def spring(obj, dt):
    # Fixed anchor directly above the object
    anchor_y = getattr(obj, "spring_anchor_y", obj.pos[1])  # fallback to current y

    # Distance from anchor to object
    dy = obj.pos[1] - anchor_y
    dist = abs(dy)

    # Spring force: F = -k (x - x_rest)
    spring_k = getattr(obj, "spring_k", 0.3)
    spring_rest = getattr(obj, "spring_rest", 100)
    force = -spring_k * (dist - spring_rest)

    # Direction of force (only vertical here)
    if dy != 0:
        direction = dy / dist
        fy = force * direction
    else:
        fy = 0

    # Apply force to velocity (F = ma => a = F/m)
    obj.vel[1] += fy / obj.mass * dt

    # Move the object
    obj.pos[1] += obj.vel[1] * dt
