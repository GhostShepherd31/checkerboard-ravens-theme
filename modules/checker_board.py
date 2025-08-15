import pygame as pg
from .statics import *  # rows, cols, sq_size, yellow, white, black
from .pieces import *  # pieces class

__all__ = ["checker_board"]


class checker_board:
    def __init__(self, white_icon=None, black_icon=None):
        # Board & selection
        self.board = []
        self.selected = None

        # Remaining pieces and kings (kept in sync via _recount_pieces)
        self.black_l = self.white_l = 12
        self.black_k = self.white_k = 0

        # Capture scores (white_score = captures made by white)
        self.white_score = 0
        self.black_score = 0

        # Optional icons passed to piece constructor
        self.white_icon = white_icon
        self.black_icon = black_icon

        # Build initial board
        self.create_board()

    # -------------------- Board / drawing --------------------
    def draw_cubes(self, window):
        """Draw the purple/yellow checkerboard."""
        PURPLE = (75, 0, 130)
        window.fill(PURPLE)
        for row in range(rows):
            for col in range(cols):
                rect = (col * sq_size, row * sq_size, sq_size, sq_size)
                if (row + col) % 2 == 0:
                    pg.draw.rect(window, PURPLE, rect)
                else:
                    pg.draw.rect(window, yellow, rect)

    def create_board(self):
        """Place pieces: BLACK on top (rows 0–2), WHITE on bottom (rows 5–7)."""
        self.board = []
        for row in range(rows):
            self.board.append([])
            for col in range(cols):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        # TOP: black
                        self.board[row].append(pieces(row, col, black, self.black_icon))
                    elif row > 4:
                        # BOTTOM: white
                        self.board[row].append(pieces(row, col, white, self.white_icon))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, window):
        self.draw_cubes(window)
        for r in range(rows):
            for c in range(cols):
                p = self.board[r][c]
                if p != 0:
                    p.draw(window)

    def get_piece(self, row, col):
        return self.board[row][col]

    # -------------------- Movement / rules --------------------
    def move(self, piece, row, col):
        """Move a piece and crown if it reaches the far rank."""
        self.board[piece.row][piece.col], self.board[row][col] = (
            self.board[row][col],
            self.board[piece.row][piece.col],
        )
        piece.move(row, col)

        # Crowning
        if row == rows - 1 or row == 0:
            was_king = piece.king
            piece.make_king()
            if piece.king and not was_king:
                if piece.color == white:
                    self.white_k += 1
                else:
                    self.black_k += 1

    def get_valid_moves(self, piece):
        """Return dict of {(row, col): [captured_pieces...]}."""
        moves = {}
        l = piece.col - 1
        r = piece.col + 1
        row = piece.row

        # Black moves upward (toward row decreasing), White downward (row increasing).
        if piece.color == black or piece.king:
            moves.update(
                self._traverse_l(row - 1, max(row - 3, -1), -1, piece.color, l)
            )
            moves.update(
                self._traverse_r(row - 1, max(row - 3, -1), -1, piece.color, r)
            )

        if piece.color == white or piece.king:
            moves.update(
                self._traverse_l(row + 1, min(row + 3, rows), 1, piece.color, l)
            )
            moves.update(
                self._traverse_r(row + 1, min(row + 3, rows), 1, piece.color, r)
            )

        return moves

    def _traverse_l(self, start, stop, step, color, l, skip=None):
        if skip is None:
            skip = []
        moves = {}
        last = []
        for r in range(start, stop, step):
            if l < 0:
                break
            current = self.board[r][l]
            if current == 0:
                if skip and not last:
                    break
                elif skip:
                    moves[(r, l)] = last + skip
                else:
                    moves[(r, l)] = last
                if last:
                    row_lim = max(r - 3, 0) if step == -1 else min(r + 3, rows)
                    moves.update(
                        self._traverse_l(
                            r + step, row_lim, step, color, l - 1, skip=last
                        )
                    )
                    moves.update(
                        self._traverse_r(
                            r + step, row_lim, step, color, l + 1, skip=last
                        )
                    )
                break
            elif current.color == color:
                break
            else:
                last = [current]
            l -= 1
        return moves

    def _traverse_r(self, start, stop, step, color, rgt, skip=None):
        if skip is None:
            skip = []
        moves = {}
        last = []
        for r in range(start, stop, step):
            if rgt >= cols:
                break
            current = self.board[r][rgt]
            if current == 0:
                if skip and not last:
                    break
                elif skip:
                    moves[(r, rgt)] = last + skip
                else:
                    moves[(r, rgt)] = last
                if last:
                    row_lim = max(r - 3, 0) if step == -1 else min(r + 3, rows)
                    moves.update(
                        self._traverse_l(
                            r + step, row_lim, step, color, rgt - 1, skip=last
                        )
                    )
                    moves.update(
                        self._traverse_r(
                            r + step, row_lim, step, color, rgt + 1, skip=last
                        )
                    )
                break
            elif current.color == color:
                break
            else:
                last = [current]
            rgt += 1
        return moves

    def remove(self, pieces_list):
        """Remove captured pieces and update capture scores & remaining counts."""
        for piece in pieces_list:
            if piece == 0:
                continue
            self.board[piece.row][piece.col] = 0
            if piece.color == black:
                self.black_l -= 1
                self.white_score += 1
            else:
                self.white_l -= 1
                self.black_score += 1

    # -------------------- Winner / counts --------------------
    def _recount_pieces(self):
        """Scan the board and refresh remaining piece counters."""
        w = 0
        b = 0
        for r in range(rows):
            for c in range(cols):
                p = self.board[r][c]
                if p == 0:
                    continue
                if p.color == white:
                    w += 1
                else:
                    b += 1
        self.white_l = w
        self.black_l = b
        return w, b

    def winner(self):
        """
        Returns 'White' or 'Black' when one side has no pieces left.
        Returns 'Draw' if both are zero, otherwise None.
        """
        w, b = self._recount_pieces()
        if w == 0 and b == 0:
            return "Draw"
        if w == 0:
            return "Black"
        if b == 0:
            return "White"
        return None
