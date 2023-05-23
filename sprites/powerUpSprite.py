import pygame
import random
import json

# Define the powerup sprite class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, windowH, windowW, color, playerY):
        super().__init__()
        self.window_height = windowH
        self.window_width = windowW
        self.color = color

        # load enemy data from file
        with open("gameData\powerup_data.json") as data_file:
            data = json.load(data_file)

        self.radius = data["radius"]
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.x = self.window_width
        self.rect.y = random.randint(data["min_y"], data["max_y"])
        self.speed_x = random.randint(data["min_speed_x"], data["max_speed_x"])
        self.passed = False

    def update(self):
        self.rect.x -= self.speed_x
        if self.rect.right < 0:
            self.kill()

    def getPowerUPCordX(self):
        return self.rect.x