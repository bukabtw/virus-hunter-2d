import pygame
import sys
from settings import *
from entities.player import Player
from entities.enemy import Enemy
from entities.item import Item
from entities.projectile import Projectile
from levels.level_loader import LevelLoader
from core.camera import Camera

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Virus Hunter")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.level_sounds = {}
        self.load_level_sounds()
    
    def load_level_sounds(self):
        for i in range(1, 4):
            sound_path = os.path.join(SOUNDS_PATH, f"level_{i}.wav")
            if os.path.exists(sound_path):
                try:
                    self.level_sounds[i] = pygame.mixer.Sound(sound_path)
                    print(f"Загружен саундтрек для уровня {i}")
                except pygame.error as e:
                    print(f"Ошибка загрузки саундтрека уровня {i}: {e}")
            else:
                print(f"Файл саундтрека уровня {i} не найден: {sound_path}")
                try:
                    from pygame.sndarray import array as sound_array
                    silent_samples = sound_array(array([[[0, 0]] * 22050], dtype='int16'))
                    self.level_sounds[i] = pygame.sndarray.make_sound(silent_samples)
                except:
                    pass
    
    def start_level(self, level_num=1, difficulty=1):
        if hasattr(self, 'menu_sound') and self.menu_sound:
            self.menu_sound.stop()
        
        for sound in self.level_sounds.values():
            sound.stop()
        
        if level_num in self.level_sounds:
            self.level_sounds[level_num].play(-1)
            print(f"Запущен саундтрек уровня {level_num}")

        level_loader = LevelLoader()
        level_data = level_loader.get_level(level_num)
        player = Player(100, SCREEN_HEIGHT - 150)
        all_sprites = pygame.sprite.Group(player)
        enemies = pygame.sprite.Group()
        items = pygame.sprite.Group()
        projectiles = pygame.sprite.Group()
        camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        enemy_speed = DIFFICULTY[difficulty]['enemy_speed']
        for ex, ey in level_data['enemies']:
            enemy = Enemy(ex, ey, speed=enemy_speed)
            enemies.add(enemy)
            all_sprites.add(enemy)
        for ix, iy in level_data['items']:
            item = Item(ix, iy)
            items.add(item)
            all_sprites.add(item)
        boss = None
        if 'boss' in level_data:
            from entities.boss import Boss
            bx, by = level_data['boss']
            boss = Boss(bx, by)
            enemies.add(boss)
            all_sprites.add(boss)
        platforms = level_data['platforms']
        running = True
        clock = pygame.time.Clock()
        last_time = pygame.time.get_ticks()
        while running:
            current_time = pygame.time.get_ticks()
            dt = (current_time - last_time) / 16.0
            last_time = current_time
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        player.move_left()
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        player.move_right()
                    if event.key == pygame.K_SPACE:
                        player.jump()
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.KEYUP:
                    keys = pygame.key.get_pressed()
                    moving_left = keys[pygame.K_a] or keys[pygame.K_LEFT]
                    moving_right = keys[pygame.K_d] or keys[pygame.K_RIGHT]
                    if not moving_left and not moving_right:
                        player.stop()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    proj = player.attack()
                    if proj:
                        projectiles.add(proj)
                        all_sprites.add(proj)
            player.update(platforms)
            enemies.update(platforms, current_time, enemies, all_sprites)
            projectiles.update(player)
            health_bar_width = 200
            health_bar_height = 20
            health_ratio = player.health / 5
            health_bar_fill = health_bar_width * health_ratio
            pygame.draw.rect(self.screen, COLORS['RED'], (10, 130, health_bar_width, health_bar_height))
            pygame.draw.rect(self.screen, COLORS['GREEN'], (10, 130, health_bar_fill, health_bar_height))
            pygame.draw.rect(self.screen, COLORS['WHITE'], (10, 130, health_bar_width, health_bar_height), 2)
            health_text = self.font.render(f"Здоровье", True, COLORS['WHITE'])
            self.screen.blit(health_text, (10, 105))
            for proj in projectiles:
                hit_enemies = pygame.sprite.spritecollide(proj, enemies, False)
                for enemy in hit_enemies:
                    if enemy != proj.owner:
                        enemy.take_damage(10)
            hit_enemies = pygame.sprite.spritecollide(player, enemies, False)
            for enemy in hit_enemies:
                player.take_damage(1)
            collected_items = pygame.sprite.spritecollide(player, items, True)
            for item in collected_items:
                player.collected_items.append(item)
                all_sprites.remove(item)
            next_level = False
            if level_data['exit']:
                exit_rect = pygame.Rect(*level_data['exit'], 50, 50)
                if player.rect.colliderect(exit_rect):
                    next_level = True
            if boss and boss.health <= 0:
                next_level = True
            if player.health <= 0:
                running = False
                self.show_game_over_screen()
            if next_level:
                running = False
                if level_num < 3:
                    self.start_level(level_num + 1, difficulty=difficulty)
                else:
                    self.show_victory_screen()
            camera.update(player)
            self.screen.fill(COLORS['DARK_GREEN'])
            for p in platforms:
                pygame.draw.rect(self.screen, COLORS['GREEN'], camera.apply_rect(p))
            for sprite in all_sprites:
                self.screen.blit(sprite.image, camera.apply(sprite))
            if level_data['exit']:
                exit_rect = pygame.Rect(*level_data['exit'], 50, 50)
                pygame.draw.rect(self.screen, COLORS['YELLOW'], camera.apply_rect(exit_rect))
            total_items = level_loader.get_total_items(level_num)
            self.screen.blit(self.font.render(f"Уровень {level_num}", True, COLORS['WHITE']), (10, 10))
            self.screen.blit(self.font.render(f"Компьютеры: {len(player.collected_items)}/{total_items}", True, COLORS['WHITE']), (10, 50))
            self.screen.blit(self.font.render(f"Здоровье: {player.health}", True, COLORS['WHITE']), (10, 90))
            pygame.display.flip()
            clock.tick(FPS)
        if level_num in self.level_sounds:
            self.level_sounds[level_num].stop()
        self.__init__()
        from ui.menu import Menu
        Menu(self).run()
    
    def show_victory_screen(self):
        self.screen.fill(COLORS['BLACK'])
        title = self.font.render("ПОБЕДА!", True, COLORS['GREEN'])
        subtitle = self.font.render("Вы победили финального босса!", True, COLORS['WHITE'])
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, SCREEN_HEIGHT//2))
        pygame.display.flip()
        pygame.time.delay(3000)
        self.run()
    
    def show_game_over_screen(self):
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
        self.run()
    
    def run(self):
        from ui.menu import Menu
        Menu(self).run()