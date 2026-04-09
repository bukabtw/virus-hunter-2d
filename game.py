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
from core.sound_manager import SoundManager
from random import random

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Virus Hunter")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.running = False
        self.level_num = 1
        self.difficulty = 1
        self.state = GameState.MENU
        self.sound_manager = SoundManager()
        self.debug_mode = True
        self._load_all_sounds()
        self._load_level_music()
    
    def _load_all_sounds(self):
        self.sound_manager.load_sound('player_attack', SOUND_PLAYER_ATTACK)
        self.sound_manager.load_sound('player_jump', SOUND_PLAYER_JUMP)
        self.sound_manager.load_sound('player_hit', SOUND_PLAYER_HIT)
        self.sound_manager.load_sound('enemy_attack', SOUND_ENEMY_ATTACK)
        self.sound_manager.load_sound('enemy_hit', SOUND_ENEMY_HIT)
        self.sound_manager.load_sound('boss_attack', SOUND_BOSS_ATTACK)
        self.sound_manager.load_sound('boss_hit', SOUND_BOSS_HIT)
        self.sound_manager.load_sound('boss_spawn', SOUND_BOSS_SPAWN)
        self.sound_manager.load_sound('boss_roar', SOUND_BOSS_ROAR)
        self.sound_manager.load_sound('boss_death', SOUND_BOSS_DEATH)
        self.sound_manager.load_sound('collect', SOUND_COLLECT)
        self.sound_manager.load_sound('victory', SOUND_VICTORY)
        self.sound_manager.load_sound('game_over', SOUND_GAME_OVER)
        self.sound_manager.load_sound('level_up', SOUND_LEVEL_UP)
        self.sound_manager.load_music('menu', SOUND_MENU)

    def _load_level_music(self):
        for i in range(1, 4):
            sound_path = os.path.join(SOUNDS_PATH, f"level_{i}.wav")
            if os.path.exists(sound_path):
                self.sound_manager.load_music(f"level_{i}", sound_path)

    def load_background(self, level_num):
        bg_path = os.path.join(ASSETS_PATH, f"themes/lvl{level_num}.png")
        try:
            bg = pygame.image.load(bg_path).convert()
            bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            return bg
        except:
            bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            bg.fill(COLORS['DARK_GREEN'])
            return bg

    def start_level(self, level_num=1, difficulty=1):
        self.level_num = level_num
        self.difficulty = difficulty
        self.state = GameState.PLAYING
        self._init_level()
        self.running = True
        self._draw()
        while self.running:
            dt = self.clock.tick(FPS) / 16.0
            self._handle_events()
            self._update(dt)
            self._draw()
        self._cleanup()

    def _init_level(self):
        self.sound_manager.play_music(f"level_{self.level_num}")
        self.level_loader = LevelLoader()
        self.level_data = self.level_loader.get_level(self.level_num)
        self.player = Player(100, SCREEN_HEIGHT - 150)
        self.all_sprites = pygame.sprite.Group(self.player)
        self.enemies = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera.update(self.player)
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
            self.boss.spawn_enabled = (self.level_num == 3)
            self.enemies.add(self.boss)
            self.all_sprites.add(self.boss)
        self.platforms = self.level_data['platforms']
        self.last_time = pygame.time.get_ticks()
        for enemy in self.enemies:
            enemy.sound_manager = self.sound_manager

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
                    self.sound_manager.play_jump()
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
                    if hasattr(enemy, 'is_boss') and enemy.is_boss:
                        self.sound_manager.play_hit('boss')
                        if enemy.health <= 0:
                            self.sound_manager.play_boss_death()
                    else:
                        self.sound_manager.play_hit('enemy')
                    break

    def _check_item_collection(self):
        collected_items = pygame.sprite.spritecollide(self.player, self.items, True)
        for item in collected_items:
            self.player.collected_items.append(item)
            self.all_sprites.remove(item)
            self.sound_manager.play_collect()

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
            self.sound_manager.play_level_up()
            self.start_level(self.level_num + 1, difficulty=self.difficulty)
        else:
            self.state = GameState.VICTORY
            self.running = False

    def _draw(self):
        self.camera.update(self.player)
        self.player.camera_x = self.camera.camera.x
        self.player.camera_y = self.camera.camera.y
        if self.background:
            if self.background.get_size() != (SCREEN_WIDTH, SCREEN_HEIGHT):
                self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(COLORS['DARK_GREEN'])
        for p in self.platforms:
            if hasattr(p, 'image') and p.image:
                self.screen.blit(p.image, self.camera.apply(p))
            else:
                pygame.draw.rect(self.screen, COLORS['GREEN'], self.camera.apply_rect(p))
        for sprite in self.all_sprites:
            flash_color = None
            if hasattr(sprite, 'get_damage_color'):
                flash_color = sprite.get_damage_color()
            if flash_color:
                colored_image = sprite.image.copy()
                colored_image.fill(flash_color, special_flags=pygame.BLEND_RGB_MULT)
                self.screen.blit(colored_image, self.camera.apply(sprite))
            else:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
        
        # Отрисовка коллизии для отладки
        if self.debug_mode:
            if hasattr(self.player, 'collision_rect'):
                col_rect = self.camera.apply_rect(self.player.collision_rect)
                pygame.draw.rect(self.screen, COLORS['BLUE'], col_rect, 2)
            for enemy in self.enemies:
                if hasattr(enemy, 'collision_rect'):
                    col_rect = self.camera.apply_rect(enemy.collision_rect)
                    pygame.draw.rect(self.screen, COLORS['GREEN'], col_rect, 2)
        
        # Полоска здоровья босса
        if self.boss and self.boss.alive():
            self.boss.draw_health_bar(self.screen, self.camera)
        
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
        self.sound_manager.stop_music()

    def show_pause_menu(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(COLORS['BLACK'])
        self.screen.blit(overlay, (0, 0))
        font = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 36)
        title = font.render("ПАУЗА", True, COLORS['PURPLE'])
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//2 - 150))
        btn_y = SCREEN_HEIGHT//2 - 50
        btn_w = 300
        btn_h = 50
        mouse = pygame.mouse.get_pos()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        resume_rect = pygame.Rect(SCREEN_WIDTH//2 - btn_w//2, btn_y, btn_w, btn_h)
        menu_rect = pygame.Rect(SCREEN_WIDTH//2 - btn_w//2, btn_y + 70, btn_w, btn_h)
        quit_rect = pygame.Rect(SCREEN_WIDTH//2 - btn_w//2, btn_y + 140, btn_w, btn_h)
        resume_color = COLORS['PURPLE'] if resume_rect.collidepoint(mouse) else (84, 2, 84)
        menu_color = COLORS['PURPLE'] if menu_rect.collidepoint(mouse) else (84, 2, 84)
        quit_color = COLORS['PURPLE'] if quit_rect.collidepoint(mouse) else (84, 2, 84)
        pygame.draw.rect(self.screen, resume_color, resume_rect, border_radius=10)
        pygame.draw.rect(self.screen, menu_color, menu_rect, border_radius=10)
        pygame.draw.rect(self.screen, quit_color, quit_rect, border_radius=10)
        resume_text = font_small.render("Продолжить", True, COLORS['WHITE'])
        menu_text = font_small.render("Выйти в меню", True, COLORS['WHITE'])
        quit_text = font_small.render("Выйти из игры", True, COLORS['WHITE'])
        self.screen.blit(resume_text, resume_text.get_rect(center=resume_rect.center))
        self.screen.blit(menu_text, menu_text.get_rect(center=menu_rect.center))
        self.screen.blit(quit_text, quit_text.get_rect(center=quit_rect.center))
        pygame.display.flip()
        if click:
            if resume_rect.collidepoint(mouse):
                self.state = GameState.PLAYING
            elif menu_rect.collidepoint(mouse):
                self.state = GameState.MENU
                self.sound_manager.stop_music()
            elif quit_rect.collidepoint(mouse):
                pygame.quit()
                sys.exit()
        pygame.time.wait(100)

    def show_victory_screen(self):
        self.sound_manager.stop_music()
        self.sound_manager.play_victory()
        waiting = True
        while waiting:
            self.screen.fill(COLORS['BLACK'])
            for _ in range(50):
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
                pygame.draw.circle(self.screen, COLORS['YELLOW'], (x, y), 2)
            title = self.font.render("ПОБЕДА!", True, COLORS['GREEN'])
            subtitle = self.font.render("Вы спасли мир от вирусов!", True, COLORS['WHITE'])
            restart_text = self.font.render("R - Играть заново", True, COLORS['GREEN'])
            menu_text = self.font.render("M - Выйти в меню", True, COLORS['YELLOW'])
            self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//2 - 100))
            self.screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, SCREEN_HEIGHT//2 - 40))
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 20))
            self.screen.blit(menu_text, (SCREEN_WIDTH//2 - menu_text.get_width()//2, SCREEN_HEIGHT//2 + 60))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.start_level(level_num=1, difficulty=self.difficulty)
                        return
                    if event.key == pygame.K_m:
                        self.state = GameState.MENU
                        return
    
    def show_game_over_screen(self):
        self.sound_manager.stop_music()
        self.sound_manager.play_game_over()
        waiting = True
        while waiting:
            self.screen.fill(COLORS['BLACK'])
            title = self.font.render("GAME OVER", True, COLORS['RED'])
            subtitle = self.font.render("Вы проиграли...", True, COLORS['WHITE'])
            restart_text = self.font.render("R - Начать заново", True, COLORS['GREEN'])
            menu_text = self.font.render("M - Выйти в меню", True, COLORS['YELLOW'])
            self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//2 - 100))
            self.screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, SCREEN_HEIGHT//2 - 40))
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 20))
            self.screen.blit(menu_text, (SCREEN_WIDTH//2 - menu_text.get_width()//2, SCREEN_HEIGHT//2 + 60))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.start_level(level_num=1, difficulty=self.difficulty)
                        return
                    if event.key == pygame.K_m:
                        self.state = GameState.MENU
                        return
    
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
                self.show_pause_menu()
            elif self.state == GameState.GAME_OVER:
                self.show_game_over_screen()
            elif self.state == GameState.VICTORY:
                self.show_victory_screen()