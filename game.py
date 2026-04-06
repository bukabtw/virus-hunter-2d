import pygame, sys
from settings import *
from entities.player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Virus Hunter")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

    def start_level(self):
        player = Player(100, SCREEN_HEIGHT - 150)
        platforms = [pygame.Rect(0, SCREEN_HEIGHT-50, SCREEN_WIDTH, 50)]
        all_sprites = pygame.sprite.Group(player)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT: player.move_left()
                    if event.key == pygame.K_RIGHT: player.move_right()
                    if event.key == pygame.K_SPACE: player.jump()
                    if event.key == pygame.K_ESCAPE: running = False
                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT): player.stop()

            player.update(platforms)

            self.screen.fill(COLORS['DARK_GREEN'])
            for p in platforms:
                pygame.draw.rect(self.screen, COLORS['GREEN'], p)
            all_sprites.draw(self.screen)

            self.screen.blit(self.font.render("Уровень 1", True, COLORS['WHITE']), (10,10))
            pygame.display.flip()
            self.clock.tick(FPS)

        self.__init__()
        from ui.menu import Menu
        Menu(self).run()

    def run(self):
        from ui.menu import Menu
        Menu(self).run()