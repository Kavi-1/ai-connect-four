"""
 A Connect-Four Player class 
"""

from .board import Board

class Player:
    """ blueprint for Player objects """
    
    def __init__(self, checker):
        """ constructs a new player with checker and num_moves attributes """
        assert(checker == 'X' or checker == 'O')
        self.checker = checker
        self.num_moves = 0
    
    def __repr__ (self):
        """ returns a String representing a Player Object """
        return "Player " + self.checker
    
    def opponent_checker(self):
        """ returns a String of the checker of the self Player object's opponent """
        if self.checker == 'X':
            return 'O'
        else:
            return 'X'
    
    def next_move(self, b):
        """ Get a next move for this player that is valid for the board b """
        self.num_moves += 1      
        while True:
            col = int(input("Enter a column: "))
            if b.can_add_to(col):
                return col
            else:
                print("Try again!\n")
    
        
      