import pygame
import sys
import os
from settings import *
from settings import ASSETS_PATH
from entities.player import Player
from entities.enemy import Enemy
from entities.item import Item
from entities.projectile import Projectile
from levels.level_loader import LevelLoader
from core.camera import Camera
from core.game_state import GameState 

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Virus Hunter")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.level_sounds = {}
        self.load_level_sounds()
        self.running = False
        self.level_num = 1
        self.difficulty = 1
        self.state = GameState.MENU
    
    def load_level_sounds(self):
        for i in range(1, 4):
            sound_path = os.path.join(SOUNDS_PATH, f"level_{i}.wav")
            if os.path.exists(sound_path):
                try:
                    self.level_sounds[i] = pygame.mixer.Sound(sound_path)
                except pygame.error as e:
                    print(f"Ошибка загрузки саундтрека уровня {i}: {e}")
            else:
                print(f"Файл саундтрека уровня {i} не найден: {sound_path}")

    def load_background(self, level_num):
        bg_path = os.path.join(ASSETS_PATH, f"themes/lvl{level_num}.png")
        try:
            bg = pygame.image.load(bg_path).convert()
            bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            return bg
        except Exception as e:
            print(f"Не удалось загрузить фон для уровня {level_num}: {e}")
            return None

    def start_level(self, level_num=1, difficulty=1):
        self.level_num = level_num
        self.difficulty = difficulty
        self.state = GameState.PLAYING
        self._init_level()
        self.running = True
        
        while self.running:
            dt = self.clock.tick(FPS) / 16.0
            self._handle_events()
            self._update(dt)
            self._draw()
        
        self._cleanup()

    def _init_level(self):
        for sound in self.level_sounds.values():
            sound.stop()
        
        if self.level_num in self.level_sounds:
            self.level_sounds[self.level_num].play(-1)

        self.level_loader = LevelLoader()
        self.level_data = self.level_loader.get_level(self.level_num)
        
        self.player = Player(100, SCREEN_HEIGHT - 150)
        self.all_sprites = pygame.sprite.Group(self.player)
        self.enemies = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.background = self.load_background(self.level_num)

        enemy_speed = DIFFICULTY[self.difficulty]['enemy_speed']
        for ex, ey in self.level_data['enemies']:
            enemy = Enemy(ex, ey, speed=enemy_speed)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
        
        for ix, iy in self.level_data['items']:
            item = Item(ix, iy)
            self.items.add(item)
            self.all_sprites.add(item)
        
        self.boss = None
        if self.level_data.get('boss'):
            from entities.boss import Boss
            bx, by = self.level_data['boss']
            self.boss = Boss(bx, by)
            self.enemies.add(self.boss)
            self.all_sprites.add(self.boss)
        
        self.platforms = self.level_data['platforms']
        self.last_time = pygame.time.get_ticks()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.player.move_left()
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.player.move_right()
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
            
            if event.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()
                moving_left = keys[pygame.K_a] or keys[pygame.K_LEFT]
                moving_right = keys[pygame.K_d] or keys[pygame.K_RIGHT]
                if not moving_left and not moving_right:
                    self.player.stop()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                world_x = mouse_x - self.camera.camera.x
                world_y = mouse_y - self.camera.camera.y
                proj = self.player.attack(world_x, world_y)
                if proj:
                    self.projectiles.add(proj)
                    self.all_sprites.add(proj)

    def _update(self, dt):
        if self.state != GameState.PLAYING:
            return
        
        current_time = pygame.time.get_ticks()
        
        self.player.update(self.platforms)
        self.enemies.update(self.platforms, current_time, self.enemies, self.all_sprites, self.player)
        self.projectiles.update(self.player)
        
        self._check_projectile_hits()
        self._check_item_collection()
        self._check_player_damage()
        self._check_level_transition(current_time)

    def _check_projectile_hits(self):
        for proj in self.projectiles:
            hit_enemies = pygame.sprite.spritecollide(proj, self.enemies, False)
            for enemy in hit_enemies:
                if enemy != proj.owner and not proj.has_hit:
                    proj.hit()
                    damage = getattr(proj, 'damage', 5)
                    enemy.take_damage(damage)
                    break

    def _check_item_collection(self):
        collected_items = pygame.sprite.spritecollide(self.player, self.items, True)
        for item in collected_items:
            self.player.collected_items.append(item)
            self.all_sprites.remove(item)

    def _check_player_damage(self):
        hit_enemies = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in hit_enemies:
            if self.player.invincible_timer <= 0:
                self.player.take_damage(1)
                if hasattr(enemy, 'knockback_timer'):
                    enemy.knockback_timer = 10
                    enemy.knockback_direction = -enemy.direction if enemy.direction else -1

    def _check_level_transition(self, current_time):
        if self.level_data.get('exit'):
            exit_rect = pygame.Rect(*self.level_data['exit'], 50, 50)
            if self.player.rect.colliderect(exit_rect):
                self._next_level()
                return
        
        if self.boss and self.boss.health <= 0:
            self._next_level()
            return
        
        if self.player.health <= 0:
            self.running = False
            self.state = GameState.GAME_OVER
            return

    def _next_level(self):
        self.running = False
        if self.level_num < 3:
            self.start_level(self.level_num + 1, difficulty=self.difficulty)
        else:
            self.state = GameState.VICTORY
            self.running = False

    def _draw(self):
        self.camera.update(self.player)
        self.player.camera_x = self.camera.camera.x
        self.player.camera_y = self.camera.camera.y

        if self.background:
            bg_x = (self.camera.camera.x // 2) % SCREEN_WIDTH
            self.screen.blit(self.background, (bg_x, 0))
            self.screen.blit(self.background, (bg_x - SCREEN_WIDTH, 0))
        else:
            self.screen.fill(COLORS['DARK_GREEN'])
        
        for p in self.platforms:
            if hasattr(p, 'image') and p.image:
                self.screen.blit(p.image, self.camera.apply(p))
            else:
                pygame.draw.rect(self.screen, COLORS['GREEN'], self.camera.apply_rect(p))
        
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        
        if self.level_data.get('exit'):
            exit_rect = pygame.Rect(*self.level_data['exit'], 50, 50)
            pygame.draw.rect(self.screen, COLORS['YELLOW'], self.camera.apply_rect(exit_rect))
        
        self._draw_hud()
        
        if self.state == GameState.PAUSED:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(COLORS['BLACK'])
            self.screen.blit(overlay, (0, 0))
            pause_text = self.font.render("ПАУЗА", True, COLORS['WHITE'])
            self.screen.blit(pause_text, (SCREEN_WIDTH//2 - pause_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
            hint_text = self.font.render("Нажмите ESC для продолжения", True, COLORS['YELLOW'])
            self.screen.blit(hint_text, (SCREEN_WIDTH//2 - hint_text.get_width()//2, SCREEN_HEIGHT//2 + 20))
        
        pygame.display.flip()

    def _draw_hud(self):
        total_items = self.level_loader.get_total_items(self.level_num)
        self.screen.blit(self.font.render(f"Уровень {self.level_num}", True, COLORS['WHITE']), (10, 10))
        self.screen.blit(self.font.render(f"Компьютеры: {len(self.player.collected_items)}/{total_items}", True, COLORS['WHITE']), (10, 50))
        self.screen.blit(self.font.render(f"Здоровье: {self.player.health}", True, COLORS['WHITE']), (10, 90))

    def _cleanup(self):
        if self.level_num in self.level_sounds:
            self.level_sounds[self.level_num].stop()

    def show_victory_screen(self):
        for sound in self.level_sounds.values():
            sound.stop()
            
        self.screen.fill(COLORS['BLACK'])
        title = self.font.render("ПОБЕДА!", True, COLORS['GREEN'])
        subtitle = self.font.render("Вы победили финального босса!", True, COLORS['WHITE'])
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, SCREEN_HEIGHT//2))
        pygame.display.flip()
        pygame.time.delay(3000)
    
    def show_game_over_screen(self):
        for sound in self.level_sounds.values():
            sound.stop()
            
        self.screen.fill(COLORS['BLACK'])
        title = self.font.render("ИГРА ОКОНЧЕНА", True, COLORS['RED'])
        subtitle = self.font.render("Нажмите любую клавишу...", True, COLORS['WHITE'])
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, SCREEN_HEIGHT//2))
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False
    
    def run(self):
        from ui.menu import Menu
        
        while True:
            if self.state == GameState.MENU:
                menu = Menu(self)
                menu.run()
                self.state = GameState.PLAYING
                self.start_level(level_num=1, difficulty=self.difficulty)
            
            elif self.state == GameState.PLAYING:
                pass
            
            elif self.state == GameState.PAUSED:
                pygame.time.wait(100)
            
            elif self.state == GameState.GAME_OVER:
                self.show_game_over_screen()
                self.state = GameState.MENU
            
            elif self.state == GameState.VICTORY:
                self.show_victory_screen()
                self.state = GameState.MENU