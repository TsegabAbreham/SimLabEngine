import pygame

class BoundingBox:
    def __init__(self, rect, color=(200, 100, 255), thickness=5, mass = 99999):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.thickness = thickness
        self.mass = mass
        
    def draw(self, screen, camera=(0,0)):
        # Adjust for camera offset if needed:
        adjusted_rect = self.rect.copy()
        adjusted_rect.topleft = (self.rect.x - camera[0], self.rect.y - camera[1])
        pygame.draw.rect(screen, self.color, adjusted_rect, self.thickness)

    def restrict(self, obj):
        # Restrict object's rect within the bounding box.
        # Assumes obj has attributes: rect (pygame.Rect) and velocity ([vx, vy])
        if obj.rect.left < self.rect.left:
            obj.rect.left = self.rect.left
            obj.vel[0] = 0
        if obj.rect.right > self.rect.right:
            obj.rect.right = self.rect.right
            obj.vel[0] = 0
        if obj.rect.top < self.rect.top:
            obj.rect.top = self.rect.top
            obj.vel[1] = 0
        if obj.rect.bottom > self.rect.bottom:
            obj.rect.bottom = self.rect.bottom
            obj.vel[1] = 0

    def apply_rules(self, dt):
        # BoundingBox is static; do nothing.
        pass

    def update(self, dt):
        # BoundingBox is static; do nothing.
        pass
