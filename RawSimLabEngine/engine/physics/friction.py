def friction(obj, dt):
    # requires: obj.mass, obj.gravity, obj.friction_coefficient, obj.vel (2-component list)
    if not (hasattr(obj, 'mass') and hasattr(obj, 'gravity')
            and hasattr(obj, 'friction_coefficient') and hasattr(obj, 'vel')):
        return

    v_x = obj.vel[0]
    if v_x == 0:
        return

    # normal force = m·g
    N = obj.mass * obj.gravity
    # friction force magnitude = μ·N
    F_fric = obj.friction_coefficient * N
    # friction acceleration = F_fric / m, opposing motion
    a_fric = F_fric / obj.mass * (-1 if v_x > 0 else 1)

    # change in velocity over dt
    dv = a_fric * dt

    # don’t overshoot past zero
    if abs(dv) > abs(v_x):
        obj.vel[0] = 0
    else:
        obj.vel[0] += dv
