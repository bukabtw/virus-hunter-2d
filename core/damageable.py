class Damageable:
    def __init__(self, max_health=5, invincible_duration=60):
        self.max_health = max_health
        self.health = max_health
        self.invincible_timer = 0
        self.invincible_duration = invincible_duration
        self._damage_flash_timer = 0
    
    def take_damage(self, amount=1):
        if self.invincible_timer <= 0:
            self.health -= amount
            self.invincible_timer = self.invincible_duration
            self._damage_flash_timer = 10
            if self.health < 0:
                self.health = 0
            return True
        return False
    
    def update_invincibility(self):
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        if self._damage_flash_timer > 0:
            self._damage_flash_timer -= 1
    
    @property
    def is_flashing(self):
        return self._damage_flash_timer > 0
    
    @property
    def is_invincible(self):
        return self.invincible_timer > 0
    
    @property
    def is_dead(self):
        return self.health <= 0