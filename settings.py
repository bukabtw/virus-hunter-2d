import os
import pygame

import ctypes
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
SCREEN_WIDTH = user32.GetSystemMetrics(0)
SCREEN_HEIGHT = user32.GetSystemMetrics(1)

FPS = 60
MAP_WIDTH = 20000
MAP_HEIGHT = 5000

COLORS = {
    'BLACK': (0,0,0),
    'WHITE': (255,255,255),
    'RED': (255,50,50),
    'GREEN': (50,255,50),
    'BLUE': (50,50,255),
    'DARK_GREEN': (20,50,20),
    'YELLOW': (255,255,50),
    'PURPLE': (128,0,128),
    'GRAY': (128,128,128),
    'CYAN': (50,255,255),
    'ORANGE': (255,165,0),
}

BASE_PATH = os.path.dirname(__file__)
ASSETS_PATH = os.path.join(BASE_PATH, 'assets')
SPRITES_PATH = os.path.join(ASSETS_PATH, 'sprites')
SOUNDS_PATH = os.path.join(ASSETS_PATH, 'sounds')
os.makedirs(SPRITES_PATH, exist_ok=True)
os.makedirs(SOUNDS_PATH, exist_ok=True)

PLAYER_SPRITESHEET = 'player.png'
ENEMY_SPRITESHEET = 'default_virus.png'
BOSS_SPRITESHEET = 'boss_virus.png'
ITEM_SPRITESHEET = 'pc.png'
PROJECTILE_SPRITESHEET = 'phone.png'

ENEMY_ANIMATIONS = {
    'idle': (0, 5),
    'walk_right': (1, 5),
    'walk_left': (2, 5),
    'attack_left': (3, 5),
    'attack_right': (4, 5)
}

BOSS_ANIMATIONS = {
    'idle': (0, 5),
    'look_left': (1, 5),
    'look_right': (2, 5),
    'attack_left': (3, 5),
    'attack_right': (4, 5)
}

ITEM_ANIMATIONS = {'idle': (0, 5)}

PLAYER_ANIMATIONS = {
    'idle_right': (25, 2),
    'idle_left': (23, 2),
    'walk_right': (11, 10),
    'walk_left': (9, 10),
    'jump_right': (29, 5),
    'jump_left': (27, 5),
    'attack_right': (15, 6),
    'attack_left': (13, 6)
}

PROJECTILE_ANIMATIONS = {'fly': (0, 12)}

SPRITE_WIDTH = 64
SPRITE_HEIGHT = 64
SPRITE_SCALE = 2

RAM_TILE_SIZE = (64, 32)
HDD_TILE_SIZE = (48, 64)
AVAST_TILE_SIZE = (64, 64)

PLATFORM_SCALE = 2

RAM_TILE_SIZE_SCALED = (RAM_TILE_SIZE[0] * PLATFORM_SCALE, RAM_TILE_SIZE[1] * PLATFORM_SCALE)
HDD_TILE_SIZE_SCALED = (HDD_TILE_SIZE[0] * PLATFORM_SCALE, HDD_TILE_SIZE[1] * PLATFORM_SCALE)
AVAST_TILE_SIZE_SCALED = (AVAST_TILE_SIZE[0] * PLATFORM_SCALE, AVAST_TILE_SIZE[1] * PLATFORM_SCALE)

TILE_CONFIG = {
    1: {
        'default_type': 'ram', 
        'tile_size': RAM_TILE_SIZE_SCALED,
        'base_size': RAM_TILE_SIZE
    },
    2: {
        'default_type': 'hdd', 
        'tile_size': HDD_TILE_SIZE_SCALED,
        'base_size': HDD_TILE_SIZE
    },
    3: {
        'default_type': 'avast', 
        'tile_size': AVAST_TILE_SIZE_SCALED,
        'base_size': AVAST_TILE_SIZE
    },
}

PLATFORM_SIZES = {
    'ram': RAM_TILE_SIZE_SCALED,
    'hdd': HDD_TILE_SIZE_SCALED,
    'avast': AVAST_TILE_SIZE_SCALED,
}


DIFFICULTY = {
    1: {'name': 'Лёгкий', 'enemy_speed': 1.5, 'player_health': 5},
    2: {'name': 'Средний', 'enemy_speed': 2.5, 'player_health': 3},
    3: {'name': 'Сложный', 'enemy_speed': 3.5, 'player_health': 1},
}

DIFFICULTY = {
    1: {'name': 'Лёгкий', 'enemy_speed': 1.5, 'player_health': 5},
    2: {'name': 'Средний', 'enemy_speed': 2.5, 'player_health': 3},
    3: {'name': 'Сложный', 'enemy_speed': 3.5, 'player_health': 1},
}

SOUND_PLAYER_ATTACK = os.path.join(SOUNDS_PATH, 'player_attack.wav')
SOUND_PLAYER_JUMP = os.path.join(SOUNDS_PATH, 'player_jump.wav')
SOUND_PLAYER_HIT = os.path.join(SOUNDS_PATH, 'player_hit.wav')
SOUND_ENEMY_ATTACK = os.path.join(SOUNDS_PATH, 'enemy_attack.wav')
SOUND_ENEMY_HIT = os.path.join(SOUNDS_PATH, 'enemy_hit.wav')
SOUND_BOSS_ATTACK = os.path.join(SOUNDS_PATH, 'boss_attack.wav')
SOUND_BOSS_HIT = os.path.join(SOUNDS_PATH, 'boss_hit.wav')
SOUND_BOSS_SPAWN = os.path.join(SOUNDS_PATH, 'boss_spawn.wav')
SOUND_BOSS_ROAR = os.path.join(SOUNDS_PATH, 'boss_roar.wav')
SOUND_BOSS_DEATH = os.path.join(SOUNDS_PATH, 'boss_death.wav')
SOUND_COLLECT = os.path.join(SOUNDS_PATH, 'collect.wav')
SOUND_VICTORY = os.path.join(SOUNDS_PATH, 'victory.wav')
SOUND_GAME_OVER = os.path.join(SOUNDS_PATH, 'game_over.wav')
SOUND_LEVEL_UP = os.path.join(SOUNDS_PATH, 'level_up.wav')
SOUND_MENU = os.path.join(SOUNDS_PATH, 'menu_soundtrack.wav')

MUSIC_VOLUME = 0.5
SFX_VOLUME = 0.7