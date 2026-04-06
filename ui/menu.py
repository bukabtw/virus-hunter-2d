import pygame, sys
from settings import *

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
            if self.action: self.action()

    def draw(self, screen, font):
        color = self.hover if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        txt = font.render(self.text, True, COLORS['WHITE'])
        screen.blit(txt, txt.get_rect(center=self.rect.center))

class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.running = True
        self.font = pygame.font.Font(None, 48)
        self.title_font = pygame.font.Font(None, 80)
        self.difficulty = 1
        self.buttons = []
        self._create_buttons()
        self.soundtrack = None
        self.load_soundtrack()

    def load_soundtrack(self):
        soundtrack_path = os.path.join(SOUNDS_PATH, 'menu_soundtrack.wav')
        if os.path.exists(soundtrack_path):
            try:
                self.soundtrack = pygame.mixer.Sound(soundtrack_path)
                self.soundtrack.play(-1)
            except pygame.error as e:
                print(f"Ошибка загрузки звука меню: {e}")
        else:
            print(f"Файл меню-саундтрека не найден: {soundtrack_path}")

    def _create_buttons(self):
        cx, cy = SCREEN_WIDTH//2, SCREEN_HEIGHT//2
        spacing = 80
        start_y = cy - 150
        button_width = BUTTON_WIDTH
        button_height = BUTTON_HEIGHT
        self.buttons = [
            Button(cx - button_width//2, start_y, button_width, button_height, "Старт", COLORS['GREEN'], (0,150,0), self.start),
            Button(cx - button_width//2, start_y + spacing, button_width, button_height, "Настройки", COLORS['GRAY'], (100,100,100), self.settings),
            Button(cx - button_width//2, start_y + 2 * spacing, button_width, button_height, "Выход", COLORS['RED'], (150,0,0), self.quit)
        ]
        
    def settings(self):
        self.settings_running = True
        font_small = pygame.font.Font(None, 36)
        
        options = [
            f"РАЗМЕР: {SCREEN_WIDTH}x{SCREEN_HEIGHT}",
            f"СЛОЖНОСТЬ: {DIFFICULTY[self.difficulty]['name'].upper()}",
            "НАЗАД"
        ]
        
        while self.settings_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, option in enumerate(options):
                        y = SCREEN_HEIGHT//2 - 50 + i * 60
                        option_rect = pygame.Rect(SCREEN_WIDTH//2 - 140, y, 280, 50)
                        if option_rect.collidepoint(mouse_pos):
                            if i == 0:
                                print("Изменение размера экрана")
                            elif i == 1:
                                self.difficulty = (self.difficulty % 3) + 1
                                options[i] = f"СЛОЖНОСТЬ: {DIFFICULTY[self.difficulty]['name'].upper()}"
                            elif i == 2:
                                self.settings_running = False

            self.screen.fill(COLORS['DARK_GREEN'])
            
            title = self.title_font.render("НАСТРОЙКИ", True, COLORS['GREEN'])
            self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
            
            for i, option in enumerate(options):
                y = SCREEN_HEIGHT//2 - 50 + i * 60
                color = COLORS['WHITE']
                if pygame.Rect(SCREEN_WIDTH//2 - 140, y, 280, 50).collidepoint(pygame.mouse.get_pos()):
                    color = COLORS['YELLOW']
                pygame.draw.rect(self.screen, COLORS['GRAY'], (SCREEN_WIDTH//2 - 140, y, 280, 50), border_radius=10)
                txt = font_small.render(option, True, color)
                self.screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH//2, y + 25)))
            
            pygame.display.flip()

    def change_difficulty(self):
        self.difficulty = (self.difficulty % 3) + 1
        self._create_buttons()

    def start(self):
        self.running = False
        self.game.start_level(difficulty=self.difficulty)

    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.quit()
                for btn in self.buttons: btn.handle(event)

            self.screen.fill(COLORS['DARK_GREEN'])
            title = self.title_font.render("VIRUS HUNTER", True, COLORS['GREEN'])
            self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))

            for btn in self.buttons: btn.draw(self.screen, self.font)
            pygame.display.flip()