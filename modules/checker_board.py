import pygame as pg
import os
import random
from .statics import *
from .pieces import *

class checker_board:
    def __init__(self, white_icon=None, black_icon=None):
        self.board = []
        self.selected = None
        self.black_l = self.white_l = 12
        self.black_k = self.white_k = 0
        self.white_score = 0
        self.black_score = 0
        self.logos = []
        self.tile_logos = {}

        self.white_icon = white_icon
        self.black_icon = black_icon

        self.create_board()
        self.load_logos()

    def load_logos(self):
        asset_path = "assets"
        for i in range(1, 13):
            logo = pg.image.load(os.path.join(asset_path, f"raven{i}.jpeg"))
            self.logos.append(pg.transform.scale(logo, (sq_size, sq_size)))

    def assign_tile_logos(self):
        for row in range(rows):
            for col in range(cols):
                if (row + col) % 2 != 0:
                    self.tile_logos[(row, col)] = random.choice(self.logos)

    def draw_cubes(self, window):
        PURPLE = (75, 0, 130)
        window.fill(PURPLE)

        for row in range(rows):
            for col in range(cols):
                rect = (col * sq_size, row * sq_size, sq_size, sq_size)
                if (row + col) % 2 == 0:
                    pg.draw.rect(window, PURPLE, rect)
                else:
                    pg.draw.rect(window, yellow, rect)
                    logo = self.tile_logos.get((row, col))
                    if logo:
                        window.blit(logo, (col * sq_size, row * sq_size))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = (
            self.board[row][col],
            self.board[piece.row][piece.col],
        )
        piece.move(row, col)
        if row == rows - 1 or row == 0:
            piece.make_king()
            if piece.color == white:
                self.white_k += 1
            else:
                self.black_k += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(rows):
            self.board.append([])
            for col in range(cols):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        # ✅ Use white player icon
                        self.board[row].append(pieces(row, col, white, self.white_icon))
                    elif row > 4:
                        # ✅ Use black player icon
                        self.board[row].append(pieces(row, col, black, self.black_icon))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, window):
        self.draw_cubes(window)
        for row in range(rows):
            for col in range(cols):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(window)

    def get_valid_moves(self, piece):
        moves = {}
        l = piece.col - 1
        r = piece.col + 1
        row = piece.row

        if piece.color == black or piece.king:
            moves.update(self._traverse_l(row - 1, max(row - 3, -1), -1, piece.color, l))
            moves.update(self._traverse_r(row - 1, max(row - 3, -1), -1, piece.color, r))

        if piece.color == white or piece.king:
            moves.update(self._traverse_l(row + 1, min(row + 3, rows), 1, piece.color, l))
            moves.update(self._traverse_r(row + 1, min(row + 3, rows), 1, piece.color, r))

        return moves

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == black:
                    self.black_l -= 1
                    self.white_score += 1
                else:
                    self.white_l -= 1
                    self.black_score += 1

    def winner(self):
        if self.black_l <= 0:
            return white
        elif self.white_l <= 0:
            return black
        return None

    def _traverse_l(self, start, stop, step, color, l, skip=[]):
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
                    row = max(r - 3, 0) if step == -1 else min(r + 3, rows)
                    moves.update(self._traverse_l(r + step, row, step, color, l - 1, skip=last))
                    moves.update(self._traverse_r(r + step, row, step, color, l + 1, skip=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            l -= 1
        return moves

    def _traverse_r(self, start, stop, step, color, rgt, skip=[]):
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
                    row = max(r - 3, 0) if step == -1 else min(r + 3, rows)
                    moves.update(self._traverse_l(r + step, row, step, color, rgt - 1, skip=last))
                    moves.update(self._traverse_r(r + step, row, step, color, rgt + 1, skip=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            rgt += 1
        return moves
