"""
Generate a move for white in the Opening phase
by using Alpha-Beta pruning algorithm
@author: Yuanjie Li, yxl174431@utdallas.edu
"""

import sys

import MorrisGame


def MaxMinABOpening(board, depth, alpha, beta):
    """ use Alpha-Beta pruning to choose the move for 'MAX' """

    if depth == 0:
        board.value = MorrisGame.openingStatic(board.position)
        MorrisGame.numEvaluate += 1
        return board
    else:
        board.child = MorrisGame.genMoveOpening(board.position)

        maxValue = float('-inf')
        retBoard = None
        for child in board.child:
            result = MinMaxABOpening(child, depth - 1, alpha, beta)
            if maxValue < result.value:
                maxValue = result.value
                retBoard = child
                retBoard.value = maxValue
            if maxValue >= beta:
                return retBoard
            else:
                if maxValue > alpha:
                    alpha = maxValue
        return retBoard


def MinMaxABOpening(board, depth, alpha, beta):
    """ use Alpha-Beta pruning to choose the move for 'MIN' """

    if depth == 0:
        board.value = MorrisGame.openingStatic(board.position)
        MorrisGame.numEvaluate += 1
        return board
    else:
        board.child = MorrisGame.genMoveOpeningBlack(board.position)

        minValue = float('inf')
        retBoard = None
        for child in board.child:
            result = MaxMinABOpening(child, depth - 1, alpha, beta)
            if minValue > result.value:
                minValue = result.value
                retBoard = child
                retBoard.value = minValue
            if minValue <= alpha:
                return retBoard
            elif minValue < beta:
                beta = minValue
        return retBoard


def main():
    inFileName, outFileName, depth = sys.argv[1], sys.argv[2], int(sys.argv[3])
    root = MorrisGame.readFromFile(inFileName)

    result = MaxMinABOpening(root, depth, float('-inf'), float('inf'))

    print('Initial position:', root.position, 'Output position: ', result.position)
    print('Position evaluated by static estimation: ', MorrisGame.numEvaluate)
    print('MINIMAX estimate: ', result.value)

    MorrisGame.write2File(outFileName, result.position)


if __name__ == '__main__':
    main()
