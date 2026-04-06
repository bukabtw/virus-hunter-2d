import pygame

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.lerp_speed = 0.1

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    
    def apply_rect(self, rect):
        if hasattr(rect, 'rect'):
            actual_rect = rect.rect
        else:
            actual_rect = rect
        return actual_rect.move(self.camera.topleft)
    
    def update(self, target):
        target_x = -target.rect.centerx + int(self.width / 2)
        target_y = -target.rect.centery + int(self.height / 2)
        
        current_x = self.camera.x
        current_y = self.camera.y
        
        new_x = current_x + (target_x - current_x) * self.lerp_speed
        new_y = current_y + (target_y - current_y) * self.lerp_speed

        new_x = int(new_x)
        new_y = int(new_y)

        new_x = min(0, new_x)
        new_y = min(0, new_y)
        new_x = max(-(self.width), new_x)
        new_y = max(-(self.height), new_y)
        
        self.camera = pygame.Rect(new_x, new_y, self.width, self.height)
