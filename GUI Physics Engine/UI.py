import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from SimLabUI.GUI import SimLabUI
from RawSimLabEngine.engine import *
from Objects.Box import BoxPrefab
import pygame
import pygame_gui

def run_ui(scene):
    # Get the screen dimensions from pygame
    screen_size = pygame.display.Info().current_w, pygame.display.Info().current_h
    # Create the UI system
    ui = SimLabUI(screen_size)
    
    # --------------------------------------------------------------------
    # Create a left-side container panel to group UI controls.
    # --------------------------------------------------------------------
    left_container = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((10, 10), (350, 500)),
        manager=ui.manager,
        anchors={'left': 'left', 'top': 'top'}
    )
    
    y_offset = 20
    # --------------------------------------------------------------------
    # Instead of checkboxes, add a text entry field for rules.
    # --------------------------------------------------------------------
    label_rules = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((20, y_offset), (300, 30)),
        text="Enter Rules (comma separated):",
        manager=ui.manager,
        container=left_container
    )
    y_offset += 40
    rule_entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((20, y_offset), (300, 30)),
        manager=ui.manager,
        container=left_container
    )
    rule_entry.set_text("gravity, velocity")  # Default rule text
    y_offset += 40

    # Available rules dictionary for lookup.
    available_rules = {"gravity": gravity, "velocity": velocity, "collision": collision}
    
    # --------------------------------------------------------------------
    # Add text entries for object attributes.
    # We'll store default values as comma-separated strings.
    # --------------------------------------------------------------------
    pos_entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((20, y_offset), (300, 30)),
        manager=ui.manager,
        container=left_container
    )
    pos_entry.set_text("100,180")  # Default position
    y_offset += 40

    vel_entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((20, y_offset), (300, 30)),
        manager=ui.manager,
        container=left_container
    )
    vel_entry.set_text("100,0")  # Default velocity
    y_offset += 40

    size_entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((20, y_offset), (300, 30)),
        manager=ui.manager,
        container=left_container
    )
    size_entry.set_text("50,50")  # Default size
    y_offset += 40

    mass_entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((20, y_offset), (300, 30)),
        manager=ui.manager,
        container=left_container
    )
    mass_entry.set_text("2")  # Default mass
    y_offset += 40

    gravity_entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((20, y_offset), (300, 30)),
        manager=ui.manager,
        container=left_container
    )
    gravity_entry.set_text("2")  # Default gravity value (can override prefab)
    y_offset += 40

    friction_entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((20, y_offset), (300, 30)),
        manager=ui.manager,
        container=left_container
    )
    friction_entry.set_text("0.8")  # Default friction coefficient
    y_offset += 40

    color_entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((20, y_offset), (300, 30)),
        manager=ui.manager,
        container=left_container
    )
    color_entry.set_text("255,60,60")  # Default RGB color
    y_offset += 40
    
    # --------------------------------------------------------------------
    # Add a button to change background color via a color picker.
    # --------------------------------------------------------------------
    def on_change_bg_color(col):
        scene.background_color = (col.r, col.g, col.b)
        print("Background color set to:", col)
    
    ui.button(
        name="bg_color_button",
        relative_rect=pygame.Rect((20, y_offset), (150, 50)),
        text="Change BG Color",
        on_click=lambda: ui.color_picker(
            name="bg_picker",
            rect=pygame.Rect((400, 100), (400, 400)),
            initial_color=scene.background_color,
            window_title="Select BG Color",
            on_color_pick=on_change_bg_color
        )
    )
    y_offset += 70

    # --------------------------------------------------------------------
    # Add a button to instantiate a Box with the values from text entries.
    # --------------------------------------------------------------------
    def on_add_box_click():
        try:
            # Parse the values from the text entries and convert them to mutable lists.
            pos_values = [int(x.strip()) for x in pos_entry.get_text().split(",")]
            vel_values = [int(x.strip()) for x in vel_entry.get_text().split(",")]
            size_values = [int(x.strip()) for x in size_entry.get_text().split(",")]
            mass_value = float(mass_entry.get_text())
            gravity_value = float(gravity_entry.get_text())
            friction_value = float(friction_entry.get_text())
            color_values = [int(x.strip()) for x in color_entry.get_text().split(",")]
        except Exception as e:
            print("Error parsing input:", e)
            return
        
        # Create a new box using BoxPrefab (a factory function).
        new_box = BoxPrefab()
        # Override the default attributes with user-provided values.
        new_box.pos = pos_values
        new_box.vel = vel_values
        new_box.size = size_values
        new_box.mass = mass_value
        new_box.gravity = gravity_value
        new_box.friction_coefficient = friction_value
        new_box.color = color_values
        
        # Parse the rules from the rule_entry (comma-separated)
        rule_text = rule_entry.get_text()
        rule_names = [r.strip().lower() for r in rule_text.split(",")]
        for rule_name in rule_names:
            if rule_name in available_rules:
                new_box.add_rule(available_rules[rule_name])
        scene.add(new_box)
        print("New BoxPrefab added:", new_box)

    ui.button(
        name="add_box_button",
        relative_rect=pygame.Rect((20, y_offset), (120, 50)),
        text="Add Box",
        on_click=on_add_box_click
    )
    
    # Run the UI loop (this call will block until the user quits)
    ui.run(scene)