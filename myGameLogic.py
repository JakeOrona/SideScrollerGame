import pygame
import myGameScore as Score
from myGamePlayer import Player
from myGameEnemy import Enemy
from myGamePowerUp import PowerUp

class Game:
    def __init__(self, window):
        # set up game variables
        self.font_size = 36
        self.font = pygame.font.Font(None, self.font_size)
        self.score_font = pygame.font.Font(None, self.font_size)
        self.high_score_font = pygame.font.Font(None, self.font_size)
        self.power_up_font = pygame.font.Font(None, self.font_size)

        self.window = window
        self.window_width = 800
        self.window_height = 600

        self.clock = pygame.time.Clock()
        self.game_started = False

        self.gravity = 0.5
        self.enemy_spawn_delay = 75
        self.enemy_spawn_timer = self.enemy_spawn_delay
        self.powerup_spawn_delay=500
        self.powerup_spawn_timer = self.powerup_spawn_delay

        # Score Variables
        self.score = 0
        self.timer = 0
        self.timer_font = pygame.font.Font(None, self.font_size)
        self.enemies_avoided = 0
        high_score, high_enemies_avoided, high_timer = Score.load_high_score()
        self.high_score = high_score
        self.high_enemies_avoided = high_enemies_avoided
        self.high_timer = high_timer

        # Define colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.LGREEN = (50,205,50)

        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()

        # Create player sprite
        self.player = Player(window.get_height(), window.get_width(), self.gravity, self.BLUE)
        self.all_sprites.add(self.player)
        self.players.add(self.player)

        # Create try again button rectangle
        self.try_again_rect = pygame.Rect(window.get_width() // 2 - 100, 300, 200, 50)

        # Create quit button rectangle
        self.quit_rect = pygame.Rect(window.get_width() // 2 - 100, 400, 200, 50)

        # Define the high score text content
        self.high_score_text_content = [
            "-Top Run-",
            "High Score: " + str(self.high_score),
            "Enemies Avoided: " + str(self.high_enemies_avoided),
            f"Timer: " + str((self.high_timer // 60))
        ]

        # Set up the high score text block
        self.high_score_text_block = []
        self.high_score_text_line_height = self.font_size + 2  # Adjust line spacing
        for line in self.high_score_text_content:
            rendered_line = self.high_score_font.render(line, True, self.YELLOW)
            self.high_score_text_block.append(rendered_line)

         # Calculate the dimensions of the text block
        self.high_score_text_block_width = max(line.get_width() for line in self.high_score_text_block)
        self.high_score_text_block_height = len(self.high_score_text_block) * self.high_score_text_line_height


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and (not self.player.is_jumping or self.player.jump_count < self.player.max_jump_count) and self.game_started:
                        self.player.speed_y = self.player.jump_power
                        self.player.is_jumping = True
                        self.player.jump_count += 1
                    elif event.key == pygame.K_a and self.game_started:
                        self.player.speed_x = -5  # Move left
                    elif event.key == pygame.K_d and self.game_started:
                        self.player.speed_x = 5  # Move right
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a and self.player.speed_x < 0:
                        self.player.speed_x = 0  # Stop left movement
                    elif event.key == pygame.K_d and self.player.speed_x > 0:
                        self.player.speed_x = 0  # Stop right movement
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.game_started:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.try_again_rect.collidepoint(mouse_pos):
                            # Start the game again
                            self.start_game()
                        elif self.quit_rect.collidepoint(mouse_pos):
                            # Quit the game
                            running = False

            if self.game_started:
                self.update()
                self.check_collisions()

            self.draw()

            pygame.display.flip()
            self.clock.tick(60)

    def update(self):
        self.all_sprites.update()

        # Spawn enemies
        self.enemy_spawn_timer -= 1
        # enemy = None  # Declare the variable with a default value
        if self.enemy_spawn_timer <= 0:
            enemy = Enemy(self.window.get_height(), self.window.get_width(), self.RED, self.player.getPlayerCordY())
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)
            self.enemy_spawn_timer = self.enemy_spawn_delay

        # Spawn power ups
        self.powerup_spawn_timer -= 1
        # power up = None  # Declare the variable with a default value
        if self.powerup_spawn_timer <= 0:
            powerUp = PowerUp(self.window.get_height(), self.window.get_width(), self.WHITE, self.player.getPlayerCordY())
            self.all_sprites.add(powerUp)
            self.power_ups.add(powerUp)
            self.powerup_spawn_timer = self.powerup_spawn_delay
        
        # Update timer and score
        self.timer += 1
        self.score = self.timer // 10
        if self.high_score < self.score:
            self.high_score = self.score
        if self.high_enemies_avoided < self.enemies_avoided:
            self.high_enemies_avoided = self.enemies_avoided
        if self.high_timer < self.timer:
            self.high_timer = self.timer

        # Update high score text content
        self.high_score_text_content[1] = "High Score: " + str(self.high_score)
        self.high_score_text_content[2] = "Enemies Avoided: " + str(self.high_enemies_avoided)
        self.high_score_text_content[3] = "Timer: " + str((self.high_timer // 60))

        # Update high score text block
        self.update_high_score_text_block()

    def check_collisions(self):
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            # Reset the game
            self.end_game()
        elif pygame.sprite.spritecollide(self.player, self.power_ups, True):
                self.player.apply_power_up(15)  # Apply the power-up for 15 seconds

        # Check if any enemy has exited the left edge of the window and increment the enemies avoided variable
        for enemy in self.enemies.sprites():
            if enemy.getEnemyCordX() < 0 and not enemy.passed:
                self.enemies_avoided += 1
                enemy.passed = True

    def update_high_score_text_block(self):
            self.high_score_text_block = []
            for line in self.high_score_text_content:
                rendered_line = self.high_score_font.render(line, True, self.YELLOW)
                self.high_score_text_block.append(rendered_line)

            self.high_score_text_block_width = max(line.get_width() for line in self.high_score_text_block)
            self.high_score_text_block_height = len(self.high_score_text_block) * self.high_score_text_line_height

    def draw(self):
        self.window.fill(self.BLACK)

        if not self.game_started:
            # Draw the text block onto the window
            self.update_high_score_text_block()
            high_score_x = self.window.get_width() - self.high_score_text_block_width -10
            high_score_y = 10
            for line in self.high_score_text_block:
                self.window.blit(line, (high_score_x, high_score_y))
                high_score_y += self.high_score_text_line_height

            pygame.draw.rect(self.window, (255, 0, 0), self.try_again_rect)
            try_again_text = pygame.font.Font(None, 40).render("Try Again", True, self.WHITE)
            try_again_text_rect = try_again_text.get_rect(center=self.try_again_rect.center)
            self.window.blit(try_again_text, try_again_text_rect)

            pygame.draw.rect(self.window, (255, 0, 0), self.quit_rect)
            quit_text = pygame.font.Font(None, 40).render("Quit", True, self.WHITE)
            quit_text_rect = quit_text.get_rect(center=self.quit_rect.center)
            self.window.blit(quit_text, quit_text_rect)

        else:
            self.all_sprites.draw(self.window)

            score_text = self.score_font.render(f"Score: {self.score}", True, self.WHITE)
            self.window.blit(score_text, (10, 10))

            enemy_avoided_text = self.score_font.render(f"Enemies Avoided: {self.enemies_avoided}", True, self.WHITE)
            self.window.blit(enemy_avoided_text, (10, 50))

            seconds = self.timer // 60
            milliseconds = (self.timer % 60) * 1000 // 60
            timer_text = self.timer_font.render(f"Timer: {seconds}.{milliseconds:02d}", True, self.WHITE)
            self.window.blit(timer_text, (10, 90))

            # Update high scores display block if necessary
            if self.score > self.high_score:
                self.high_score = self.score
            if self.enemies_avoided > self.high_enemies_avoided:
                self.high_enemies_avoided = self.enemies_avoided
            if self.timer > self.high_timer:
                self.high_timer = self.timer

            # Get High Score Timer formatting
            hs_seconds = self.high_timer // 60
            hs_milliseconds = (self.high_timer % 60) * 1000 // 60
            # Update high score text content
            self.high_score_text_content[1] = "High Score: " + str(self.high_score)
            self.high_score_text_content[2] = "Enemies Avoided: " + str(self.high_enemies_avoided)
            self.high_score_text_content[3] = f"Timer: {hs_seconds}.{int(hs_milliseconds):02d}"

            # Update high score text block
            self.update_high_score_text_block()

            # Draw the text block onto the window
            high_score_x = self.window.get_width() - self.high_score_text_block_width -10
            high_score_y = 10
            for line in self.high_score_text_block:
                self.window.blit(line, (high_score_x, high_score_y))
                high_score_y += self.high_score_text_line_height
            
            # If Player powerup active display text
            if self.player.powerup_active:
                powerup_text = self.power_up_font.render("Triple Jump Active", True, self.LGREEN)
                powerup_text_rect = powerup_text.get_rect(center=((self.window_width // 2)+50, 16))
                powerup_text_rect.x -= powerup_text_rect.width // 2
                self.window.blit(powerup_text, powerup_text_rect)

                powerup_timer_text = self.power_up_font.render(f"Time Left: {self.player.powerup_timer/100:.1f}s", True, self.LGREEN)
                powerup_timer_text_rect = powerup_timer_text.get_rect(center=((self.window_width // 2)+50, 48))
                powerup_timer_text_rect.x -= powerup_timer_text_rect.width // 2
                self.window.blit(powerup_timer_text, powerup_timer_text_rect)

    def start_game(self):
        self.game_started = True
        self.reset_game()

    def end_game(self):
        #check for new high score
        if self.score > self.high_score:
            self.high_score = self.score
        if self.enemies_avoided > self.high_enemies_avoided:
            self.high_enemies_avoided = self.enemies_avoided
        if self.timer > self.high_timer:
            self.high_timer = self.timer
        Score.save_high_score(self.high_score, self.high_enemies_avoided, self.high_timer)

        self.game_started = False
        self.reset_game()

    def reset_game(self):
        self.all_sprites.empty()
        self.players.empty()
        self.enemies.empty()
        self.player = Player(self.window.get_height(), self.window.get_width(), self.gravity, self.BLUE)
        self.all_sprites.add(self.player)
        self.players.add(self.player)
        self.score = 0
        self.timer = 0
        self.enemies_avoided = 0
