import numpy as np
from .Digits import int2base

"""
Random and Human-ineracting players for the game of TicTacToe.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the OthelloPlayers by Surag Nair.

"""
class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a


class HumanAlquerquePlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        jump = False
        valid = self.game.getValidMoves(board, 1)

        for i in range(len(valid)):
            if valid[i]:
                if len(int2base(i,self.game.n,4)) == 5:
                    jump = True
                else:
                    print(int2base(i,self.game.n,4))

        if jump:
            return self.game.getActionSize() - 1
        else:
            while True:
                a = input()

                x1,y1,x2,y2 = [int(x) for x in a.strip().split(' ')]
                a = x1 + y1 * self.game.n + x2 * self.game.n**2 + y2 * self.game.n**3 
                
                if valid[a]:
                    break
                else:
                    print('Invalid')

        return a
