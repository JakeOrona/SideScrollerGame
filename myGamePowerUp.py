import pygame
import random

# Define the powerup sprite class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, windowH, windowW, color, playerY):
        super().__init__()
        self.window_height = windowH
        self.window_width = windowW
        self.color = color
        self.player = playerY
        self.radius = 10
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.x = self.window_width
        self.rect.y = self.player
        self.speed_x = random.randint(3, 10)
        self.passed = False

    def update(self):
        self.rect.x -= self.speed_x
        if self.rect.right < 0:
            self.kill()

    def getPowerUPCordX(self):
        return self.rect.x