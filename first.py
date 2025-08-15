"""
Author: Reshard Turner (based on original by Dhruv B Kakadiya)
Purpose: Main game loop for the Ravens-themed Checkerboard
"""

import pygame as pg
import modules.statics as st
from modules.statics import sq_size, rows, cols
from modules.checker_board import checker_board
from modules.checker import checker

FPS = 60


def get_row_col_mouse(pos):
    x, y = pos
    return y // sq_size, x // sq_size


def draw_score_overlay(surface, board_obj, font):
    panel_rect = pg.Rect(8, 8, 250, 68)
    overlay = pg.Surface(panel_rect.size, pg.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    surface.blit(overlay, panel_rect.topleft)
    white_text = font.render(
        f"White Score: {getattr(board_obj, 'white_score', 0)}", True, (255, 255, 255)
    )
    black_text = font.render(
        f"Black Score: {getattr(board_obj, 'black_score', 0)}", True, (255, 255, 255)
    )
    surface.blit(white_text, (panel_rect.x + 10, panel_rect.y + 8))
    surface.blit(black_text, (panel_rect.x + 10, panel_rect.y + 38))


def draw_winner_banner(surface, winner, font):
    msg = f"Winner: {winner}"
    text = font.render(msg, True, (255, 255, 255))
    padding = 24
    box_w, box_h = text.get_width() + padding * 2, text.get_height() + padding * 2
    box_x = (st.width - box_w) // 2
    box_y = (st.height - box_h) // 2
    overlay = pg.Surface((box_w, box_h), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (box_x, box_y))
    surface.blit(text, (box_x + padding, box_y + padding))


if __name__ == "__main__":
    pg.init()
    pg.font.init()

    WIN = pg.display.set_mode((st.width, st.height))
    pg.display.set_caption("Checkers")

    try:
        score_font = pg.font.SysFont("Arial", 24)
        banner_font = pg.font.SysFont("Arial", 36, bold=True)
    except Exception:
        score_font = pg.font.Font(None, 24)
        banner_font = pg.font.Font(None, 36)

    clock = pg.time.Clock()
    run = True

    board = checker_board()
    game = checker(WIN)

    print("[Controls]  Esc: Quit   R: Reset game")

    while run:
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
                elif event.key == pg.K_r:
                    board = checker_board()
                    game = checker(WIN)
                    print("[Info] Game reset.")
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                row, col = get_row_col_mouse(pg.mouse.get_pos())
                if 0 <= row < rows and 0 <= col < cols:
                    game.selectrc(row, col)

        game.update()
        draw_score_overlay(WIN, board, score_font)
        w = board.winner()
        if w is not None:
            draw_winner_banner(WIN, w, banner_font)

        pg.display.update()

    pg.quit()
