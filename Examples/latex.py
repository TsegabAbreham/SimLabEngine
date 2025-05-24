import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from RawSimLabEngine.engine import *

scene = Scene(800, 600)


text = Text(
    text="Hello, World!",
    font=10,
    pos=(100, 100),
    color=(200, 100, 255)
)

text.latex(r"\nabla f(x, y) = \left(\frac{\partial f}{\partial x}, \frac{\partial f}{\partial y}\right), \quad \iint_D \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) \, dx\,dy = \oint_C (P\,dx + Q\,dy)",
           fontsize=5)


scene.add(text)

scene.simulate(10, fps=60)