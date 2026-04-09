import pygame
from settings import *
from core.animated_entity import AnimatedEntity
from core.damageable import Damageable
from entities.enemy import Enemy

class Boss(AnimatedEntity, Damageable):
    def __init__(self, x, y, spawn_interval=3000):
        animations = {
            'idle': BOSS_ANIMATIONS['idle'],
            'look_left': BOSS_ANIMATIONS['look_left'],
            'look_right': BOSS_ANIMATIONS['look_right'],
            'attack_left': BOSS_ANIMATIONS['attack_left'],
            'attack_right': BOSS_ANIMATIONS['attack_right'],
        }
        
        sprite_path = f"{SPRITES_PATH}/{BOSS_SPRITESHEET}"
        super().__init__(x, y, sprite_path, SPRITE_WIDTH, SPRITE_HEIGHT, SPRITE_SCALE, animations)
        Damageable.__init__(self, max_health=100, invincible_duration=30)
        
        COLLIDE_W = 90
        COLLIDE_H = 100
        OFFSET_X = 19
        OFFSET_Y = 14
        
        self.collide_offset_x = OFFSET_X
        self.collide_offset_y = OFFSET_Y
        
        self.visual_rect = self.rect.copy()
        
        self.collision_rect = pygame.Rect(
            self.visual_rect.x + OFFSET_X,
            self.visual_rect.y + OFFSET_Y,
            COLLIDE_W,
            COLLIDE_H
        )
        
        self.speed = 1.5
        self.direction = 1
        self.phase = 1
        self.phase_changed = False
        
        self.spawn_timer = 0
        self.spawn_interval = spawn_interval
        self.attack_timer = 0
        self.attack_delay = 60
        self.attack_cooldown = 0
        self.dash_timer = 0
        self.spawn_enabled = True
        
        self.knockback_timer = 0
        self.knockback_direction = 0
        self.is_boss = True
        self.sound_manager = None
        self.frozen = False
    
    def update(self, platforms, current_time, enemies_group, all_sprites_group, player):
        self.update_invincibility()
        
        if self.health <= 66 and self.phase == 1:
            self.phase = 2
            self.phase_changed = True
            self.speed = 2.0
            if self.sound_manager:
                self.sound_manager.play_boss_roar()
        elif self.health <= 33 and self.phase == 2:
            self.phase = 3
            self.phase_changed = True
            self.speed = 2.5
            if self.sound_manager:
                self.sound_manager.play_boss_roar()
        
        if self.frozen:
            self.rect = self.visual_rect
            self.update_animation()
            return
        
        self.collision_rect.x = self.visual_rect.x + self.collide_offset_x
        self.collision_rect.y = self.visual_rect.y + self.collide_offset_y
        
        if self.knockback_timer > 0:
            self.knockback_timer -= 1
            self.visual_rect.x += self.knockback_direction * 5
            self.collision_rect.x = self.visual_rect.x + self.collide_offset_x
            self.rect = self.visual_rect
            return
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        if player and player.alive():
            if self.visual_rect.x < player.visual_rect.x:
                self.direction = 1
                self.facing_right = True
            elif self.visual_rect.x > player.visual_rect.x:
                self.direction = -1
                self.facing_right = False
            
            self.visual_rect.x += self.speed * self.direction
            self.collision_rect.x = self.visual_rect.x + self.collide_offset_x
            
            if self.collision_rect.colliderect(player.collision_rect) and self.attack_cooldown == 0:
                self.attack_cooldown = self.attack_delay
                damage = 2 if self.phase == 1 else (3 if self.phase == 2 else 4)
                player.take_damage(damage)
                self.knockback_timer = 10
                self.knockback_direction = -self.direction
                if self.sound_manager:
                    self.sound_manager.play_attack('boss')
        
        if self.spawn_enabled and self.phase >= 2:
            if current_time - self.spawn_timer > self.spawn_interval:
                self.spawn_timer = current_time
                offset = -60 if self.direction > 0 else 60
                count = 2 if self.phase == 3 else 1
                for i in range(count):
                    virus = Enemy(
                        self.visual_rect.centerx + offset + (i * 40),
                        self.visual_rect.bottom - 20,
                        speed=2.5 if self.phase == 3 else 2.0
                    )
                    enemies_group.add(virus)
                    all_sprites_group.add(virus)
                if self.sound_manager:
                    self.sound_manager.play_boss_spawn()
        
        if self.phase == 3:
            self.dash_timer += 1
            if self.dash_timer > 180 and abs(self.visual_rect.x - player.visual_rect.x) < 200:
                self.dash_timer = 0
                self.visual_rect.x += 100 * self.direction
                if self.sound_manager:
                    self.sound_manager.play_attack('boss')
        
        if self.visual_rect.left < 0:
            self.visual_rect.left = 0
        if self.visual_rect.right > MAP_WIDTH:
            self.visual_rect.right = MAP_WIDTH
        
        self.rect = self.visual_rect
        self.collision_rect.x = self.visual_rect.x + self.collide_offset_x
        self.collision_rect.y = self.visual_rect.y + self.collide_offset_y
        
        if self.attack_cooldown > 0:
            self.state = 'attack_left' if not self.facing_right else 'attack_right'
        else:
            self.state = 'look_left' if not self.facing_right else 'look_right'
        
        self.update_animation()
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            if self.sound_manager:
                self.sound_manager.play_boss_death()
            self.kill()
        else:
            self.knockback_timer = 8
            self.knockback_direction = -self.direction

    def get_damage_color(self):
        if self.is_flashing:
            return COLORS['BLACK']
        return None
    
    def draw_health_bar(self, screen, camera):
        bar_width = 400
        bar_height = 25
        bar_x = SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = 20
        
        pygame.draw.rect(screen, COLORS['RED'], (bar_x, bar_y, bar_width, bar_height))
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, COLORS['GREEN'], (bar_x, bar_y, bar_width * health_ratio, bar_height))
        pygame.draw.rect(screen, COLORS['WHITE'], (bar_x, bar_y, bar_width, bar_height), 2)
        
        font = pygame.font.Font(None, 24)
        phase_text = font.render(f"ФАЗА {self.phase}", True, COLORS['YELLOW'])
        screen.blit(phase_text, (bar_x + bar_width // 2 - phase_text.get_width() // 2, bar_y + bar_height + 5))