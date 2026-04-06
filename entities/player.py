import pygame
from settings import COLORS, SPRITE_SIZE, SPRITE_SCALE, SPRITES_PATH, PLAYER_SPRITESHEET

try:
    from core.sprite_sheet import SpriteSheet
except ImportError:
    class SpriteSheet:
        def __init__(self, *args, **kwargs): pass

        def get_animation(self, *args, **kwargs): return []

        def get_frames(self, *args, **kwargs): return []


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, use_spritesheet=True):
        super().__init__()

        self.use_spritesheet = use_spritesheet
        self.facing_right = True
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8
        self.state = 'idle'

        # Сначала создаем fallback-спрайты (на всякий случай)
        self._generate_fallback_sprites()

        if use_spritesheet:
            try:
                import os
                sprite_path = os.path.join(SPRITES_PATH, PLAYER_SPRITESHEET)
                sheet = SpriteSheet(sprite_path, SPRITE_SIZE, SPRITE_SIZE, SPRITE_SCALE)

                idle_frames = sheet.get_animation(0, 4)
                if idle_frames:
                    self.idle_frames = idle_frames

                run_frames = sheet.get_animation(1, 6)
                if run_frames:
                    self.run_frames = run_frames

                jump_frames = sheet.get_animation(2, 2)
                if jump_frames:
                    self.jump_frames = jump_frames

                attack_frames = sheet.get_animation(3, 4)
                if attack_frames:
                    self.attack_frames = attack_frames

                print("Спрайт-лист успешно загружен!")
            except Exception as e:
                print(f"Не удалось загрузить спрайт-лист: {e}, используем fallback-спрайты")

        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = True
        self.speed = 5
        self.jump_power = -12
        self.gravity = 0.8

        self.health = 5
        self.attack_timer = 0
        self.invincible_timer = 0

    def _generate_fallback_sprites(self):
        self.idle_frames = []
        self.run_frames = []
        self.jump_frames = []
        self.attack_frames = []

        for i in range(4):
            surf = pygame.Surface((45, 55), pygame.SRCALPHA)
            pygame.draw.rect(surf, COLORS['BLACK'], (10, 15, 25, 35))
            pygame.draw.ellipse(surf, (200, 180, 150), (12, 5, 21, 20))
            pygame.draw.rect(surf, COLORS['CYAN'], (14, 12, 8, 6), 2)
            pygame.draw.rect(surf, COLORS['CYAN'], (24, 12, 8, 6), 2)
            pygame.draw.rect(surf, COLORS['GRAY'], (28, 25, 12, 18))
            pygame.draw.rect(surf, COLORS['BLUE'], (30, 27, 8, 14))
            pygame.draw.ellipse(surf, COLORS['BLACK'], (12, 2, 22, 10))
            self.idle_frames.append(surf)

        self.run_frames = self.idle_frames[:]
        self.jump_frames = [self.idle_frames[0], self.idle_frames[0]]
        self.attack_frames = self.idle_frames[:]

    def update(self, platforms):

        self.vel_y += self.gravity
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p) and self.vel_y >= 0:
                self.rect.bottom = p.top
                self.vel_y = 0
                self.on_ground = True

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > 1200: self.rect.right = 1200

        self._update_animation()

        if self.attack_timer > 0:
            self.attack_timer -= 1
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

    def _update_animation(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0

            frames = self._get_current_frames()
            if frames:
                self.current_frame = (self.current_frame + 1) % len(frames)
                self.image = frames[self.current_frame]

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def _get_current_frames(self):
        if self.attack_timer > 0:
            return self.attack_frames
        elif not self.on_ground:
            return self.jump_frames
        elif abs(self.vel_x) > 0.5:
            return self.run_frames
        else:
            return self.idle_frames

    def move_left(self):
        self.vel_x = -self.speed
        self.facing_right = False

    def move_right(self):
        self.vel_x = self.speed
        self.facing_right = True

    def stop(self):
        self.vel_x = 0

    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_power

    def attack(self):
        if self.attack_timer == 0:
            self.attack_timer = 20
            self.current_frame = 0
            return True
        return False

    def take_damage(self, amount=1):
        if self.invincible_timer == 0:
            self.health -= amount
            self.invincible_timer = 30
            return True
        return False

    def draw(self, screen, camera_x=0):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))