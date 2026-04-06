import os

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60

MAP_WIDTH = 2400
MAP_HEIGHT = 1400

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

ITEM_ANIMATIONS = {
    'idle': (0, 5)
}

PLAYER_ANIMATIONS = {
    'idle_right': (25, 2),
    'idle_left': (23, 2),
    'walk_right': (11, 10),
    'walk_left': (9, 10),
    'jump_right': (4, 2),
    'jump_left': (2, 2),
    'attack_right': (29, 6),
    'attack_left': (27, 6)
}

PROJECTILE_ANIMATIONS = {
    'fly': (0, 12)
}

SPRITE_WIDTH = 64
SPRITE_HEIGHT = 64
SPRITE_SCALE = 2

SPRITE_ROWS = {
    'walk_left': (6, 13),
    'walk_right': (11, 10),
    'idle_left': (6, 2),
    'idle_right': (4, 2),
    'jump': (4, 2),
    'attack': (6, 4),
}

PLAYER_SPEED = 5
PLAYER_JUMP_POWER = -12
GRAVITY = 0.8

DIFFICULTY = {
    1: {'name': 'Лёгкий', 'enemy_speed': 1.5, 'player_health': 5},
    2: {'name': 'Средний', 'enemy_speed': 2.5, 'player_health': 3},
    3: {'name': 'Сложный', 'enemy_speed': 3.5, 'player_health': 2},
}

DEFAULT_RESOLUTIONS = [(1200, 700), (1024, 768), (800, 600), (1920, 1080)]

MUSIC_VOLUME = 0.5
SFX_VOLUME = 0.7

# Размеры кнопок
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 60