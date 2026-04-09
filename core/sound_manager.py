import pygame
from settings import SFX_VOLUME, MUSIC_VOLUME

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music = {}
        self.sfx_volume = SFX_VOLUME
        self.music_volume = MUSIC_VOLUME
        self.current_music = None
        self.looped_sounds = {}
    
    def load_sound(self, name, path):
        try:
            self.sounds[name] = pygame.mixer.Sound(path)
            self.sounds[name].set_volume(self.sfx_volume)
        except Exception as e:
            print(f"Не удалось загрузить звук {name}: {e}")
    
    def load_music(self, name, path):
        try:
            self.music[name] = path
        except Exception as e:
            print(f"Не удалось загрузить музыку {name}: {e}")
    
    def play_music(self, name, loop=-1):
        if name in self.music:
            if self.current_music == name:
                return
            pygame.mixer.music.load(self.music[name])
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loop)
            self.current_music = name
    
    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None
    
    def play_looped(self, name, fade_ms=0):
        if name in self.sounds:
            if name in self.looped_sounds and self.looped_sounds[name]:
                return
            channel = self.sounds[name].play(loops=-1, fade_ms=fade_ms)
            self.looped_sounds[name] = channel
    
    def stop_looped(self, name, fade_ms=0):
        if name in self.looped_sounds and self.looped_sounds[name]:
            self.looped_sounds[name].fadeout(fade_ms)
            self.looped_sounds[name] = None

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()
    
    def play_attack(self, entity_type):
        sound_map = {
            'player': 'player_attack',
            'enemy': 'enemy_attack',
            'boss': 'boss_attack'
        }
        sound_name = sound_map.get(entity_type)
        if sound_name and sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_hit(self, entity_type):
        sound_map = {
            'player': 'player_hit',
            'enemy': 'enemy_hit',
            'boss': 'boss_hit'
        }
        sound_name = sound_map.get(entity_type)
        if sound_name and sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_boss_spawn(self):
        if 'boss_spawn' in self.sounds:
            self.sounds['boss_spawn'].play()
    
    def play_boss_roar(self):
        if 'boss_roar' in self.sounds:
            self.sounds['boss_roar'].play()
    
    def play_boss_death(self):
        if 'boss_death' in self.sounds:
            self.sounds['boss_death'].play()
    
    def play_collect(self):
        if 'collect' in self.sounds:
            self.sounds['collect'].play()
    
    def play_victory(self):
        if 'victory' in self.sounds:
            self.sounds['victory'].play()
    
    def play_game_over(self):
        if 'game_over' in self.sounds:
            self.sounds['game_over'].play()
    
    def play_level_up(self):
        if 'level_up' in self.sounds:
            self.sounds['level_up'].play()
    
    def play_jump(self):
        if 'player_jump' in self.sounds:
            self.sounds['player_jump'].play()
    
    def set_volume(self, volume):
        self.sfx_volume = volume
        for sound in self.sounds.values():
            sound.set_volume(volume)
    
    def set_music_volume(self, volume):
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)