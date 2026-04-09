import pygame, sys
from settings import *
import os

class Button:
    def __init__(self, x, y, w, h, text, color, hover, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover = hover
        self.action = action
        self.hovered = False

    def handle(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            if self.action:
                self.action()

    def draw(self, screen, font):
        color = self.hover if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        text_surf = font.render(self.text, True, COLORS['WHITE'])
        if text_surf.get_width() > self.rect.width - 20:
            smaller_font = pygame.font.Font(None, font.get_height() - 4)
            text_surf = smaller_font.render(self.text, True, COLORS['WHITE'])
        screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, initial_val, label, bg_color, handle_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.bg_color = bg_color
        self.handle_color = handle_color
        self.dragging = False
        
    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            rel_x = max(0, min(self.rect.width, event.pos[0] - self.rect.x))
            self.value = self.min_val + (rel_x / self.rect.width) * (self.max_val - self.min_val)
            return True
        return False
    
    def draw(self, screen, font):
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=5)
        
        fill_width = int((self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(screen, self.handle_color, fill_rect, border_radius=5)
        
        handle_x = self.rect.x + fill_width - 5
        pygame.draw.circle(screen, COLORS['WHITE'], (handle_x, self.rect.centery), 8)
        
        label_text = font.render(f"{self.label}: {int(self.value * 100)}%", True, COLORS['WHITE'])
        screen.blit(label_text, (self.rect.x, self.rect.y - 25))

class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 64)
        self.difficulty = 1
        self.buttons = []
        self.sliders = []
        self._create_buttons()
        self.background_image = None
        self.load_background()

    def load_background(self):
        bg_path = os.path.join(SPRITES_PATH, 'main_menu.png')
        if os.path.exists(bg_path):
            try:
                loaded_image = pygame.image.load(bg_path).convert()
                self.background_image = pygame.transform.scale(loaded_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except:
                pass

    def _create_buttons(self):
        button_positions = [
            (920, 400),
            (920, 445),
            (920, 490),
        ]
        
        button_width = 400
        button_height = 50
        
        self.buttons = []
        for i, (x, y) in enumerate(button_positions):
            if i == 0:
                action = self.start
                text = "СТАРТ"
            elif i == 1:
                action = self.settings
                text = "НАСТРОЙКИ"
            else:
                action = self.quit
                text = "ВЫХОД"
            
            scaled_x = int(x * SCREEN_WIDTH / 1920)
            scaled_y = int(y * SCREEN_HEIGHT / 1080)
            
            btn = Button(
                scaled_x - button_width//2, scaled_y,
                button_width, button_height, text,
                COLORS['PURPLE'], (84, 2, 84), action
            )
            self.buttons.append(btn)

    def settings(self):
        self.settings_running = True
        font_small = pygame.font.Font(None, 28)
        BG_W, BG_H = 1920, 1080

        title_pos = (920, 310)
        slider_music_pos = (920, 400)
        slider_sfx_pos = (920, 460)
        difficulty_pos = (920, 495)
        back_pos = (920, 540)
        
        title_x = int(title_pos[0] * SCREEN_WIDTH / BG_W)
        title_y = int(title_pos[1] * SCREEN_HEIGHT / BG_H)
        slider_music_x = int(slider_music_pos[0] * SCREEN_WIDTH / BG_W)
        slider_music_y = int(slider_music_pos[1] * SCREEN_HEIGHT / BG_H)
        slider_sfx_x = int(slider_sfx_pos[0] * SCREEN_WIDTH / BG_W)
        slider_sfx_y = int(slider_sfx_pos[1] * SCREEN_HEIGHT / BG_H)
        difficulty_x = int(difficulty_pos[0] * SCREEN_WIDTH / BG_W)
        difficulty_y = int(difficulty_pos[1] * SCREEN_HEIGHT / BG_H)
        back_x = int(back_pos[0] * SCREEN_WIDTH / BG_W)
        back_y = int(back_pos[1] * SCREEN_HEIGHT / BG_H)

        self.sliders = []
        
        music_slider = Slider(
            slider_music_x - 150, slider_music_y, 300, 12,
            0.0, 1.0, self.game.sound_manager.music_volume, "МУЗЫКА",
            COLORS['GRAY'], COLORS['PURPLE']
        )
        sfx_slider = Slider(
            slider_sfx_x - 150, slider_sfx_y, 300, 12,
            0.0, 1.0, self.game.sound_manager.sfx_volume, "ЭФФЕКТЫ",
            COLORS['GRAY'], COLORS['PURPLE']
        )
        self.sliders = [music_slider, sfx_slider]
        
        clock = pygame.time.Clock()
        
        while self.settings_running:
            if self.background_image:
                bg_scaled = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.screen.blit(bg_scaled, (0, 0))
            else:
                self.screen.fill(COLORS['DARK_GREEN'])
            
            title = self.title_font.render("НАСТРОЙКИ", True, COLORS['PURPLE'])
            self.screen.blit(title, (title_x - title.get_width()//2, title_y))
            
            mouse_pos = pygame.mouse.get_pos()
            click = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
                for slider in self.sliders:
                    if slider.handle(event):
                        if slider.label == "МУЗЫКА":
                            self.game.sound_manager.set_music_volume(slider.value)
                        else:
                            self.game.sound_manager.set_volume(slider.value)
            
            diff_rect = pygame.Rect(difficulty_x - 150, difficulty_y, 300, 50)
            back_rect = pygame.Rect(back_x - 150, back_y, 300, 50)
            
            diff_color = COLORS['PURPLE'] if diff_rect.collidepoint(mouse_pos) else (84, 2, 84)
            back_color = COLORS['PURPLE'] if back_rect.collidepoint(mouse_pos) else (84, 2, 84)
            
            pygame.draw.rect(self.screen, diff_color, diff_rect, border_radius=10)
            pygame.draw.rect(self.screen, back_color, back_rect, border_radius=10)
            
            diff_text = font_small.render(f"СЛОЖНОСТЬ: {DIFFICULTY[self.difficulty]['name'].upper()}", True, COLORS['WHITE'])
            back_text = font_small.render("НАЗАД", True, COLORS['WHITE'])
            
            self.screen.blit(diff_text, diff_text.get_rect(center=diff_rect.center))
            self.screen.blit(back_text, back_text.get_rect(center=back_rect.center))
            
            for slider in self.sliders:
                slider.draw(self.screen, font_small)
            
            pygame.display.flip()
            
            if click:
                if diff_rect.collidepoint(mouse_pos):
                    self.difficulty = (self.difficulty % 3) + 1
                elif back_rect.collidepoint(mouse_pos):
                    self.settings_running = False
            
            clock.tick(60)

    def start(self):
        self.game.difficulty = self.difficulty
        self.running = False

    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        self.game.sound_manager.play_music('menu')
        clock = pygame.time.Clock()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                for btn in self.buttons:
                    btn.handle(event)
            
            if self.background_image:
                if self.background_image.get_size() != (SCREEN_WIDTH, SCREEN_HEIGHT):
                    self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.screen.blit(self.background_image, (0, 0))
            else:
                self.screen.fill(COLORS['DARK_GREEN'])
            
            title_x = int(920 * SCREEN_WIDTH / 1920)
            title_y = int(310 * SCREEN_HEIGHT / 1080)
            
            title = self.title_font.render("VIRUS HUNTER", True, COLORS['PURPLE'])
            self.screen.blit(title, (title_x - title.get_width()//2, title_y))
            
            for btn in self.buttons:
                btn.draw(self.screen, self.font)
            
            pygame.display.flip()
            clock.tick(60)
        