import math

def collision(obj, dt):
    if not obj.scene:
        raise AttributeError("The object is not part of a scene.")

    for other in obj.scene.objects:
        if obj != other and obj.rect.colliderect(other.rect):
            if id(obj) > id(other):
                continue

            m1 = obj.mass
            m2 = other.mass
            v1x, v1y = obj.vel
            v2x, v2y = other.vel

            # Handle infinite mass (immovable object)
            if math.isinf(m1) and math.isinf(m2):
                # Both immovable, do nothing
                continue
            elif math.isinf(m1):
                # Obj is immovable
                other.vel[0] = -v2x * other.damping_factor
                other.vel[1] = -v2y * other.damping_factor
            elif math.isinf(m2):
                # Other is immovable
                if abs(v1y) > 0.1:  # Only bounce if impact is strong enough
                    obj.vel[1] = -v1y * obj.damping_factor
                else:
                    obj.vel[1] = 0  # Stop bouncing
            else:
                # Normal collision
                if m1 + m2 != 0:
                    obj.vel[0] = ((m1 - m2) / (m1 + m2)) * v1x + ((2 * m2) / (m1 + m2)) * v2x
                    obj.vel[1] = ((m1 - m2) / (m1 + m2)) * v1y + ((2 * m2) / (m1 + m2)) * v2y

                    other.vel[0] = ((m2 - m1) / (m1 + m2)) * v2x + ((2 * m1) / (m1 + m2)) * v1x
                    other.vel[1] = ((m2 - m1) / (m1 + m2)) * v2y + ((2 * m1) / (m1 + m2)) * v1y

            # Collision resolution (prevent overlap)
            dx = (obj.rect.centerx - other.rect.centerx)
            dy = (obj.rect.centery - other.rect.centery)
            overlap_x = (obj.rect.width + other.rect.width) // 2 - abs(dx)
            overlap_y = (obj.rect.height + other.rect.height) // 2 - abs(dy)

            if overlap_x > 0 and overlap_y > 0:
                if overlap_x < overlap_y:
                    shift = overlap_x // 2
                    if dx > 0:
                        if not math.isinf(obj.mass): obj.pos[0] += shift
                        if not math.isinf(other.mass): other.pos[0] -= shift
                    else:
                        if not math.isinf(obj.mass): obj.pos[0] -= shift
                        if not math.isinf(other.mass): other.pos[0] += shift
                else:
                    shift = overlap_y // 2
                    if dy > 0:
                        if not math.isinf(obj.mass): obj.pos[1] += shift
                        if not math.isinf(other.mass): other.pos[1] -= shift
                    else:
                        if not math.isinf(obj.mass): obj.pos[1] -= shift
                        if not math.isinf(other.mass): other.pos[1] += shift
