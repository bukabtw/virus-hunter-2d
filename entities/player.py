import pygame
from settings import (
    COLORS, SPRITE_WIDTH, SPRITE_HEIGHT, SPRITE_SCALE,
    SPRITES_PATH, PLAYER_SPRITESHEET, PLAYER_ANIMATIONS,
    MAP_WIDTH, MAP_HEIGHT
)
from entities.projectile import Projectile

try:
    from core.sprite_sheet import SpriteSheet
except ImportError:
    class SpriteSheet:
        def __init__(self, *args, **kwargs): pass

        def get_frames(self, *args, **kwargs): return []


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.facing_right = True
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8

        self.idle_right_frames = []
        self.idle_left_frames = []
        self.walk_right_frames = []
        self.walk_left_frames = []
        self.jump_frames = []
        self.jump_right_frames = []
        self.jump_left_frames = []
        self.attack_right_frames = []
        self.attack_left_frames = []

        self.state = 'idle'
        self.on_ground = True

        try:
            sprite_path = f"{SPRITES_PATH}/{PLAYER_SPRITESHEET}"
            sheet = SpriteSheet(sprite_path, SPRITE_WIDTH, SPRITE_HEIGHT, SPRITE_SCALE)

            self.idle_right_frames = sheet.get_row_frames(PLAYER_ANIMATIONS['idle_right'][0], PLAYER_ANIMATIONS['idle_right'][1])
            self.idle_left_frames = sheet.get_row_frames(PLAYER_ANIMATIONS['idle_left'][0], PLAYER_ANIMATIONS['idle_left'][1])
            self.walk_right_frames = sheet.get_row_frames(PLAYER_ANIMATIONS['walk_right'][0], PLAYER_ANIMATIONS['walk_right'][1])
            self.walk_left_frames = sheet.get_row_frames(PLAYER_ANIMATIONS['walk_left'][0], PLAYER_ANIMATIONS['walk_left'][1])
            self.jump_right_frames = sheet.get_row_frames(PLAYER_ANIMATIONS['jump_right'][0], PLAYER_ANIMATIONS['jump_right'][1])
            self.jump_left_frames = sheet.get_row_frames(PLAYER_ANIMATIONS['jump_left'][0], PLAYER_ANIMATIONS['jump_left'][1])
            self.attack_right_frames = sheet.get_row_frames(PLAYER_ANIMATIONS['attack_right'][0], PLAYER_ANIMATIONS['attack_right'][1])
            self.attack_left_frames = sheet.get_row_frames(PLAYER_ANIMATIONS['attack_left'][0], PLAYER_ANIMATIONS['attack_left'][1])

            print(f"Player: Загружено кадров idle_right: {len(self.idle_right_frames)}, walk: {len(self.walk_right_frames)}, attack: {len(self.attack_right_frames)}, jump_right: {len(self.jump_right_frames)}, jump_left: {len(self.jump_left_frames)}")

            if self.idle_right_frames:
                self.image = self.idle_right_frames[0]
            else:
                self.image = self._make_fallback()
        except Exception as e:
            print(f"Ошибка загрузки спрайтов игрока: {e}")
            self.image = self._make_fallback()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width = SPRITE_WIDTH * SPRITE_SCALE
        self.rect.height = SPRITE_HEIGHT * SPRITE_SCALE

        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = -20
        self.gravity = 0.8
        self.health = 5
        self.friction = 0.8
        self.max_speed = 6.5
        self.ram_platform = False
        self.collected_items = []
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 400
        self.attack_cooldown = 0
        self.attack_cooldown_time = 1000

    def _make_fallback(self):
        size = (SPRITE_WIDTH * SPRITE_SCALE, SPRITE_HEIGHT * SPRITE_SCALE)
        surf = pygame.Surface(size)
        surf.fill(COLORS['BLACK'])
        pygame.draw.circle(surf, COLORS['WHITE'], (size[0] // 3, size[1] // 3), 5)
        pygame.draw.circle(surf, COLORS['WHITE'], (size[0] * 2 // 3, size[1] // 3), 5)
        pygame.draw.rect(surf, COLORS['BLUE'], (size[0] // 2 - 5, size[1] // 2, 10, 15))
        return surf

    def update(self, platforms):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        self.on_ground = False
        self.ram_platform = False
        for p in platforms:
            if self.rect.colliderect(p):
                if self.vel_y > 0:
                    self.rect.bottom = p.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    if hasattr(p, 'platform_type') and p.platform_type == 'ram':
                        self.ram_platform = True
                elif self.vel_y < 0:
                    self.rect.top = p.rect.bottom
                    self.vel_y = 0

        if self.ram_platform:
            self.speed = self.max_speed
        else:
            self.speed = 5

        self.rect.x += self.vel_x

        for p in platforms:
            if self.rect.colliderect(p):
                if self.vel_x > 0:
                    self.rect.right = p.rect.left
                elif self.vel_x < 0:
                    self.rect.left = p.rect.right

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > MAP_WIDTH:
            self.rect.right = MAP_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > MAP_HEIGHT:
            self.rect.bottom = MAP_HEIGHT
            self.vel_y = 0
            self.on_ground = True

        if self.is_attacking:
            self.state = 'attack_right' if self.facing_right else 'attack_left'
            if pygame.time.get_ticks() - self.attack_timer > self.attack_duration:
                self.is_attacking = False
        elif abs(self.vel_x) > 0.5:
            self.state = 'walk_right' if self.facing_right else 'walk_left'
        else:
            self.state = 'idle_right' if self.facing_right else 'idle_left'
        if not self.on_ground:
            self.state = 'jump_right' if self.facing_right else 'jump_left'

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
        if self.state == 'idle_right':
            return self.idle_right_frames if self.idle_right_frames else [self.image]
        elif self.state == 'idle_left':
            return self.idle_left_frames if self.idle_left_frames else [self.image]
        elif self.state == 'walk_right':
            return self.walk_right_frames if self.walk_right_frames else [self.image]
        elif self.state == 'walk_left':
            return self.walk_left_frames if self.walk_left_frames else [self.image]
        elif self.state == 'jump_right':
            return self.jump_right_frames if self.jump_right_frames else [self.image]
        elif self.state == 'jump_left':
            return self.jump_left_frames if self.jump_left_frames else [self.image]
        elif self.state == 'attack_right':
            return self.attack_right_frames if self.attack_right_frames else [self.image]
        elif self.state == 'attack_left':
            return self.attack_left_frames if self.attack_left_frames else [self.image]
        return [self.image]


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
            self.on_ground = False

    def attack(self):
        current_time = pygame.time.get_ticks()
        if not self.is_attacking and current_time - self.attack_cooldown > self.attack_cooldown_time:
            self.is_attacking = True
            self.attack_timer = current_time
            self.attack_cooldown = current_time
            proj = Projectile(
                self.rect.centerx,
                self.rect.centery,
                self.facing_right,
                self
            )
            return proj
        return None

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0