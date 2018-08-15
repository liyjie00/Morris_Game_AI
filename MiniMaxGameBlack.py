"""
Generate a move for black in the Midgame and Endgame phases
by using MINIMAX algorithm
@author: Yuanjie Li, yxl174431@utdallas.edu
"""

import sys

import MorrisGame
from MiniMaxGame import MaxMinMidEnd, MinMaxMidEnd


def MiniMaxGameBlack(root, depth):
    """ use MINIMAX algorithm to generate a move for black """

    # reverse the board
    root.position = MorrisGame.reverse(root.position)

    result = MaxMinMidEnd(root, depth)

    # reverse the result
    result.position = MorrisGame.reverse(result.position)
    root.position = MorrisGame.reverse(root.position)

    return result


def main():
    # inFileName, outFileName, depth = 'board3.txt', '1.txt', int('4')
    inFileName, outFileName, depth = sys.argv[1], sys.argv[2], int(sys.argv[3])
    root = MorrisGame.readFromFile(inFileName)

    result = MiniMaxGameBlack(root, depth)

    print('Initial position:', root.position, 'Output position: ', result.position)
    print('Position evaluated by static estimation: ', MorrisGame.numEvaluate)
    print('MINIMAX estimate: ', result.value)

    MorrisGame.write2File(outFileName, result.position)
    # print(root)

if __name__ == '__main__':
    main()
