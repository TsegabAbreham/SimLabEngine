For full documentation visit [mkdocs.org](https://www.mkdocs.org).


* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.


    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.



## Creating a New Window


To create a new window using the SimLabEngine we first have to follow these steps.

We first have to import the RawSimLabEngine, where all the main engine file is stored:

    from RawSimLabEngine.engine import * # This imports all the necessary engine files.

According to the code above we can make our scene by: 

    scene = Scene(width=800,height=600,title= "First Window", background_color=(255, 255, 255))

The code above makes the window 800x600, changes its title to "First Window" then makes it background white. If you click run you notice that nothing appears, this happened because SimLab doesn't know for how much you want to open it. To do this add this line below: 

    scene.simulate(duration=10, fps=60)

We set the duration to 10 seconds (the time the window will stay open before closing again), then the fps or frames per second, the higher it is the smoother the simulation becomes, but keep in mind 60 is a recommended fps to run and making it higher than that makes your computer slower. 

If you now click run you should see an empty window.