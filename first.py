"""
Author: Reshard Turner (based on original by Dhruv B Kakadiya)
Purpose: Main game loop for the Ravens-themed Checkerboard
"""

# Import libraries
import pygame as pg
from modules import statics as st
from modules.statics import *
from modules.checker_board import *
from modules.checker import *

# Static variables for this file
fps = 60

# Initialize Pygame display
WIN = pg.display.set_mode((st.width, st.height))
pg.display.set_caption("Checkers")

# 🎨 Initialize font for score display
pg.font.init()
score_font = pg.font.SysFont('Arial', 30)

# Get row and column for mouse position
def get_row_col_mouse(pos):
    x, y = pos
    row = y // sq_size
    col = x // sq_size
    return row, col

# 🏁 Main function
if __name__ == "__main__":
    # Represents the game state
    run = True

    # Clock to control FPS
    clock = pg.time.Clock()

    # Create board and game objects
    board = checker_board()
    game = checker(WIN)

    # 🎮 Main game loop
    while run:
        clock.tick(fps)

        # Check for a winner
        if board.winner() is not None:
            print(f"Winner: {board.winner()}")

        # Check events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                row, col = get_row_col_mouse(pos)
                game.selectrc(row, col)

        # 🔄 Update game display
        game.update()

        # 🏆 Draw live scores on the screen
        white_score_text = score_font.render(f"White Score: {board.white_score}", True, (255, 255, 255))
        black_score_text = score_font.render(f"Black Score: {board.black_score}", True, (0, 0, 0))

        WIN.blit(white_score_text, (10, 10))
        WIN.blit(black_score_text, (10, 40))

        # Refresh display to show new scores
        pg.display.update()

    # Quit Pygame when the loop ends
    pg.quit()
