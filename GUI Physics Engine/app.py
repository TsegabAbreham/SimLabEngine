import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from RawSimLabEngine.engine import Scene, Box, BoundingBox, gravity, velocity
from UI import run_ui
from Objects.Box import BoxPrefab
import pygame

pygame.init()
screen_size = (1280, 720)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("SimLab with UI")

# ----------------------------
# Setup Simulation Scene
# ----------------------------
scene = Scene(1280, 720, background_color=(220, 255, 220), title="Video Recording")



scene.add()
run_ui(scene)

run_ui.on_my_button_click()