import pygame
import os
import ctypes
ctypes.windll.user32.SetProcessDPIAware()

class Scene:
    def __init__(self, width=800, height=600, background_color=(0, 0, 0), title="Scene", icon="SimLabEngineLogo.png"):
        pygame.init()
        pygame.display.set_caption(title)

        icon_path = os.path.join(os.path.dirname(__file__), icon)
        if os.path.exists(icon_path):
            pygame.display.set_icon(pygame.image.load(icon_path))
        else:
            print(f"Warning: Icon not found at {icon_path}")

        self.screen = pygame.display.set_mode((width, height), pygame.SCALED)
        self.background_color = background_color
        self.clock = pygame.time.Clock()
        self.objects = []
        self.running = True
        self.camera = [0, 0]
        self.follow_target = None
        self.time_scale = 1.0  # 1.0 = normal speed

    def reset(self):
        self.camera = [0, 0]
        self.running = True
        for obj in self.objects:
            if hasattr(obj, 'reset'):
                obj.reset()

    def set_time_scale(self, scale: float):
        self.time_scale = scale

    def add(self, *objs):
        for obj in objs:
            obj.scene = self
        self.objects.extend(objs)

    def playsound(self, sound_path):
        pygame.mixer.init()
        sound = pygame.mixer.Sound(sound_path)
        sound.play()

    def follow_object(self, target):
        self.follow_target = target

    def update_camera(self, dt):
        if self.follow_target:
            self.camera[0] = self.follow_target.pos[0] - self.screen.get_width() / 2
            self.camera[1] = self.follow_target.pos[1] - self.screen.get_height() / 2

    def simulate(self, duration=10, fps=60, on_event=None, on_update=None, on_draw=None):
        time_elapsed = 0
        while self.running and time_elapsed < duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if on_event:
                    on_event(event)

            raw_dt = self.clock.tick(fps) / 1000.0
            dt = raw_dt * self.time_scale
            time_elapsed += dt

            self.update_camera(dt)

            if on_update:
                on_update(dt)

            for obj in self.objects:
                obj.apply_rules(dt)
                obj.update(dt)

            self.screen.fill(self.background_color)

            for obj in self.objects:
                obj.draw(self.screen, self.camera)

            if on_draw:
                on_draw(self.screen)

            pygame.display.flip()

        pygame.quit()

    def get_all_objects(self):
        return self.objects
