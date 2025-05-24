import pygame

def clothsimualtion(obj, dt):
     # 1) apply gravity as force + Verlet integration
    gravity_force = pygame.Vector2(0, obj.gravity * obj.mass)
    for p in obj.particles:
        if not p.pinned:
            p.apply_force(gravity_force)
            p.verlet(dt)

    # 2) collisions: circles or AABBs
    for p in obj.particles:
        if p.pinned or not hasattr(obj, 'colliders'):
            continue
        for col in obj.colliders:
            # --- Circle collider ---
            if hasattr(col, 'radius'):
                delta = p.pos - col.pos
                dist = delta.length()
                if dist < col.radius:
                    n = delta.normalize()
                    p.pos = col.pos + n * col.radius
                    vel = p.pos - p.prev
                    damping = getattr(col, 'damping', 0.8)
                    p.prev = p.pos - vel.reflect(n) * damping

            # --- Box collider (axis‑aligned) ---
            elif hasattr(col, 'size'):
                # compute particle inside box?
                half = pygame.Vector2(col.size) * 0.5
                box_min = col.pos - half
                box_max = col.pos + half
                # if inside AABB
                if (box_min.x < p.pos.x < box_max.x and
                    box_min.y < p.pos.y < box_max.y):
                    # find nearest face
                    # distances to each side
                    dx_min = abs(p.pos.x - box_min.x)
                    dx_max = abs(box_max.x - p.pos.x)
                    dy_min = abs(p.pos.y - box_min.y)
                    dy_max = abs(box_max.y - p.pos.y)
                    # pick smallest
                    min_dist = min(dx_min, dx_max, dy_min, dy_max)
                    if min_dist == dx_min:
                        p.pos.x = box_min.x
                        normal = pygame.Vector2(-1, 0)
                    elif min_dist == dx_max:
                        p.pos.x = box_max.x
                        normal = pygame.Vector2(1, 0)
                    elif min_dist == dy_min:
                        p.pos.y = box_min.y
                        normal = pygame.Vector2(0, -1)
                    else:
                        p.pos.y = box_max.y
                        normal = pygame.Vector2(0, 1)
                    # bounce
                    vel = p.pos - p.prev
                    damping = getattr(col, 'damping', 0.8)
                    refl = vel.reflect(normal) * damping
                    p.prev = p.pos - refl

    # 3) satisfy structural constraints
    iterations = getattr(obj, 'constraint_iterations', 5)
    for _ in range(iterations):
        for c in obj.constraints:
            c.satisfy()