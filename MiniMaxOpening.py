"""
Generate a move for white in the opening phase
by using MINIMAX algorithm
@author: Yuanjie Li, yxl174431@utdallas.edu
"""

import sys

import MorrisGame


def MaxMinOpening(board, depth):
    """ use MINIMAX algorithm to choose the move for 'MAX' """
    if depth == 0:
        board.value = MorrisGame.openingStatic(board.position)
        MorrisGame.numEvaluate += 1
        return board
    else:
        board.child = MorrisGame.genMoveOpening(board.position)

        maxValue = float('-inf')
        retBoard = None
        for child in board.child:
            result = MinMaxOpening(child, depth - 1)
            if maxValue < result.value:
                # retBoard = result # for test
                maxValue = result.value
                retBoard = child
                retBoard.value = maxValue
        return retBoard


def MinMaxOpening(board, depth):
    """ use MINIMAX algorithm to choose the move for 'MIN' """
    if depth == 0:
        board.value = MorrisGame.openingStatic(board.position)
        MorrisGame.numEvaluate += 1
        return board
    else:
        board.child = MorrisGame.genMoveOpeningBlack(board.position)

        minValue = float('inf')
        retBoard = None
        for child in board.child:
            result = MaxMinOpening(child, depth - 1)
            if minValue > result.value:
                retBoard = result   # for test
                minValue = result.value
                retBoard = child
                retBoard.value = minValue
        return retBoard


def main():
    # inFileName, outFileName, depth = 'board1.txt', 'board2.txt', 5    # for test

    inFileName, outFileName, depth = sys.argv[1], sys.argv[2], int(sys.argv[3])
    root = MorrisGame.readFromFile(inFileName)

    result = MaxMinOpening(root, depth)

    print('Initial position:', root.position, 'Output position: ', result.position)
    print('Position evaluated by static estimation: ', MorrisGame.numEvaluate)
    print('MINIMAX estimate: ', result.value)

    MorrisGame.write2File(outFileName, result.position)


if __name__ == '__main__':
    main()
