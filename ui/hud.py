import pygame
from settings import *

class HUD:
    def __init__(self, player, level_loader):
        self.player = player
        self.level_loader = level_loader
        self.font = pygame.font.Font(None, 36)
    def draw(self, screen, level_num):
        health_bar_width = 200
        health_bar_height = 20
        max_health = DIFFICULTY[self.level_loader.difficulty]['player_health']
        health_ratio = self.player.health / max_health
        health_bar_fill = health_bar_width * health_ratio
        pygame.draw.rect(screen, COLORS['RED'], (10, 130, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, COLORS['GREEN'], (10, 130, health_bar_fill, health_bar_height))
        pygame.draw.rect(screen, COLORS['WHITE'], (10, 130, health_bar_width, health_bar_height), 2)
        health_text = self.font.render(f"Здоровье", True, COLORS['WHITE'])
        screen.blit(health_text, (10, 105))
        lives_text = self.font.render(f"Жизни: {self.player.health}", True, COLORS['WHITE'])
        screen.blit(lives_text, (10, 160))
        level_text = self.font.render(f"Уровень {level_num}", True, COLORS['WHITE'])
        screen.blit(level_text, (10, 10))
        total_items = self.level_loader.get_total_items(level_num)
        items_text = self.font.render(f"Компьютеры: {len(self.player.collected_items)}/{total_items}", True, COLORS['WHITE'])
        screen.blit(items_text, (10, 50))
        if self.player.collected_items:
            pc_icon = pygame.transform.scale(self.player.collected_items[0].image, (20, 20))
            screen.blit(pc_icon, (180, 50))