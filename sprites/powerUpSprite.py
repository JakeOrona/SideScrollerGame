import pygame
import random
import json

# Define the powerup sprite class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, windowH, windowW):
        super().__init__()
        self.window_height = windowH
        self.window_width = windowW

        # Load powerup data from file
        with open("gameData/powerup_data.json") as data_file:
            self.data = json.load(data_file)

        self.radius = self.data["radius"]
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)

        # Load the powerup image and resize it to fit within the circular shape
        self.powerup_image1 = pygame.image.load("resources/petrol.png")
        self.powerup_image2 = pygame.image.load("resources/petrolAlt2.png")
        self.powerup_image1 = pygame.transform.scale(self.powerup_image1, (self.radius * 2, self.radius * 2))
        self.powerup_image2 = pygame.transform.scale(self.powerup_image2, (self.radius * 2, self.radius * 2))
        # Set current image
        self.current_image = self.powerup_image1
        self.rect = self.image.get_rect()

        # Set sprite variables
        self.rect.x = self.window_width
        self.rect.y = random.randint(self.data["min_y"], self.data["max_y"])
        self.speed_x = random.randint(self.data["min_speed_x"], self.data["max_speed_x"])
        self.passed = False
        self.animation_timer = 0

    def update(self):
        self.rect.x -= self.speed_x # move right to left
        if self.rect.right < 0:
            self.kill()
        
        # Animation timer to switch between images
        self.animation_timer += 1
        if self.animation_timer >= self.data["animation_interval"]:  # Adjust the interval to control the speed of the animation
            self.animation_timer = 0
            if self.current_image == self.powerup_image1:
                self.current_image = self.powerup_image2
            else:
                self.current_image = self.powerup_image1

        # Update the powerup image
        self.image.blit(self.current_image, (0, 0))

    def getPowerUPCordX(self):
        return self.rect.x
