import math

def collisionhandlephysics(obj, other, dt, debug=False):
    """
    Resolves collision between two objects that are either:
      • circles (have .radius)
      • boxes (have .size = (width, height))
    Both must have: pos [x,y], vel [vx,vy], mass, bounciness.
    """
    # --- determine overlap & collision normal ---
    ax, ay = obj.pos
    bx, by = other.pos
    rvx = other.vel[0] - obj.vel[0]
    rvy = other.vel[1] - obj.vel[1]

    # Circle vs Circle
    if hasattr(obj, 'radius') and hasattr(other, 'radius'):
        dx, dy = bx - ax, by - ay
        dist = math.hypot(dx, dy)
        total_r = obj.radius + other.radius
        if dist == 0 or dist >= total_r:
            return
        # normal vector
        nx, ny = dx / dist, dy / dist
        overlap = total_r - dist

    # AABB vs AABB
    elif hasattr(obj, 'size') and hasattr(other, 'size'):
        w1, h1 = obj.size
        w2, h2 = other.size
        # half-extents
        hx1, hy1 = w1 / 2, h1 / 2
        hx2, hy2 = w2 / 2, h2 / 2
        dx = bx - ax
        dy = by - ay
        overlap_x = hx1 + hx2 - abs(dx)
        overlap_y = hy1 + hy2 - abs(dy)
        if overlap_x <= 0 or overlap_y <= 0:
            return
        # choose axis of least penetration
        if overlap_x < overlap_y:
            nx = 1 if dx > 0 else -1
            ny = 0
            overlap = overlap_x
        else:
            nx = 0
            ny = 1 if dy > 0 else -1
            overlap = overlap_y

    else:
        # unsupported shapes
        return

    # --- relative velocity along normal ---
    vel_norm = rvx * nx + rvy * ny
    if vel_norm > 0:
        return  # objects are moving apart

    # --- compute impulse scalar ---
    e = min(obj.bounciness, other.bounciness)
    inv_m1 = 0 if obj.mass == 0 else 1 / obj.mass
    inv_m2 = 0 if other.mass == 0 else 1 / other.mass
    inv_sum = inv_m1 + inv_m2
    if inv_sum == 0:
        return  # both objects immovable

    j = -(1 + e) * vel_norm / inv_sum
    ix, iy = j * nx, j * ny

    # --- apply impulse ---
    obj.vel[0] -= ix * inv_m1
    obj.vel[1] -= iy * inv_m1
    other.vel[0] += ix * inv_m2
    other.vel[1] += iy * inv_m2

    # --- positional correction ---
    percent = 0.2  # usually 0.2–0.8
    slop = 0.01
    correction = max(overlap - slop, 0) / inv_sum * percent
    corr_x = correction * nx
    corr_y = correction * ny

    obj.pos[0] -= corr_x * inv_m1
    obj.pos[1] -= corr_y * inv_m1
    other.pos[0] += corr_x * inv_m2
    other.pos[1] += corr_y * inv_m2

    threshold = 1
    for v in (obj.vel, other.vel):
        if abs(v[0]) < threshold:
            v[0] = 0
        if abs(v[1]) < threshold:
            v[1] = 0

    if debug:
        print(f"[C] {obj} ↔ {other} | impulse={j:.2f}, overlap={overlap:.2f}")
        print(f"    post-vel obj={obj.vel}, other={other.vel}")
        print(f"    correction=({corr_x:.2f},{corr_y:.2f})")


def collision(*targets):
    def collision_rule(self, dt):
        for other in targets:
            if other is not self and hasattr(other, "rect") and self.rect.colliderect(other.rect):
                collisionhandlephysics(self, other, dt)
    return collision_rule

