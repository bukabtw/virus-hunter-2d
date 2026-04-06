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
        self.buttons = []
        self._create_buttons()

    def _create_buttons(self):
        cx, cy = SCREEN_WIDTH//2, SCREEN_HEIGHT//2
        self.buttons = [
            Button(cx-100, cy-60, 200, 60, "СТАРТ", COLORS['GREEN'], (0,150,0), self.start),
            Button(cx-100, cy+20, 200, 60, "ВЫХОД", COLORS['RED'], (150,0,0), self.quit)
        ]

    def start(self):
        self.running = False
        self.game.start_level()

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