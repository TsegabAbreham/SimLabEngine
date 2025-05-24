The `Cloth` class represents a 2D object that is meant to simulate clothing.

---

### Initialization
Creates a new instance with the following parameter:

    cloth = Cloth(rows, cols, spacing, vel=(0,0), pos=(0,0), gravity=9.8, mass=1, pin_top=False)

- **rows**(int): Rows of the cloth.
- **cols**(int): Columns of the cloth.
- **spacing** (int): Spacing between the particles on the cloth. 
- **vel** (tuple): The velocity of the cloth.
- **pos** (tuple): The position of the cloth.
- **gravity** (float): The gravity acceleration of the cloth.
- **mass** (float): Mass of the cloth.
- **pin_top** (bool): Wheather to pin the top so the cloth doesn't fall.


### Physics Rule
To add physics rule to cloth: 

    cloth.add_rule(rule)

- **rule**: Rule name

