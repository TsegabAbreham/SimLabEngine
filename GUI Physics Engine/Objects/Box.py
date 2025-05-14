from RawSimLabEngine.engine import Box



default_rules = []

def addrules(rule):
    default_rules.append(rule)

# Factory function to create new Box instances
def BoxPrefab(default_pos = (100, 180),
    default_vel = (100, 0),
    default_size = (50, 50),
    default_mass = 2,
    default_gravity = 2,
    default_friction_coefficient = 0.8,
    default_color = (255, 60, 60)):
    # Default attributes for the BoxPrefab
    



    box = Box(
        pos=default_pos,
        vel=default_vel,
        size=default_size,
        mass=default_mass,
        gravity=default_gravity,
        friction_coefficient=default_friction_coefficient,
        color=default_color
    )
    for rule in default_rules:
        box.add_rule(rule)
    return box