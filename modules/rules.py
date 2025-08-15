# modules/rules.py

from typing import Tuple, Optional


def is_simple_move(start, end, is_king: bool, player_dir: int) -> bool:
    sr, sc = start
    er, ec = end
    dr, dc = er - sr, ec - sc
    if abs(dr) == 1 and abs(dc) == 1:
        # Non-kings must move in the player's forward direction (e.g., +1 or -1)
        return is_king or dr == player_dir
    return False


def is_jump_move(start, end, is_king: bool, player_dir: int) -> bool:
    sr, sc = start
    er, ec = end
    dr, dc = er - sr, ec - sc
    if abs(dr) == 2 and abs(dc) == 2:
        # Non-kings can only jump forward; kings can jump both ways
        return is_king or (dr == 2 * player_dir)
    return False


def intermediate_square(start, end) -> Tuple[int, int]:
    sr, sc = start
    er, ec = end
    return (sr + (er - sr) // 2, sc + (ec - sc) // 2)


def is_valid_move(
    board, start, end, is_king: bool, player_color: str, player_dir: int
) -> Tuple[bool, Optional[Tuple[int, int]]]:
    """Return (ok, captured_pos). captured_pos is None for simple moves."""
    sr, sc = start
    er, ec = end

    # 1) Destination must be on board and empty
    if not (0 <= er < 8 and 0 <= ec < 8):
        return (False, None)
    if board[er][ec] is not None:
        return (False, None)

    # 2) Simple diagonal step?
    if is_simple_move(start, end, is_king, player_dir):
        return (True, None)

    # 3) Jump (capture)?
    if is_jump_move(start, end, is_king, player_dir):
        mr, mc = intermediate_square(start, end)
        mid_piece = board[mr][mc]
        if mid_piece is None:
            return (False, None)
        if mid_piece.color == player_color:
            return (False, None)
        return (True, (mr, mc))

    # 4) Anything else is illegal
    return (False, None)
