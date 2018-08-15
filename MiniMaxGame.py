"""
Generate a move for white in the Midgame and Endgame phases
by using MINIMAX algorithm
@author: Yuanjie Li, yxl174431@utdallas.edu
"""
import sys

import MorrisGame


def MaxMinMidEnd(board, depth):
    """ use MINIMAX algorithm to choose the move for 'MAX' """

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
            result = MinMaxMidEnd(child, depth - 1)
            if maxValue < result.value:
                # retBoard = result   # for test

                maxValue = result.value
                retBoard = child
                retBoard.value = maxValue
        return retBoard


def MinMaxMidEnd(board, depth):
    """ use MINIMAX algorithm to choose the move for 'MIN' """

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
            result = MaxMinMidEnd(child, depth - 1)
            if minValue > result.value:
                # retBoard = result   # for test

                minValue = result.value
                retBoard = child
                retBoard.value = minValue
        return retBoard


def main():
    inFileName, outFileName, depth = sys.argv[1], sys.argv[2], int(sys.argv[3])
    # inFileName, outFileName, depth = 'board3.txt', '1.txt', 1
    root = MorrisGame.readFromFile(inFileName)

    # print(MorrisGame.staticMidEnd(root.position))

    result = MaxMinMidEnd(root, depth)
    # result = MinMaxMidEnd(root, depth)

    print('Initial position:', root.position, 'Output position: ', result.position)
    print('Position evaluated by static estimation: ', MorrisGame.numEvaluate)
    print('MINIMAX estimate: ', result.value)

    MorrisGame.write2File(outFileName, result.position)


if __name__ == '__main__':
    main()
