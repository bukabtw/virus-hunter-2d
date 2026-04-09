import pygame
import random
from settings import *
from core.animated_entity import AnimatedEntity
from core.damageable import Damageable
from entities.enemy import Enemy

class Boss(AnimatedEntity, Damageable):
    def __init__(self, x, y, spawn_interval=5000):
        animations = {
            'idle': BOSS_ANIMATIONS['idle'],
            'look_left': BOSS_ANIMATIONS['look_left'],
            'look_right': BOSS_ANIMATIONS['look_right'],
            'attack_left': BOSS_ANIMATIONS['attack_left'],
            'attack_right': BOSS_ANIMATIONS['attack_right'],
        }
        
        sprite_path = f"{SPRITES_PATH}/{BOSS_SPRITESHEET}"
        BOSS_SCALE = 3
        super().__init__(x, y, sprite_path, SPRITE_WIDTH, SPRITE_HEIGHT, BOSS_SCALE, animations)
        Damageable.__init__(self, max_health=150, invincible_duration=40)
        
        COLLIDE_W = 90 * BOSS_SCALE
        COLLIDE_H = 100 * BOSS_SCALE
        OFFSET_X = 19 * BOSS_SCALE
        OFFSET_Y = 14 * BOSS_SCALE
        
        self.collide_offset_x = OFFSET_X
        self.collide_offset_y = OFFSET_Y
        
        self.visual_rect = self.rect.copy()
        
        self.collision_rect = pygame.Rect(
            self.visual_rect.x + OFFSET_X,
            self.visual_rect.y + OFFSET_Y,
            COLLIDE_W,
            COLLIDE_H
        )
        
        self.speed = 2.0 * BOSS_SCALE
        self.direction = 1
        self.phase = 1
        self.phase_changed = False
        
        self.spawn_timer = 0
        self.spawn_interval = spawn_interval
        self.attack_cooldown = 0
        self.attack_delay = 60
        self.dash_timer = 0
        self.jump_timer = 0
        
        self.spawn_enabled = True
        self.can_jump = True
        self.arena_bounds = None
        
        self.vel_y = 0
        self.gravity = 0.8
        self.on_ground = False

        self.knockback_timer = 0
        self.knockback_direction = 0
        self.is_boss = True
        self.sound_manager = None
        self.frozen = False
        self.enraged = False 
    
    def set_arena_bounds(self, min_x, max_x, ground_y):
        self.arena_bounds = {'min_x': min_x, 'max_x': max_x, 'ground_y': ground_y}
    
    def check_ground_below(self, platforms):
        test_rect = self.collision_rect.copy()
        test_rect.y += 10
        test_rect.x += self.direction * 30
        
        for p in platforms:
            if test_rect.colliderect(p.rect):
                return True
        return False
    
    def update(self, platforms, current_time, enemies_group, all_sprites_group, player):
        self.update_invincibility()
        
        if self.health <= 100 and self.phase == 1:
            self.phase = 2
            self.phase_changed = True
            self.speed = 3.0
            self.spawn_interval = 4000
            if self.sound_manager:
                self.sound_manager.play_boss_roar()
        elif self.health <= 50 and self.phase == 2:
            self.phase = 3
            self.phase_changed = True
            self.speed = 4.0
            self.spawn_interval = 3000
            self.enraged = True
            if self.sound_manager:
                self.sound_manager.play_boss_roar()
        
        if self.frozen or not player or not player.alive():
            self.rect = self.visual_rect
            self.update_animation()
            return
        
        self.collision_rect.x = self.visual_rect.x + self.collide_offset_x
        self.collision_rect.y = self.visual_rect.y + self.collide_offset_y
        
        if self.knockback_timer > 0:
            self.knockback_timer -= 1
            self.visual_rect.x += self.knockback_direction * 8
            self.collision_rect.x = self.visual_rect.x + self.collide_offset_x
            self.rect = self.visual_rect
            return
        
        self.vel_y += self.gravity
        self.collision_rect.y += self.vel_y
        
        self.on_ground = False
        for p in platforms:
            if self.collision_rect.colliderect(p.rect):
                if self.vel_y > 0:
                    self.collision_rect.bottom = p.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.collision_rect.top = p.rect.bottom
                    self.vel_y = 0
        
        self.visual_rect.y = self.collision_rect.y - self.collide_offset_y

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        if self.on_ground:
            dx = player.visual_rect.centerx - self.visual_rect.centerx
            
            if abs(dx) > 50:
                if dx > 0:
                    self.direction = 1
                    self.facing_right = True
                else:
                    self.direction = -1
                    self.facing_right = False
                
                if self.check_ground_below(platforms):
                    self.visual_rect.x += self.speed * self.direction
                else:
                    if self.can_jump and random.random() < 0.3:
                        self.vel_y = -20
                        self.can_jump = False
                    else:
                        self.direction *= -1
                        self.facing_right = not self.facing_right

            self.collision_rect.x = self.visual_rect.x + self.collide_offset_x
            for p in platforms:
                if self.collision_rect.colliderect(p.rect):
                    if self.direction > 0:
                        self.collision_rect.right = p.rect.left
                    else:
                        self.collision_rect.left = p.rect.right
                    self.direction *= -1
                    self.facing_right = not self.facing_right
                    break
            
            self.visual_rect.x = self.collision_rect.x - self.collide_offset_x
            
            if self.collision_rect.colliderect(player.collision_rect) and self.attack_cooldown == 0:
                self.attack_cooldown = self.attack_delay
                damage = 2 if self.phase == 1 else (3 if self.phase == 2 else 5)
                player.take_damage(damage)
                
                player.knockback_timer = 15
                player.knockback_direction = self.direction
                
                if self.sound_manager:
                    self.sound_manager.play_attack('boss')
            
            if self.phase >= 2 and self.on_ground:
                self.jump_timer += 1
                if self.jump_timer > 120 and abs(dx) < 200:
                    self.vel_y = -25
                    self.jump_timer = 0
                    self.can_jump = True
        
        if self.spawn_enabled and self.phase >= 2:
            if current_time - self.spawn_timer > self.spawn_interval:
                self.spawn_timer = current_time
                count = 2 if self.phase == 3 else 1
                
                for i in range(count):
                    spawn_x = self.visual_rect.centerx + random.randint(-100, 100)
                    spawn_y = self.visual_rect.bottom - 50
                    
                    virus = Enemy(spawn_x, spawn_y, 
                                 speed=3.0 if self.phase == 3 else 2.0,
                                 enemy_type='fast' if self.phase == 3 else 'normal')
                    enemies_group.add(virus)
                    all_sprites_group.add(virus)
                
                if self.sound_manager:
                    self.sound_manager.play_boss_spawn()

        if self.phase == 3:
            self.dash_timer += 1
            if self.dash_timer > 150:
                self.dash_timer = 0
                dash_distance = 200 * self.direction
                self.visual_rect.x += dash_distance
                
                if abs(self.visual_rect.centerx - player.visual_rect.centerx) < 100:
                    player.take_damage(4)
                
                if self.sound_manager:
                    self.sound_manager.play_attack('boss')
        
        if self.arena_bounds:
            if self.visual_rect.left < self.arena_bounds['min_x']:
                self.visual_rect.left = self.arena_bounds['min_x']
                self.direction *= -1
                self.facing_right = not self.facing_right
            if self.visual_rect.right > self.arena_bounds['max_x']:
                self.visual_rect.right = self.arena_bounds['max_x']
                self.direction *= -1
                self.facing_right = not self.facing_right
        else:
            if self.visual_rect.left < 0:
                self.visual_rect.left = 0
                self.direction *= -1
                self.facing_right = not self.facing_right
            if self.visual_rect.right > MAP_WIDTH:
                self.visual_rect.right = MAP_WIDTH
                self.direction *= -1
                self.facing_right = not self.facing_right
        
        self.rect = self.visual_rect
        self.collision_rect.x = self.visual_rect.x + self.collide_offset_x
        self.collision_rect.y = self.visual_rect.y + self.collide_offset_y
        
        if self.attack_cooldown > 0:
            self.state = 'attack_left' if not self.facing_right else 'attack_right'
        else:
            self.state = 'look_left' if not self.facing_right else 'look_right'
        
        self.update_animation()
    
    def take_damage(self, amount):
        if self.invincible_timer <= 0:
            self.health -= amount
            self.invincible_timer = self.invincible_duration
            self._damage_flash_timer = 10
            
            if self.health <= 0:
                if self.sound_manager:
                    self.sound_manager.play_boss_death()
                self.kill()
            else:
                self.knockback_timer = 10
                self.knockback_direction = -self.direction
                if self.sound_manager:
                    self.sound_manager.play_hit('boss')
            return True
        return False

    def get_damage_color(self):
        if self.is_flashing:
            return COLORS['PURPLE'] if self.enraged else COLORS['BLACK']
        return None
    
    def draw_health_bar(self, screen, camera):
        bar_width = 500
        bar_height = 30
        bar_x = SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = 30
        
        pygame.draw.rect(screen, COLORS['BLACK'], (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
        pygame.draw.rect(screen, COLORS['RED'], (bar_x, bar_y, bar_width, bar_height))
        
        health_ratio = self.health / self.max_health
        health_color = COLORS['GREEN'] if not self.enraged else COLORS['ORANGE']
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, bar_width * health_ratio, bar_height))
        
        pygame.draw.rect(screen, COLORS['WHITE'], (bar_x, bar_y, bar_width, bar_height), 3)
        
        font = pygame.font.Font(None, 28)
        name_text = font.render("VIRUS BOSS", True, COLORS['WHITE'])
        screen.blit(name_text, (bar_x, bar_y - 25))
        
        phase_text = font.render(f"ФАЗА {self.phase}/3", True, COLORS['YELLOW'])
        screen.blit(phase_text, (bar_x + bar_width - phase_text.get_width(), bar_y - 25))
        
        hp_text = font.render(f"{self.health}/{self.max_health}", True, COLORS['WHITE'])
        screen.blit(hp_text, (bar_x + bar_width // 2 - hp_text.get_width() // 2, bar_y + bar_height + 5))