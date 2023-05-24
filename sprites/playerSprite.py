import pygame
import json

class Player(pygame.sprite.Sprite):
    def __init__(self, windowH, windowW, gravity):
        super().__init__()
        self.image = pygame.image.load("resources/tank-80-55.png").convert_alpha() # load player image
        self.rect = self.image.get_rect()  # Get the rectangle of the player image
        self.window_height = windowH
        self.window_width = windowW
        self.gravity = gravity

        # load player data from file
        with open('gameData\player_data.json') as data_file:
            data = json.load(data_file)
        
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.x = data["initial_x"]
        self.rect.y = self.window_height - self.height
        self.speed_x = data["player_speed_x"]
        self.speed_y = data["player_speed_y"]
        self.is_jumping = False
        self.jump_count = data["initial_jump_count"]
        self.powerup_timer = data["initial_powerup_timer"]
        self.jump_power = data["jump_power"]
        self.max_jump_count = data["max_jump_count"]
        self.powerup_active = False

    def update(self):
        self.speed_y += self.gravity
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.window_width:
            self.rect.right = self.window_width
        if self.rect.bottom > self.window_height:
            self.rect.bottom = self.window_height
            self.speed_y = 0
            self.is_jumping = False
            self.jump_count = 0
        if self.powerup_timer > 0:
                self.max_jump_count = 3  # add a 3rd jump
                self.powerup_timer -= 1
                if self.powerup_timer == 0:
                    self.max_jump_count= 2  # Restore the original speed
                    self.powerup_active = False

    def apply_power_up(self, duration):
        self.powerup_timer = duration * 60  # Convert duration to frames (assuming 60 FPS)
        self.powerup_active = True

    def getPlayerCordY(self):
        return self.rect.y