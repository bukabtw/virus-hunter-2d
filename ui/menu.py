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

class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 64)
        self.difficulty = 1
        self.buttons = []
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
        cx = SCREEN_WIDTH // 2
        cy = SCREEN_HEIGHT // 2
        spacing = 70
        start_y = cy - 120
        button_width = 300
        button_height = 60
        self.buttons = [
            Button(cx - button_width//2, start_y, button_width, button_height, "СТАРТ", COLORS['PURPLE'], (84, 2, 84), self.start),
            Button(cx - button_width//2, start_y + spacing, button_width, button_height, "НАСТРОЙКИ", COLORS['PURPLE'], (84, 2, 84), self.settings),
            Button(cx - button_width//2, start_y + 2 * spacing, button_width, button_height, "ВЫХОД", COLORS['PURPLE'], (84, 2, 84), self.quit)
        ]

    def settings(self):
        self.settings_running = True
        font_small = pygame.font.Font(None, 28)
        while self.settings_running:
            if self.background_image:
                bg_scaled = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.screen.blit(bg_scaled, (0, 0))
            else:
                self.screen.fill(COLORS['DARK_GREEN'])
            title = self.title_font.render("НАСТРОЙКИ", True, COLORS['PURPLE'])
            self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
            opt_y = SCREEN_HEIGHT//2 - 50
            opt_w = 400
            opt_h = 50
            opt_x = SCREEN_WIDTH//2 - opt_w//2
            mouse_pos = pygame.mouse.get_pos()
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
            diff_rect = pygame.Rect(opt_x, opt_y, opt_w, opt_h)
            back_rect = pygame.Rect(opt_x, opt_y + 80, opt_w, opt_h)
            diff_color = COLORS['PURPLE'] if diff_rect.collidepoint(mouse_pos) else (84, 2, 84)
            back_color = COLORS['PURPLE'] if back_rect.collidepoint(mouse_pos) else (84, 2, 84)
            pygame.draw.rect(self.screen, diff_color, diff_rect, border_radius=10)
            pygame.draw.rect(self.screen, back_color, back_rect, border_radius=10)
            diff_text = font_small.render(f"СЛОЖНОСТЬ: {DIFFICULTY[self.difficulty]['name'].upper()}", True, COLORS['WHITE'])
            back_text = font_small.render("НАЗАД", True, COLORS['WHITE'])
            self.screen.blit(diff_text, diff_text.get_rect(center=diff_rect.center))
            self.screen.blit(back_text, back_text.get_rect(center=back_rect.center))
            pygame.display.flip()
            if click:
                if diff_rect.collidepoint(mouse_pos):
                    self.difficulty = (self.difficulty % 3) + 1
                elif back_rect.collidepoint(mouse_pos):
                    self.settings_running = False
            pygame.time.wait(100)

    def start(self):
        self.game.sound_manager.stop_music()
        self.running = False
        self.game.difficulty = self.difficulty
        self.game.start_level(difficulty=self.difficulty)

    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        self.game.sound_manager.play_music('menu')
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
            
            title = self.title_font.render("VIRUS HUNTER", True, COLORS['PURPLE'])
            self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
            for btn in self.buttons:
                btn.draw(self.screen, self.font)
            pygame.display.flip()