import pygame
import random

# Define the enemy sprite class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, windowH, windowW, color, playerY):
        super().__init__()
        self.window_height = windowH
        self.window_width = windowW
        self.color = color
        self.player = playerY
        self.width = 35
        self.height = 35
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.window_width
        self.rect.y = random.randint(self.window_height // 2, self.window_height - self.height)
        self.speed_x = random.randint(3, 6)
        self.passed = False

    def update(self):
        self.rect.x -= self.speed_x
        if self.rect.right < 0:
            self.kill()

    def getEnemyCordX(self):
        return self.rect.x