from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .AlquerqueLogic import Board
import numpy as np
from .Digits import int2base
import time

"""
Game class implementation for the game of Alquerque de Doce.

Author: Francisco Rodríguez Cuenca, github.com/francisco-rodriguez-cuenca
Date: Jul 25, 2022.

Based on the OthelloGame by Surag Nair and tictacToe by Evgeny Tyurin.
"""
class AlquerqueGame(Game):
    def __init__(self):
        self.n = 5

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board()
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n+1, self.n)

    def getActionSize(self):
        # return number of actions
        return self.n**4 + 1

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        b = Board()
        b.pieces = np.copy(board)

        if action < self.getActionSize()-1: #The last action is passing
            move = int2base(action,self.n,4)
            b.execute_move(move, player)
        elif b.pieces[5][0]<0: # If the other player just jumped pass and invert the jump index
            b.pieces[5][0] = -b.pieces[5][0]
        elif b.pieces[5][0]>0: #If we jumped but dont have any actions pass and return to normal game
            b.pieces[5][0] = 0

        return (b.pieces, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board()
        b.pieces = np.copy(board)
        legalMoves =  b.get_legal_moves(player)
        if len(legalMoves)==0:
            valids[-1]=1
            return np.array(valids)
        for x1, y1, x2, y2 in legalMoves:
            valids[x1+y1*self.n+x2*self.n**2+y2*self.n**3]=1

        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board()
        b.pieces = np.copy(board)

        if b.is_win(player):
            return 1
        elif b.is_win(-player):
            return -1
        elif b.is_draw():
            return 1e-4
        else:
            return 0


    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        res = np.append(player*board[:self.n], board[self.n:], axis = 0)
        # print(res)
        return res

    def getSymmetries(self, board, pi):
        return [(board,pi)]

        # new_board = board[:self.n]
        # pi_board = np.reshape(pi, (self.n, self.n, self.n, self.n))
        # l = []

        # for i in range(1, 5):
        #     for j in [True, False]:
        #         newB = np.rot90(new_board, i)
        #         newPi = np.rot90(pi_board, i)
        #         newPi = np.rot90(np.array([[np.rot90(y_0, i).tolist() for y_0 in x_0] for x_0 in pi_board]),i)
        #         if j:
        #             newB = np.fliplr(newB)
        #             newPi = np.fliplr(np.array([[np.fliplr(y_0).tolist() for y_0 in x_0] for x_0 in newPi]))
        #         l += [(np.append(newB, board[self.n:], axis = 0), list(newPi.ravel()))]
        # return l
    
    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return board.tostring()

    @staticmethod
    def display(board):

        n = board.shape[1]

        print("   ", end="")
        for y in range(n):
            print (f" {y}","", end=" ")
        print("")
        print("  ", end="")
        for _ in range(n):
            print ("  ", end="  ")
        print("  ")
        for y in range(n):
            print(y, "  ",end="")    # print the row #
            for x in range(n):
                piece = board[y][x]    # get the piece to print
                if piece == -1: print("X ",end="")
                elif piece == 1: print("O ",end="")
                else:
                    if x==n:
                        print(" ",end="")
                    else:
                        print("  ",end="")
                if x<n-1:
                    print("- ",end="")
            print("  ")

            if y < n-1:

                print("    ",end="")

                for x in range(n):
                    print("| ",end="")
                    if x<n-1:

                        if (x + y)%2 == 0:
                            print("\ ",end="")
                        else:
                            print("/ ",end="")


                print("  ")


        print("  ", end="")
        
        for _ in range(n):
            print ("  ", end="  ")
        print("  ")

if __name__ == "__main__":

    b= Board()
    
    g = AlquerqueGame()

    print(g.display(g.getInitBoard()))

    print(
        g.getValidMoves(b, 1)
    )