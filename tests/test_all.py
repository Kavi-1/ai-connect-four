"""
    tests using pytest
"""

from connect4.board import Board
from connect4.ai_player import AIPlayer


def test_add_and_remove_checker():
    b = Board(6, 7)
    b.add_checker('X', 0)
    assert b.slots[5][0] == 'X'
    b.remove_checker(0)
    assert b.slots[5][0] == ' '


def test_can_add_to_and_is_full():
    b = Board(2, 2)
    assert b.can_add_to(0)
    assert b.can_add_to(1)
    b.add_checker('X', 0)
    b.add_checker('O', 0)
    assert not b.can_add_to(0)
    assert b.can_add_to(1)
    b.add_checker('X', 1)
    b.add_checker('O', 1)
    assert b.is_full()


def test_horizontal_win():
    b = Board(6, 7)
    b.add_checker('X', 0)
    b.add_checker('X', 1)
    b.add_checker('X', 2)
    b.add_checker('X', 3)
    assert b.is_horizontal_win('X')
    assert b.is_win_for('X')


def test_vertical_win():
    b = Board(6, 7)
    for _ in range(4):
        b.add_checker('O', 4)
    assert b.is_vertical_win('O')
    assert b.is_win_for('O')


def test_down_diagonal_win():
    b = Board(6, 7)
    b.add_checker('X', 0)
    b.add_checker('O', 1)
    b.add_checker('X', 1)
    b.add_checker('O', 2)
    b.add_checker('O', 2)
    b.add_checker('X', 2)
    b.add_checker('O', 3)
    b.add_checker('O', 3)
    b.add_checker('O', 3)
    b.add_checker('X', 3)
    assert b.is_up_diagonal_win('X') or b.is_down_diagonal_win('X')
    assert b.is_win_for('X')


def test_up_diagonal_win():
    b = Board(6, 7)
    b.add_checker('O', 0)
    b.add_checker('X', 1)
    b.add_checker('O', 1)
    b.add_checker('X', 2)
    b.add_checker('X', 2)
    b.add_checker('O', 2)
    b.add_checker('X', 3)
    b.add_checker('X', 3)
    b.add_checker('X', 3)
    b.add_checker('O', 3)
    assert b.is_up_diagonal_win('O')
    assert b.is_win_for('O')


def test_add_checkers_and_copy():
    b = Board(6, 7)
    b.add_checkers('0123')
    assert b.slots[5][0] in ('X', 'O')
    b2 = b.copy()
    b2.add_checker('X', 6)
    assert b.slots[5][6] == ' '


def test_ai_next_move_minimax_blocks():
    b = Board(6, 7)
    b.add_checker('X', 0)
    b.add_checker('X', 1)
    b.add_checker('X', 2)
    ai = AIPlayer('O', 'LEFT', 2, algo='MINIMAX')
    col = ai.next_move(b)
    assert 0 <= col < b.width
    assert col == 3


def test_ai_next_move_alphabeta_blocks():
    b = Board(6, 7)
    b.add_checker('X', 0)
    b.add_checker('X', 1)
    b.add_checker('X', 2)
    ai = AIPlayer('O', 'LEFT', 2, algo='ALPHABETA')
    col = ai.next_move(b)
    assert 0 <= col < b.width
    assert col == 3


def test_ai_returns_valid_on_empty_board():
    b = Board(6, 7)
    ai = AIPlayer('X', 'LEFT', 1, algo='MINIMAX')
    col = ai.next_move(b)
    assert 0 <= col < b.width
