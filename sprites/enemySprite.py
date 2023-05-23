import pygame
import random
import json

# Define the enemy sprite class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, windowH, windowW, color, playerY):
        super().__init__()
        self.window_height = windowH
        self.window_width = windowW
        self.color = color
        self.player = playerY

        # load enemy data from file
        with open('gameData\enemy_data.json') as data_file:
            data = json.load(data_file)

        self.width = data["width"]
        self.height = data["height"]
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = data["initial_x"]
        self.rect.y = random.randint(data["min_y"], data["max_y"])
        self.speed_x = random.randint(data["min_speed_x"], data["max_speed_x"])
        self.passed = False

    def update(self):
        self.rect.x -= self.speed_x
        if self.rect.right < 0:
            self.kill()

    def getEnemyCordX(self):
        return self.rect.x