def gravity(obj, dt):
    if hasattr(obj, 'gravity'):  # Check if the object has gravity
        obj.vel[1] += obj.gravity * obj.mass * dt  # Apply gravity to vertical velocity
    return obj.vel