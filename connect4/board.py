
"""
 A Connect Four Board class
"""

class Board:
    """ a data type for a Connect Four board with arbitrary dimensions
    """   
        
    def __init__(self, height, width):
        """ constructs a new board object """
        self.height = height
        self.width = width
        self.slots = [[' '] * self.width for row in range(self.height)]

    def __repr__(self):
        """ Returns a string that represents a Board object.
        """
        s = ''         #  begin with an empty string

        # add one row of slots at a time to s
        for row in range(self.height):
            s += '|'   # one vertical bar at the start of the row

            for col in range(self.width):
                s += self.slots[row][col] + '|'

            s += '\n'  # newline at the end of the row

        loop_times = 2 * self.width + 1
        for i in range(loop_times):
            s += '-'
        s += '\n'
        
        s += ' '
        for col in range(self.width):
            col %= 10
            s += (str(col) + ' ')
        s += '\n'        
        return s

    def add_checker(self, checker, col):
        """ adds the specified checker (either 'X' or 'O') to the
            column with the specified index col in the called Board.
            inputs: checker is either 'X' or 'O'
                    col is a valid column index
        """
        assert(checker == 'X' or checker == 'O')
        assert(col >= 0 and col < self.width)
        
        for row in range(self.height):
            if (self.slots[self.height - 1 - row][col] == ' '): # start at bottom row
                self.slots[self.height - 1 - row][col] = checker          
                break

    def reset(self):
        """ resets the Board object by setting all slots to empty """
        for row in range(self.height):
            for col in range(self.width):
                self.slots[row][col] = ' '
    
    def add_checkers(self, colnums):
        """ takes a string of column numbers and places alternating
            checkers in those columns of the called Board object,
            starting with 'X'.
            input: colnums is a string of valid column numbers
        """
        checker = 'X'   # start by playing 'X'

        for col_str in colnums:
            col = int(col_str)
            if 0 <= col < self.width:
                self.add_checker(checker, col)

            if checker == 'X':
                checker = 'O'
            else:
                checker = 'X'
    
    def can_add_to(self, col):
        """ returns True/False whether checker can be added to column col """
        if (col < 0 or col > self.width - 1):
            return False
        for row in range(self.height):
            if self.slots[row][col] == ' ':
                return True
        return False
        
    def is_full(self):
        """ returns True/False whether Board object is all full of checkers """
        for col in range(self.width):
            if self.can_add_to(col):
                return False
        return True
        
    def remove_checker(self, col):
        """Remove the top checker from column col (if any)."""
        # column empty? nothing to do
        # The bottom slot is at index self.height - 1. If it's empty,
        # the column has no checkers.
        if self.slots[self.height - 1][col] == ' ':
            return
        # remove the first non-empty from the top (the highest occupied slot)
        for row in range(self.height):
            if self.slots[row][col] != ' ':
                self.slots[row][col] = ' '
                return
 
    def is_win_for(self, checker):
        """ returns True/False whether 4 consecutive slots contain checker """
        assert(checker == 'X' or checker == 'O')
        # call the helper functions and use their return values to
        # determine whether to return True or False  
        return self.is_horizontal_win(checker) or \
               self.is_vertical_win(checker) or \
               self.is_down_diagonal_win(checker) or \
               self.is_up_diagonal_win(checker)                            
        
    def is_horizontal_win(self, checker):
        """ Checks for a horizontal win for the specified checker.
        """
        for row in range(self.height):
            for col in range(self.width - 3):
                # Check if the next four columns in this row
                # contain the specified checker.
                if self.slots[row][col] == checker and \
                   self.slots[row][col + 1] == checker and \
                   self.slots[row][col + 2] == checker and \
                   self.slots[row][col + 3] == checker:
                    return True
    
        # if we make it here, there were no horizontal wins
        return False
    
    def is_vertical_win(self, checker):
        """ Checks for a vertical win for the specified checker.
        """
        for row in range(self.height - 3):
            for col in range(self.width):
                if self.slots[row][col] == checker and \
                   self.slots[row + 1][col] == checker and \
                   self.slots[row + 2][col] == checker and \
                   self.slots[row + 3][col] == checker:
                       return True
        return False
    
    def is_down_diagonal_win(self, checker):
        """ Checks for a down diagonal win for the specified checker """
        for row in range(self.height - 3):
            for col in range(self.width - 3):
                if self.slots[row][col] == checker and \
                   self.slots[row +1][col + 1] == checker and \
                   self.slots[row + 2][col + 2] == checker and \
                   self.slots[row + 3][col + 3] == checker:
                       return True
        return False
    
    def is_up_diagonal_win(self, checker):
        """ Checks for a up diagonal win for the specified checker """
        for row in range(self.height - 3):
            for col in range(self.width - 3):
                if self.slots[self.height - 1 - row][col] == checker and \
                   self.slots[self.height - 2 - row][col + 1] == checker and \
                   self.slots[self.height - 3 - row][col + 2] == checker and \
                   self.slots[self.height - 4 - row][col + 3] == checker:
                       return True
        return False
        
    def copy(self):
        b2 = Board(self.height, self.width)
        b2.slots = [row[:] for row in self.slots]
        return b2

        
        
        
        
        
        
        
        
        
        
        
        
        
        