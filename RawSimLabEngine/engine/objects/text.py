import pygame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import io

class Text:
    def __init__(self, text, font, pos, color=(200, 100, 255)):
        self.pos = list(pos)
        self.text = text
        self.font = font
        self.color = color
        self.rules = []  # List to hold object-specific rules
        self.scene = None  # Will be set when added to scene
        self.latex_surface = None  # Surface to store LaTeX rendering

    def add_rule(self, rule):
        pass

    def apply_rules(self, dt):
        pass

    def update(self, dt):
        pass

    def _rgb_to_mpl(self, rgb):
        return tuple(c / 255.0 for c in rgb)


    def latex(self, latex_string, fontsize=20):

        # Step 1: Create temporary figure to measure text
        fig = plt.figure(dpi=300)
        fig.patch.set_alpha(0.0)
        text = fig.text(0, 0, f"${latex_string}$", fontsize=fontsize, color=self._rgb_to_mpl(self.color))
        canvas = FigureCanvasAgg(fig)
        canvas.draw()

        # Step 2: Get bounding box of the text
        renderer = canvas.get_renderer()
        bbox = text.get_window_extent(renderer).expanded(1.1, 1.1)  # add a little padding
        width, height = bbox.width / fig.dpi, bbox.height / fig.dpi

        # Step 3: Create a new figure with correct size
        plt.close(fig)
        fig = plt.figure(figsize=(width, height), dpi=300)
        fig.patch.set_alpha(0.0)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        ax.text(0, 0, f"${latex_string}$", fontsize=fontsize, color=self._rgb_to_mpl(self.color), va='bottom', ha='left')

        # Step 4: Render again
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        raw_data = canvas.buffer_rgba()
        size = canvas.get_width_height()
        self.latex_surface = pygame.image.frombuffer(raw_data, size, "RGBA")
        plt.close(fig)



    def draw(self, screen, camera):
        if self.latex_surface:
            screen.blit(self.latex_surface, self.pos)
        else:
            font = pygame.font.SysFont(None, self.font)
            text_surface = font.render(self.text, True, self.color)
            screen.blit(text_surface, self.pos)
