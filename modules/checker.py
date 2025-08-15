"""
Author : Dhruv B Kakadiya
"""

import pygame as pg
from .checker_board import checker_board
from .statics import white, black, sq_size

DOT_RADIUS = max(4, sq_size // 10)


class checker:
    def __init__(self, win):
        self.win = win
        self._init()

    def _init(self):
        self.selected = None
        self.board = checker_board()
        # White (bottom) moves first to match the board setup
        self.turn = white
        self.valid_moves = {}

    # ---- Public API used by first.py ----
    def update(self):
        self.board.draw(self.win)
        self._draw_valid_moves(self.valid_moves)
        pg.display.update()

    def selectrc(self, row, col):
        """
        Click handler: select a piece or attempt to move to (row, col).
        Returns True if the click led to a selection or a move.
        """
        # If a piece is already selected, try to move it
        if self.selected:
            moved = self._move(row, col)
            if not moved:
                # If the move failed, allow reselecting another piece of the same color
                self.selected = None
                return self.selectrc(row, col)
            return True

        # No piece selected yet — try to select a piece belonging to current turn
        piece = self.board.get_piece(row, col)
        if piece != 0 and getattr(piece, "color", None) == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece) or {}
            return True

        # Clicked empty square or opponent piece
        self.valid_moves = {}
        return False

    # ---- Internal helpers ----
    def _move(self, row, col):
        """
        Attempt to move selected piece to (row, col).
        Only moves to squares in valid_moves; applies captures and changes turn.
        """
        if not self.selected:
            return False

        if (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)

            self.selected = None
            self.valid_moves = {}
            self._change_turn()
            return True

        return False

    def _change_turn(self):
        self.turn = black if self.turn == white else white

    def _draw_valid_moves(self, moves):
        """Render small dots on valid destination squares for visual feedback."""
        for r, c in moves.keys():
            x = c * sq_size + sq_size // 2
            y = r * sq_size + sq_size // 2
            pg.draw.circle(self.win, (240, 240, 240), (x, y), DOT_RADIUS)
            pg.draw.circle(
                self.win, (20, 20, 20), (x, y), max(1, DOT_RADIUS // 2), width=1
            )
