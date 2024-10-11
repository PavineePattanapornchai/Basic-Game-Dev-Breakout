import pygame
from src.resources import power_up_images  # Ensure power_up_images is imported

class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.type = power_type
        self.width = 24
        self.height = 24

        # Correctly referencing extra life and multi-ball power-up
        if self.type == 'heart':
            self.image = power_up_images['extra_life']  # Image for extra life power-up
        elif self.type == 'ball':  
            self.image = power_up_images['ball']  # Image for multi-ball power-up
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.dy = 100  # Speed at which power-up falls

    def update(self, dt):
        self.rect.y += self.dy * dt

    def render(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def Collides(self, target):
        if self.rect.x > target.rect.x + target.width or target.rect.x > self.rect.x + self.width:
            return False
        if self.rect.y > target.rect.y + target.height or target.rect.y > self.rect.y + self.height:
            return False
        return True
