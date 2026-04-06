import pygame
import random
from settings import COLORS

class Particle:
    __slots__ = ('x', 'y', 'vx', 'vy', 'life', 'color', 'size')
    
    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -1)
        self.life = 30
        self.color = color or random.choice([COLORS['RED'], COLORS['ORANGE'], COLORS['YELLOW']])
        self.size = random.randint(2, 5)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.3
        self.life -= 1
        return self.life > 0
    
    def draw(self, screen, camera_x=0, camera_y=0):
        if self.life > 0:
            alpha = min(255, self.life * 8)
            pygame.draw.circle(screen, self.color, (int(self.x - camera_x), int(self.y - camera_y)), self.size)

class ParticleSystem:
    def __init__(self, capacity=500):
        self.particles = []
        self.capacity = capacity
    
    def emit(self, x, y, count=10, color=None):
        for _ in range(min(count, self.capacity - len(self.particles))):
            self.particles.append(Particle(x, y, color))
    
    def update(self):
        self.particles = [p for p in self.particles if p.update()]
    
    def draw(self, screen, camera_x=0, camera_y=0):
        for p in self.particles:
            p.draw(screen, camera_x, camera_y)
    
    def clear(self):
        self.particles.clear()