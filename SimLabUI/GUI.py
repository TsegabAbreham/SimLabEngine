import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from RawSimLabEngine.engine import *
import pygame
import pygame_gui

# --- Custom realtime graph element ---
class RealtimeGraph:
    def __init__(self, relative_rect, max_points=100, background_color=(0, 0, 0), line_color=(0, 255, 0)):
        self.rect = pygame.Rect(relative_rect)
        self.max_points = max_points
        self.data = []
        self.background_color = background_color
        self.line_color = line_color
        self.surface = pygame.Surface(self.rect.size)
        self.surface.fill(self.background_color)
    
    def add_data(self, data_point):
        if len(self.data) >= self.max_points:
            self.data.pop(0)
        self.data.append(data_point)
        self.redraw()
    
    def redraw(self):
        self.surface.fill(self.background_color)

        if len(self.data) > 1:
            # Fixed vertical scale: set your own min and max
            min_val = 0
            max_val = 100  # Adjust this to match your data range

            scaled = [
                ((val - min_val) / (max_val - min_val)) * self.rect.height 
                for val in self.data
            ]
            points = []
            dx = self.rect.width / (self.max_points - 1)

            for i, y in enumerate(scaled):
                # Invert the y value because pygame's y=0 is at the top.
                points.append((i * dx, self.rect.height - y))

            pygame.draw.lines(self.surface, self.line_color, False, points, 2)

    
    def draw(self, screen):
        screen.blit(self.surface, self.rect)


class SimLabUI:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.manager = pygame_gui.UIManager(screen_size)
        self.elements = {}    # Stores UI elements by name.
        self.callbacks = {}   # Stores on_click or on_change callbacks for elements.
        # Hold any custom UI elements such as realtime graphs.
        self.custom_elements = {}
    
    def button(self, name, relative_rect, text, on_click=None):
        btn = pygame_gui.elements.UIButton(
            relative_rect=relative_rect,
            text=text,
            manager=self.manager
        )
        self.elements[name] = btn
        if on_click:
            self.callbacks[name] = on_click
        return btn

    def slider(self, name, relative_rect, start_value, value_range, on_value_change=None):
        slider_element = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=relative_rect,
            start_value=start_value,
            value_range=value_range,
            manager=self.manager
        )
        self.elements[name] = slider_element
        if on_value_change:
            self.callbacks[name] = on_value_change
        return slider_element

    def label(self, name, relative_rect, text):
        label_element = pygame_gui.elements.UILabel(
            relative_rect=relative_rect,
            text=text,
            manager=self.manager
        )
        self.elements[name] = label_element
        return label_element

    def text_entry(self, name, relative_rect, on_text_entered=None):
        text_entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=relative_rect,
            manager=self.manager
        )
        self.elements[name] = text_entry
        if on_text_entered:
            self.callbacks[name] = on_text_entered
        return text_entry

    def text_box(self, name, relative_rect, html_text):
        text_box = pygame_gui.elements.UITextBox(
            html_text=html_text,
            relative_rect=relative_rect,
            manager=self.manager
        )
        self.elements[name] = text_box
        return text_box

    def drop_down(self, name, relative_rect, options_list, starting_option, on_option_selected=None):
        drop_down = pygame_gui.elements.UIDropDownMenu(
            options_list=options_list,
            starting_option=starting_option,
            relative_rect=relative_rect,
            manager=self.manager
        )
        self.elements[name] = drop_down
        if on_option_selected:
            self.callbacks[name] = on_option_selected
        return drop_down

    def check_box(self, name, relative_rect, text, on_checked=None):
        check_box = pygame_gui.elements.UICheckBox(
            text=text,
            relative_rect=relative_rect,
            manager=self.manager
        )
        self.elements[name] = check_box
        if on_checked:
            self.callbacks[name] = on_checked
        return check_box

    def progress_bar(self, name, relative_rect, progress=0.0):
        progress_bar = pygame_gui.elements.UIProgressBar(
            relative_rect=relative_rect,
            manager=self.manager
        )
        progress_bar.set_current_progress(progress)
        self.elements[name] = progress_bar
        return progress_bar

    def color_picker(self, name, rect, initial_color, window_title="Pick a Color", on_color_pick=None):
        if not isinstance(initial_color, pygame.Color):
            initial_color = pygame.Color(*initial_color)
        color_picker_dialog = pygame_gui.windows.UIColourPickerDialog(
            rect=rect,
            manager=self.manager,
            window_title=window_title,
            initial_colour=initial_color
        )
        self.elements[name] = color_picker_dialog
        if on_color_pick:
            self.callbacks[name] = on_color_pick
        return color_picker_dialog

    def file_dialog(self, name, rect, window_title="Select a File", on_file_selected=None):
        file_dialog = pygame_gui.windows.UIFileDialog(
            rect=rect,
            manager=self.manager,
            window_title=window_title
        )
        self.elements[name] = file_dialog
        if on_file_selected:
            self.callbacks[name] = on_file_selected
        return file_dialog

    def add_realtime_graph(self, name, relative_rect, max_points=100, background_color=(0, 0, 0), line_color=(0, 255, 0)):
        graph = RealtimeGraph(relative_rect, max_points, background_color, line_color)
        self.custom_elements[name] = graph
        return graph

    def process_events(self, event):
        """
        Process events for the UI manager and call callbacks if necessary.
        """
        self.manager.process_events(event)
        if event.type == pygame.USEREVENT:
            # Process button pressed events.
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                for name, element in list(self.elements.items()):
                    if event.ui_element == element and name in self.callbacks:
                        self.callbacks[name]()
            # Process slider moved events.
            elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                for name, element in list(self.elements.items()):
                    if event.ui_element == element and name in self.callbacks:
                        self.callbacks[name](event.value)
            # Process colour picker events.
            elif event.user_type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                for name, element in list(self.elements.items()):
                    if event.ui_element == element and name in self.callbacks:
                        self.callbacks[name](event.colour)
            # Process text entry events.
            elif event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                for name, element in list(self.elements.items()):
                    if event.ui_element == element and name in self.callbacks:
                        self.callbacks[name](event.text)
            # Process drop-down menu events.
            elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                for name, element in list(self.elements.items()):
                    if event.ui_element == element and name in self.callbacks:
                        self.callbacks[name](event.text)

    def update(self, time_delta):
        self.manager.update(time_delta)

    def draw(self, surface):
        self.manager.draw_ui(surface)
        # Draw any custom elements (like realtime graphs)
        for element in self.custom_elements.values():
            element.draw(surface)
    
    def run(self, scene, simulation_update=None):
        clock = pygame.time.Clock()
        running = True
        while running:
            time_delta = clock.tick(60) / 1000.0  # frame time in seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.process_events(event)
            
            # Update simulation objects: either use custom callback or default.
            if simulation_update and callable(simulation_update):
                simulation_update(time_delta)
            else:
                for obj in scene.objects:
                    obj.apply_rules(time_delta)
                    obj.update(time_delta)
            
            # Clear screen and draw simulation objects.
            scene.screen.fill(scene.background_color)
            for obj in scene.objects:
                obj.draw(scene.screen, scene.camera)
            
            # Update and draw UI on top plus custom (realtime) elements.
            self.update(time_delta)
            self.draw(scene.screen)
            
            pygame.display.flip()
        pygame.quit()