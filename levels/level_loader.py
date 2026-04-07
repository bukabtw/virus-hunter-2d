import pygame
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_CONFIG
from entities.platform import Platform

class LevelLoader:
    def __init__(self):
        self.levels = {}
        self._create_levels()

    def _create_levels(self):
        from levels.level_1 import get_level_1
        level_1_data = get_level_1()
        
        tile_scale_1 = TILE_CONFIG[1]['tile_scale']
        default_type_1 = TILE_CONFIG[1]['default_type']
        
        platforms_1 = []
        for p in level_1_data['platforms']:
            platforms_1.append(Platform(
                p.x, p.y, p.width, p.height, 
                platform_type=default_type_1, 
                tile_scale=tile_scale_1
            ))
        
        self.levels[1] = {
            'platforms': platforms_1,
            'items': level_1_data['items'],
            'enemies': level_1_data['enemies'],
            'exit': level_1_data['exit'],
            'boss': level_1_data.get('boss')
        }

        from levels.level_2 import get_level_2
        level_2_data = get_level_2()
        
        tile_scale_2 = TILE_CONFIG[2]['tile_scale']
        default_type_2 = TILE_CONFIG[2]['default_type']
        
        platforms_2 = []
        for p in level_2_data['platforms']:
            platforms_2.append(Platform(
                p.x, p.y, p.width, p.height, 
                platform_type=default_type_2, 
                tile_scale=tile_scale_2
            ))
        
        self.levels[2] = {
            'platforms': platforms_2,
            'items': level_2_data['items'],
            'enemies': level_2_data['enemies'],
            'exit': level_2_data['exit'],
            'boss': level_2_data.get('boss')
        }

        from levels.level_3 import get_level_3
        level_3_data = get_level_3()
        
        tile_scale_3 = TILE_CONFIG[3]['tile_scale']
        default_type_3 = TILE_CONFIG[3]['default_type']
        
        platforms_3 = []
        for p in level_3_data['platforms']:
            platforms_3.append(Platform(
                p.x, p.y, p.width, p.height, 
                platform_type=default_type_3, 
                tile_scale=tile_scale_3
            ))
        
        self.levels[3] = {
            'platforms': platforms_3,
            'items': level_3_data['items'],
            'enemies': level_3_data['enemies'],
            'exit': level_3_data['exit'],
            'boss': level_3_data.get('boss')
        }

    def get_level(self, level_num):
        return self.levels.get(level_num, self.levels[1])

    def get_total_items(self, level_num):
        level = self.levels.get(level_num, self.levels[1])
        return len(level['items'])