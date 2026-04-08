class Damageable:
    
    def __init__(self, max_health=5, invincible_duration=60):
        self.max_health = max_health
        self.health = max_health
        self.invincible_timer = 0
        self.invincible_duration = invincible_duration
    
    def take_damage(self, amount=1):
        if self.invincible_timer <= 0:
            self.health -= amount
            self.invincible_timer = self.invincible_duration
            if self.health < 0:
                self.health = 0
            return True
        return False
    
    def heal(self, amount=1):
        self.health = min(self.max_health, self.health + amount)
    
    def update_invincibility(self):
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
    
    @property
    def is_invincible(self):
        return self.invincible_timer > 0
    
    @property
    def is_dead(self):
        return self.health <= 0