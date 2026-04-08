import pygame
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_CONFIG
from entities.platform import Platform

class LevelLoader:
    def __init__(self):
        self.levels = {}
        self._create_levels()

    def _create_levels(self):
        for level_num in range(1, 4):
            level_module = __import__(f"levels.level_{level_num}", fromlist=["get_level"])
            level_data = level_module.get_level()
            
            tile_scale = TILE_CONFIG[level_num]['tile_scale']
            default_type = TILE_CONFIG[level_num]['default_type']
            
            platforms = []
            for p in level_data['platforms']:
                platforms.append(Platform(
                    p.x, p.y, p.width, p.height,
                    platform_type=default_type,
                    tile_scale=tile_scale
                ))
            
            self.levels[level_num] = {
                'platforms': platforms,
                'items': level_data['items'],
                'enemies': level_data['enemies'],
                'exit': level_data['exit'],
                'boss': level_data.get('boss')
            }

    def get_level(self, level_num):
        return self.levels.get(level_num, self.levels[1])

    def get_total_items(self, level_num):
        level = self.levels.get(level_num, self.levels[1])
        return len(level['items'])