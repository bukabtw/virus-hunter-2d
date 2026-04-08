import pygame
from core.sprite_sheet import SpriteSheet

class AnimatedEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_path, frame_w, frame_h, scale, animations):
        super().__init__()
        self.frames = {}
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8
        self.state = 'idle'
        self.facing_right = True

        sheet = SpriteSheet(sprite_path, frame_w, frame_h, scale)
        for anim_name, (row, count) in animations.items():
            self.frames[anim_name] = sheet.get_row_frames(row, count)
        
        for anim_name in ['fly', 'idle', 'walk_right', 'look_right']:
            frames = self.frames.get(anim_name, [])
            if frames:
                self.image = frames[0]
                break
        else:
            self.image = self._make_fallback()
        
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def _make_fallback(self):
        surf = pygame.Surface((64, 64))
        surf.fill((100, 100, 100))
        return surf
    
    def update_animation(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            frames = self.frames.get(self.state, [])
            if frames:
                self.current_frame = (self.current_frame + 1) % len(frames)
                self.image = frames[self.current_frame]
                
    
    def set_state(self, state):
        if state != self.state:
            self.state = state
            self.current_frame = 0