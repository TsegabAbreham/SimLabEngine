The `Image` class represents a 2D objects for loading custom images to the scene.  

---

### Initialization

Creates a new instance with the following parameter:

    image = Image(path, pos, vel, rotation=0, mass=1, gravity=9.8, damping_factor=0.99, friction_coefficient=0.2)

- **pos** (tuple): Initial position `[x, y]`.
- **vel** (tuple): Initial velocity `[vx, vy]`.

These are the needed parameters for this class. Even though there is more, the 'Image' class only supports those two.


### Rotation

Changes the rotation angle of the box by a given amount.

Example:

    image.rotate(angle)


- **Parameter:** `angle` — rotation amount in degrees.
- Keeps rotation normalized between 0 and 360 degrees.
