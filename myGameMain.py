import pygame
from myGameLogic import Game

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Jump Nerd! Jump!")

# Create the game object
game = Game(window)

# Start the gamedd
game.run()

# Quit the game
pygame.quit()
