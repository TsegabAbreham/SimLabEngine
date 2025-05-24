The `Text` class represents a 2D text component for adding text to your simulations.  
It supports Latex so you can showcase your physics simulations with the theory behind it.

---

### Initialization
Creates a new instance with the following parameter:

    text = Text(text, font, pos, color=(200, 100, 255))

- **text** (string): The text you want to display.
- **font** (float): Font size of your text.
- **pos** (tuple): The position your text will be placed.
- **color** (tuple): The color of you text rgb.

---

### Latex
Renders a latex from latex code: 

    text.latex(latexcode,fontsize)

- **latexcode** (string): Takes in latex code.
- **fonsize** (float): size of the font for the latex.

