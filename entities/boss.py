import pygame
from settings import (
    COLORS, SPRITE_WIDTH, SPRITE_HEIGHT, SPRITE_SCALE,
    SPRITES_PATH, BOSS_SPRITESHEET, BOSS_ANIMATIONS
)
from enemy import Enemy

try:
    from core.sprite_sheet import SpriteSheet
except ImportError:
    class SpriteSheet:
        def __init__(self, *args, **kwargs): pass

        def get_frames(self, *args, **kwargs): return []


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, spawn_interval=2000):
        super().__init__()

        self.facing_right = True
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8

        self.idle_frames = []
        self.look_left_frames = []
        self.look_right_frames = []
        self.attack_left_frames = []
        self.attack_right_frames = []

        self.state = 'idle'
        self.health = 100

        try:
            sprite_path = f"{SPRITES_PATH}/{BOSS_SPRITESHEET}"
            sheet = SpriteSheet(sprite_path, SPRITE_WIDTH, SPRITE_HEIGHT, SPRITE_SCALE)

            self.idle_frames = sheet.get_row_frames(BOSS_ANIMATIONS['idle'][0], BOSS_ANIMATIONS['idle'][1])
            self.look_left_frames = sheet.get_row_frames(BOSS_ANIMATIONS['look_left'][0], BOSS_ANIMATIONS['look_left'][1])
            self.look_right_frames = sheet.get_row_frames(BOSS_ANIMATIONS['look_right'][0], BOSS_ANIMATIONS['look_right'][1])
            self.attack_left_frames = sheet.get_row_frames(BOSS_ANIMATIONS['attack_left'][0], BOSS_ANIMATIONS['attack_left'][1])
            self.attack_right_frames = sheet.get_row_frames(BOSS_ANIMATIONS['attack_right'][0], BOSS_ANIMATIONS['attack_right'][1])

            print(f"Boss: Загружено кадров idle: {len(self.idle_frames)}, look: {len(self.look_left_frames)}, attack: {len(self.attack_left_frames)}")

            if self.idle_frames:
                self.image = self.idle_frames[0]
            else:
                self.image = self._make_fallback()
        except Exception as e:
            print(f"Ошибка загрузки спрайтов босса: {e}")
            self.image = self._make_fallback()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.direction = 1
        self.spawn_timer = 0
        self.spawn_interval = spawn_interval
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 1000

    def _make_fallback(self):
        size = (SPRITE_WIDTH * SPRITE_SCALE * 2, SPRITE_HEIGHT * SPRITE_SCALE * 2)
        surf = pygame.Surface(size)
        surf.fill(COLORS['PURPLE'])
        return surf

    def update(self, platforms, current_time, enemies_group, all_sprites_group):
        player_centerx = 600
        if self.rect.centerx > player_centerx:
            self.facing_right = False
            self.state = 'attack_left' if self.is_attacking else 'look_left'
        else:
            self.facing_right = True
            self.state = 'attack_right' if self.is_attacking else 'look_right'

        # Обновление анимации атаки
        if self.is_attacking:
            if current_time - self.attack_timer > self.attack_duration:
                self.is_attacking = False
        else:
            # Спавн вирусов
            if current_time - self.spawn_timer > self.spawn_interval:
                self.spawn_timer = current_time
                virus = Enemy(self.rect.centerx, self.rect.bottom, speed=2.5)
                enemies_group.add(virus)
                all_sprites_group.add(virus)
            # Случайная атака
            if current_time % 5000 < 10:
                self.is_attacking = True
                self.attack_timer = current_time

        self.rect.x += self.speed * self.direction

        on_platform = False
        for p in platforms:
            if abs(self.rect.bottom - p.top) < 10 and p.left <= self.rect.centerx <= p.right:
                on_platform = True
                if self.rect.right >= p.right:
                    self.direction = -1
                elif self.rect.left <= p.left:
                    self.direction = 1
                break

        if not on_platform:
            self.direction *= -1

        if self.rect.right > 1200:
            self.rect.right = 1200
            self.direction = -1
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction = 1

        self._update_animation()

    def _update_animation(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0

            frames = self._get_current_frames()
            if frames:
                self.current_frame = (self.current_frame + 1) % len(frames)
                self.image = frames[self.current_frame]

    def _get_current_frames(self):
        if self.state == 'idle':
            return self.idle_frames if self.idle_frames else [self.image]
        elif self.state == 'look_left':
            return self.look_left_frames if self.look_left_frames else [self.image]
        elif self.state == 'look_right':
            return self.look_right_frames if self.look_right_frames else [self.image]
        elif self.state == 'attack_left':
            return self.attack_left_frames if self.attack_left_frames else [self.image]
        elif self.state == 'attack_right':
            return self.attack_right_frames if self.attack_right_frames else [self.image]
        return [self.image]


    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()