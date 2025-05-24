# Scene

The scene class takes in:

    Scene(width=800, height=600, background_color=(0, 0, 0), title="Scene", icon="SimLabEngineLogo.png")

 - Width and height control the window width and height.
 - background_color control the color of the background, takes in rgb value. 
 - title takes in the title of the window when it is created.
 - The icon is set by default and is the icon of the window.

### Reset

To reset the whole scene use:
    
    scene.reset()

where "scene" is:

    scene = Scene(width=800, height=600, background_color=(0, 0, 0), title="Scene")

### Time Scale

To control the time of the scene, meaning to make it fast or slow motion use:

    scene.set_time_scale(1) 

Where 1 is normal motion, upove 1 is fast motion and below 1 is slow motion.

### Adding objects

To add objects to the scene use:

    scene.add(obj1, obj2)

Note obj1 and obj2 are examples. This will add obj1 and obj2 to the scene. Adding more objects is possible. 

### Sound

To add sound use:

    scene.playsound(path_to_your_sound)

This will play the sound provided by the path. 


### Follow Object

To follow an object use:

    scene.follow_object(targetobj)

Note: "targetobj" is the object in the scene. This follows the object in the scene. 

### Get All Objects

To get all the objects existing in the scene use:

    scene.get_all_objects()

This will return an array of the objects' name exisitng in the scene.

### Displaying the window

To open or display the scene you made use:

    scene.simulate(duration=10, fps=60)

The duration parameter controls for how long the window should stay open then the fps controls the frames per second.





 
