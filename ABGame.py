"""
Generate a move for white in the Midgmae and Endgame phases
by using Alpha-Beta pruning algorithm
@author: Yuanjie Li, yxl174431@utdallas.edu
"""

import sys

import MorrisGame


def MaxMinABMidEnd(board, depth, alpha, beta):
    """ use Alpha-Beta pruning to choose the move for 'MAX' """

    numWhite = MorrisGame.countNums(board.position)[0]
    if depth == 0 or numWhite < 3:
        board.value = MorrisGame.staticMidEnd(board.position)
        MorrisGame.numEvaluate += 1
        return board
    else:
        board.child = MorrisGame.genMoveMidEnd(board.position)

        maxValue = float('-inf')
        retBoard = None
        for child in board.child:
            result = MinMaxABMidEnd(child, depth - 1, alpha, beta)
            if maxValue < result.value:
                maxValue = result.value
                retBoard = child
                retBoard.value = maxValue
            if maxValue >= beta:
                return retBoard
            elif maxValue > alpha:
                alpha = maxValue
        return retBoard


def MinMaxABMidEnd(board, depth, alpha, beta):
    """ use Alpha-Beta pruning to choose the move for 'MIN' """

    numBlack = MorrisGame.countNums(board.position)[1]
    if depth == 0 or numBlack < 3:
        board.value = MorrisGame.staticMidEnd(board.position)
        MorrisGame.numEvaluate += 1
        return board
    else:
        board.child = MorrisGame.genMoveMidEndBlack(board.position)

        minValue = float('inf')
        retBoard = None
        for child in board.child:
            result = MaxMinABMidEnd(child, depth - 1, alpha, beta)
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

    result = MaxMinABMidEnd(root, depth, float('-inf'), float('inf'))

    print('Initial position:', root.position, 'Output position: ', result.position)
    print('Position evaluated by static estimation: ', MorrisGame.numEvaluate)
    print('MINIMAX estimate: ', result.value)

    MorrisGame.write2File(outFileName, result.position)


if __name__ == '__main__':
    main()
