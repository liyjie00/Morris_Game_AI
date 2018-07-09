import time
import sys

import MorrisGame

numWhite = 0
numBlack = 0
numEvaluate = 0


def openingStatic(position):
    countNums(position)
    return numWhite - numBlack


def countNums(position):
    global numWhite, numBlack
    numWhite = 0
    numBlack = 0
    for pos in position:
        if pos == 'W':
            numWhite += 1
        elif pos == 'B':
            numBlack += 1


def MiniMaxOpening(board, depth):
    global numEvaluate

    if depth == 0:
        board.value = openingStatic(board.position)
        numEvaluate += 1
        return board
    else:
        board.child = MorrisGame.genMoveOpening(board)

    max = float('-inf')
    retBoard = None
    for child in board.child:
        result = MiniMaxOpeningBlack(child, depth - 1)
        if max < result.value:
            # retBoard = result
            max = result.value

            retBoard = child
            retBoard.value = max
    return retBoard


def MiniMaxOpeningBlack(board, depth):
    global numEvaluate

    if depth == 0:
        board.value = openingStatic(board.position)
        numEvaluate += 1
        return board
    else:
        board.child = MorrisGame.genMoveOpeningBlack(board)

    min = float('inf')
    retBoard = None
    for child in board.child:
        result = MiniMaxOpening(child, depth - 1)
        if min > result.value:
            # retBoard = result
            min = result.value

            retBoard = child
            retBoard.value = min
    return retBoard


def main():
    # inFileName, outFileName, searchDepth = sys.argv[0], sys.argv[1], int(sys.argv[2])

    inFileName, outFileName, depth = 'board1.txt', 'board2.txt', 2
    initPos = MorrisGame.readFromFile(inFileName)
    inputBoard = MorrisGame.BoardNode(initPos)

    tStart = time.time()
    result = MiniMaxOpening(inputBoard, depth)
    tEnd = time.time()
    t = tEnd - tStart

    print('Initial position:', inputBoard.position, 'Output position: ', result.position)
    print('Position evaluated by static estimation: ', numEvaluate)
    print('MINIMAX estimate: ', result.value)

    print('time = ', t)

    # print(inputBoard)


if __name__ == '__main__':
    main()
