"""
Author : Dhruv B Kakadiya

"""

import pygame as pg
from .statics import *
from .pieces import *
import os


"""
Author: Reshard Turner (based on original by Dhruv B Kakadiya)
Purpose: Checkerboard logic with Baltimore Ravens-themed tiles
"""

import pygame as pg
import os
import random
from .statics import *
from .pieces import *

class checker_board:
    def __init__(self):
        self.board = []
        self.selected = None
        self.black_l = self.white_l = 12
        self.black_k = self.white_k = 0
        self.logos = []
        self.create_board()
        self.load_logos()

    def load_logos(self):
        """Load all Raven-themed logos once and scale them to square size."""
        asset_path = "assets"
        # Load raven1.jpeg to raven12.jpeg
        for i in range(1, 13):
            img = pg.image.load(os.path.join(asset_path, f"raven{i}.jpeg"))
            self.logos.append(pg.transform.scale(img, (sq_size, sq_size)))

        # Load crown and ravens_logo
        crown = pg.image.load(os.path.join(asset_path, "crown.png"))
        logo = pg.image.load(os.path.join(asset_path, "ravens_logo.png"))
        self.logos.append(pg.transform.scale(crown, (sq_size, sq_size)))
        self.logos.append(pg.transform.scale(logo, (sq_size, sq_size)))

    def draw_cubes(self, window):
        """Draw checkerboard with random Raven-themed logos on yellow tiles."""
        window.fill(green)

        for row in range(rows):
            for col in range(row % 2, cols, 2):
                rect = (row * sq_size, col * sq_size, sq_size, sq_size)
                pg.draw.rect(window, yellow, rect)
                random_logo = random.choice(self.logos)
                window.blit(random_logo, (row * sq_size, col * sq_size))

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
                        self.board[row].append(pieces(row, col, white))
                    elif row > 4:
                        self.board[row].append(pieces(row, col, black))
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
                else:
                    self.white_l -= 1

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

# checker board creation
class checker_board:
    def __init__(self):
        self.board = []
        self.selected = None
        self.black_l = self.white_l = 12
        self.black_k = self.white_k = 0
        self.create_board()

    # to design the board
    def draw_cubes(self, window):
       window.fill(green)

    # Load and scale the logo once
       logo = pg.image.load(os.path.join("assets", "ravens_logo.png"))
       logo = pg.transform.scale(logo, (sq_size, sq_size))  # Fill the square

       for row in range(rows):
           for col in range(row % 2, cols, 2):
               rect = (row * sq_size, col * sq_size, sq_size, sq_size)
               pg.draw.rect(window, yellow, rect)
               window.blit(logo, (row * sq_size, col * sq_size))
 

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

    # to get piece whatever they want
    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(rows):
            self.board.append([])
            for col in range(cols):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(pieces(row, col, white))
                    elif row > 4:
                        self.board[row].append(pieces(row, col, black))
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

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == black:
                    self.black_l -= 1
                else:
                    self.white_l -= 1

    def winner(self):
        if self.black_l <= 0:
            return white
        elif self.white_l <= 0:
            return black
        return None

    # Traversal Left
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
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, rows)
                    moves.update(
                        self._traverse_l(r + step, row, step, color, l - 1, skip=last)
                    )
                    moves.update(
                        self._traverse_r(r + step, row, step, color, l + 1, skip=last)
                    )
                break

            elif current.color == color:
                break
            else:
                last = [current]
            l -= 1
        return moves

    # Traversal Right
    def _traverse_r(self, start, stop, step, color, right, skip=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= cols:
                break
            current = self.board[r][right]
            if current == 0:
                if skip and not last:
                    break
                elif skip:
                    moves[(r, right)] = last + skip
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, rows)
                    moves.update(
                        self._traverse_l(
                            r + step, row, step, color, right - 1, skip=last
                        )
                    )
                    moves.update(
                        self._traverse_r(
                            r + step, row, step, color, right + 1, skip=last
                        )
                    )
                break

            elif current.color == color:
                break
            else:
                last = [current]
            right += 1
        return moves
