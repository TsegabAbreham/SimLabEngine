def gravity(obj, dt):
    if hasattr(obj, 'gravity'):
        obj.vel[1] += obj.gravity * obj.mass * dt