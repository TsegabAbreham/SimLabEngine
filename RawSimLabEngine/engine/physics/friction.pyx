def friction(obj, dt):
    if hasattr(obj, 'friction_coefficient') and hasattr(obj, 'vel'):

        normal_force = obj.mass * obj.gravity

        mult = max(0, 1 - obj.friction_coefficient * obj.mass * obj.gravity * dt)
        obj.vel[0] *= mult
        obj.vel[1] *= mult

