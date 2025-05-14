import pygame

class Text:
    def __init__(self, text, font, pos, color=(200, 100, 255)):
        self.pos = list(pos)
        self.text = text
        self.font = font
        self.color = color
        self.rules = []  # List to hold object-specific rules
        self.scene = None  # Will be set when added to scene

    def add_rule(self, rule):
        pass

    def apply_rules(self, dt):
        pass

    def update(self, dt):
        pass

    def draw(self, screen, camera):
        font = pygame.font.SysFont(None, self.font)
        text_surface = font.render(self.text, True, self.color)
        screen.blit(text_surface, self.pos)