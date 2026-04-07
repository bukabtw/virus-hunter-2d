import pygame
from settings import (
    COLORS, SPRITE_WIDTH, SPRITE_HEIGHT, SPRITE_SCALE,
    SPRITES_PATH, PROJECTILE_SPRITESHEET, PROJECTILE_ANIMATIONS
)

try:
    from core.sprite_sheet import SpriteSheet
except ImportError:
    class SpriteSheet:
        def __init__(self, *args, **kwargs): pass

        def get_frames(self, *args, **kwargs): return []


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_right, owner):
        super().__init__()

        self.facing_right = facing_right
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10

        self.fly_frames = []
        self.owner = owner
        self.state = 'fly'
        self.return_speed = 3
        self.max_distance = 800
        self.start_x = x

        try:
            sprite_path = f"{SPRITES_PATH}/{PROJECTILE_SPRITESHEET}"
            sheet = SpriteSheet(sprite_path, 32, 32, SPRITE_SCALE)
            self.fly_frames = sheet.get_row_frames(PROJECTILE_ANIMATIONS['fly'][0], PROJECTILE_ANIMATIONS['fly'][1])
            print(f"Projectile: Загружено кадров fly: {len(self.fly_frames)}")
            if self.fly_frames:
                self.image = self.fly_frames[0]
                if not self.facing_right:
                    self.image = pygame.transform.flip(self.image, True, False)
            else:
                self.image = self._make_fallback()
        except Exception as e:
            print(f"Ошибка загрузки спрайтов снаряда: {e}")
            self.image = self._make_fallback()


        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 20

    def _make_fallback(self):
        size = (SPRITE_WIDTH * SPRITE_SCALE // 4, SPRITE_HEIGHT * SPRITE_SCALE // 4)
        surf = pygame.Surface(size)
        surf.fill(COLORS['YELLOW'])
        return surf

    def update(self, player):
        if self.state == 'fly':
            if self.facing_right:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed

            if abs(self.rect.centerx - self.start_x) >= self.max_distance:
                self.state = 'return'
            if self.rect.right < 0 or self.rect.left > 5000:
                self.kill()
        elif self.state == 'return':
            if self.rect.centerx < player.rect.centerx:
                self.rect.x += self.return_speed
            elif self.rect.centerx > player.rect.centerx:
                self.rect.x -= self.return_speed
            if abs(self.rect.centerx - player.rect.centerx) < 5:
                self.kill()

        self._update_animation()


    def _update_animation(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0

            if self.fly_frames:
                self.current_frame = (self.current_frame + 1) % len(self.fly_frames)
                self.image = self.fly_frames[self.current_frame]
                if self.state == 'return':
                    if self.rect.centerx < self.owner.rect.centerx:
                        self.facing_right = True
                    else:
                        self.facing_right = False
                if not self.facing_right:
                    self.image = pygame.transform.flip(self.image, True, False)


    def is_returning(self):
        return self.state == 'return'


    def set_return(self):
        self.state = 'return'