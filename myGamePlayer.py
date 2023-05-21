import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, windowH, windowW, gravity, color):
        super().__init__()
        self.window_height = windowH
        self.window_width = windowW
        self.gravity = gravity
        self.color= color
        self.width = 40
        self.height = 60
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = self.window_height - self.height
        self.speed_x = 0
        self.speed_y = 0
        self.is_jumping = False
        self.jump_count = 0
        self.powerup_timer = 0
        self.jump_power = -12
        self.max_jump_count = 2
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