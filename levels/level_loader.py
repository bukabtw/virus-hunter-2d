import pygame
import os
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT
from entities.platform import Platform

class LevelLoader:
    def __init__(self):
        self.levels = {}
        self._create_levels()

    def _create_levels(self):
        level_1_path = os.path.join(os.path.dirname(__file__), 'level_1.py')
        if not os.path.exists(level_1_path):
            raise FileNotFoundError(f"Файл уровня 1 не найден: {level_1_path}")

        from levels.level_1 import get_level_1
        platforms_1, items_1, enemies_1, exit_pos_1 = get_level_1()
        platform_list = []
        random.seed(42)
        for p in platforms_1:
            platform_type = 'ram' if random.random() < 0.5 else 'hdd'
            new_width = p.width * 3   # например, растянуть в 3 раза
            new_height = p.height * 3  # растянуть в 2 раза по высоте
            platform_list.append(Platform(p.x, p.y, new_width, new_height, platform_type))
        self.levels[1] = {
            'platforms': platform_list,
            'items': items_1,
            'enemies': enemies_1,
            'exit': exit_pos_1
        }

        platforms_2 = [
            Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50, 'hdd'),
            Platform(200, SCREEN_HEIGHT - 150, 150, 30, 'ram'),
            Platform(400, SCREEN_HEIGHT - 250, 150, 30, 'ram'),
            Platform(600, SCREEN_HEIGHT - 350, 150, 30, 'ram'),
            Platform(800, SCREEN_HEIGHT - 450, 150, 30, 'ram'),
        ]
        items_2 = [
            (250, SCREEN_HEIGHT - 180),
            (450, SCREEN_HEIGHT - 280),
            (650, SCREEN_HEIGHT - 380),
            (850, SCREEN_HEIGHT - 480)
        ]
        enemies_2 = [
            (220, SCREEN_HEIGHT - 180),
            (620, SCREEN_HEIGHT - 380)
        ]
        self.levels[2] = {
            'platforms': platforms_2,
            'items': items_2,
            'enemies': enemies_2,
            'exit': (SCREEN_WIDTH - 100, 100)
        }

        platforms_3 = [
            Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50, 'hdd'),
            Platform(300, SCREEN_HEIGHT - 200, 600, 40, 'hdd'),
            Platform(100, SCREEN_HEIGHT - 350, 150, 30, 'ram'),
            Platform(850, SCREEN_HEIGHT - 350, 150, 30, 'ram'),
        ]
        items_3 = [
            (500, SCREEN_HEIGHT - 230),
            (150, SCREEN_HEIGHT - 380),
            (900, SCREEN_HEIGHT - 380)
        ]
        enemies_3 = []
        self.levels[3] = {
            'platforms': platforms_3,
            'items': items_3,
            'enemies': enemies_3,
            'boss': (500, SCREEN_HEIGHT - 400),
            'exit': None
        }

    def get_level(self, level_num):
        return self.levels.get(level_num, self.levels[1])

    def get_total_items(self, level_num):
        level = self.levels.get(level_num, self.levels[1])
        return len(level['items'])