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
            
            level_config = TILE_CONFIG[level_num]
            default_type = level_config['default_type']
            tile_w, tile_h = level_config['tile_size']
            
            platforms = []
            for p in level_data['platforms']:
                width = ((p.width + tile_w - 1) // tile_w) * tile_w
                height = ((p.height + tile_h - 1) // tile_h) * tile_h
                
                width = max(width, tile_w)
                height = max(height, tile_h)
                
                platform = Platform(p.x, p.y, width, height, 
                                  platform_type=default_type)
                platforms.append(platform)
            
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