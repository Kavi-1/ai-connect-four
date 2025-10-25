"""
Playing the game 
"""

from .board import Board
from .player import Player
import random
    
def connect_four(p1, p2):
    """ Plays a game of Connect Four between the two specified players,
        and returns the Board object as it looks at the end of the game.
        inputs: p1 and p2 are objects representing Connect Four
          players (objects of the class Player or a subclass of Player).
          One player should use 'X' checkers and the other player should
          use 'O' checkers.
    """
    # Make sure one player is 'X' and one player is 'O'.
    if p1.checker not in 'XO' or p2.checker not in 'XO' \
       or p1.checker == p2.checker:
        print('need one X player and one O player.')
        return None

    print('Welcome to Connect Four!')
    print()
    b = Board(6, 7)
    print(b)
    
    while True:
        if process_move(p1, b) == True:
            return b

        if process_move(p2, b) == True:
            return b

def process_move(p, b):
    """ process a single move by player p on board b """
    print(str(p) + "'s turn")
    print()
    col = p.next_move(b) # column number for next move
    b.add_checker(p.checker, col)
    print()
    print(b)
    if b.is_win_for(p.checker):
        print(str(p) + " wins in", p.num_moves, "moves\nCongratulations!")
        return True
    elif b.is_full():
        print("It's a tie!")
        return True
    return False
        
class RandomPlayer(Player):
    """ subclass of Player class that represents an untelligent computer player;
        Inherits from Player """
    
    def next_move(self, b):
        """ overrides next_move method from Player; chooses a random col """
        self.num_moves += 1
        available_cols = [col for col in range(b.width) if b.can_add_to(col)]
        return random.choice(available_cols)
        
        
        










