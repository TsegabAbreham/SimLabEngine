def velocity(obj, dt):
    if hasattr(obj, 'vel'):  # Check if the object has gravity
        obj.pos[0] += obj.vel[0] * dt
        obj.pos[1] += obj.vel[1] * dt
        obj.vel[1] += obj.gravity * dt
