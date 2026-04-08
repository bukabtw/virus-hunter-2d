import os

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60

MAP_WIDTH = 8000
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
PHONE_SPRITE_SIZE = (384, 32)
PHONE_FRAME_WIDTH = 32

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
    'jump_right': (29, 5),
    'jump_left': (27, 5),
    'attack_right': (15, 6),
    'attack_left': (13, 6)
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

TILE_CONFIG = {
    1: {
        'default_type': 'ram',
        'tile_scale': (2, 2),
        'platform_height': 32,
        'platform_style': 'green',
    },
    2: {
        'default_type': 'hdd',
        'tile_scale': (2, 2),
        'platform_height': 36,
        'platform_style': 'metal',
    },
    3: {
        'default_type': 'avast',
        'tile_scale': (1, 1),
        'platform_height': 40,
        'platform_style': 'dark',
    },
}

RAM_TILE_SIZE = (52, 15)
HDD_TILE_SIZE = (47, 36)
AVAST_TILE_SIZE = (64, 64)

PLAYER_SPEED = 5
PLAYER_JUMP_POWER = -12
GRAVITY = 0.8

DIFFICULTY = {
    1: {'name': 'Лёгкий', 'enemy_speed': 1.5, 'player_health': 5},
    2: {'name': 'Средний', 'enemy_speed': 2.5, 'player_health': 3},
    3: {'name': 'Сложный', 'enemy_speed': 3.5, 'player_health': 1},
}

DEFAULT_RESOLUTIONS = [(1200, 700), (1024, 768), (800, 600), (1920, 1080)]

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

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 40