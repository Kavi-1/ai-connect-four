"""
AI Player for use in Connect Four  
"""

import random
from .connect_four import *


class AIPlayer(Player):
    """ subclass of Player class that represents an intelligent computer player;
        Inherits from Player """
    
    def __init__(self, checker, tiebreak, lookahead, algo='MINIMAX'):
        """ contructs a AI player Object with checker, num_moves,
            tiebreak, and lookahead attributes 
        """
        assert(checker == 'X' or checker == 'O')
        assert(tiebreak == 'LEFT' or tiebreak == 'RIGHT' or tiebreak == 'RANDOM')
        assert(lookahead >= 0)
        super().__init__(checker)
        self.tiebreak = tiebreak
        self.lookahead = lookahead
        # algo may be 'MINIMAX' or 'ALPHABETA'
        self.algo = algo
         
    def __repr__(self):
        """ Overrides Player __repr__ method;
            returns a string representing an AIPlayer Ojbect """
        return super().__repr__() + " ("  + self.tiebreak + ", " + str(self.lookahead) + ")"
       
    def max_score_column(self, scores):
        """ takes a list scores and returns the index of the column with a max score """   
        max_score = max(scores)
        max_score_indices = []
        for i in range(len(scores)):
            if scores[i] == max_score:
                max_score_indices += [i]
        if self.tiebreak == "LEFT":
            return max_score_indices[0]
        elif self.tiebreak == "RIGHT":
            return max_score_indices[-1]
        return random.choice(max_score_indices)
    
    def minimax(self, board, depth, player_checker):
        """Return -1/0/1 for loss/neutral/win from this AI's perspective using plain minimax.

        player_checker indicates whose turn it is on 'board'.
        """
        # terminal states
        if board.is_win_for(self.checker):
            return 1
        if board.is_win_for(self.opponent_checker()):
            return -1
        if depth == 0:
            return 0

        if player_checker == self.checker:
            # max player
            best = -2
            for c in range(board.width):
                if not board.can_add_to(c):
                    continue
                nb = board.copy()
                nb.add_checker(player_checker, c)
                val = self.minimax(nb, depth - 1, self.opponent_checker())
                if val > best:
                    best = val
                    if best == 1:
                        break
            return best
        else:
            # min player 
            best = 2
            for c in range(board.width):
                if not board.can_add_to(c):
                    continue
                nb = board.copy()
                nb.add_checker(player_checker, c)
                val = self.minimax(nb, depth - 1, self.checker)
                if val < best:
                    best = val
                    if best == -1:
                        break
            return best

    def alphabeta(self, board, depth, player_checker, alpha, beta):
        """Return -1/0/1 using negamax-style alpha-beta (player_checker's turn).

        alpha/beta are bounds in the same -2..2 domain.
        """
        # terminal 
        if board.is_win_for(self.checker):
            return 1
        if board.is_win_for(self.opponent_checker()):
            return -1
        if depth == 0:
            return 0

        if player_checker == self.checker:
            # max
            value = -2
            for c in range(board.width):
                if not board.can_add_to(c):
                    continue
                nb = board.copy()
                nb.add_checker(player_checker, c)
                val = self.alphabeta(nb, depth - 1, self.opponent_checker(), alpha, beta)
                if val > value:
                    value = val
                if value > alpha:
                    alpha = value
                if alpha >= beta:
                    break
            return value
        else:
            # min
            value = 2
            for c in range(board.width):
                if not board.can_add_to(c):
                    continue
                nb = board.copy()
                nb.add_checker(player_checker, c)
                val = self.alphabeta(nb, depth - 1, self.checker, alpha, beta)
                if val < value:
                    value = val
                if value < beta:
                    beta = value
                if alpha >= beta:
                    break
            return value
    def scores_for(self, b):
        """Return a list of scores for each column on board b using plain minimax.

        This implements a simple depth-limited minimax (no alpha-beta). The
        minimax value domain is {-1, 0, 1} (loss/neutral/win) from this AI's
        perspective. We map those to the existing score scale {0,50,100} so the
        rest of the code (max_score_column) remains unchanged.
        """

        scores = [0] * b.width
        for col in range(b.width):
            if not b.can_add_to(col):
                scores[col] = -1
                continue

            nb = b.copy()
            nb.add_checker(self.checker, col)

            if nb.is_win_for(self.checker):
                scores[col] = 100
            elif self.lookahead == 0:
                scores[col] = 50
            else:
                if getattr(self, 'algo', 'MINIMAX') == 'ALPHABETA':
                    val = self.alphabeta(nb, self.lookahead - 1, self.opponent_checker(), -2, 2)
                else:
                    val = self.minimax(nb, self.lookahead - 1, self.opponent_checker())
                if val > 0:
                    scores[col] = 100
                elif val < 0:
                    scores[col] = 0
                else:
                    scores[col] = 50

        return scores

    def next_move(self, b):
        """Overrides Player.next_move: return this AI's chosen column."""
        self.num_moves += 1
        return self.max_score_column(self.scores_for(b))


