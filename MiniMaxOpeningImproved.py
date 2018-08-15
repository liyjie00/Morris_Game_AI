"""
Generate a move for black in the Opening phase
by using MINIMAX algorithm and an improved static estimation
@author: Yuanjie Li, yxl174431@utdallas.edu
"""

import sys

import MorrisGame


def MaxMinOpeningImproved(board, depth):
    """ use MINIMAX algorithm and an improved estimation to choose the move for 'MAX' """

    if depth == 0:
        board.value = openingStaticImproved(board.position)
        MorrisGame.numEvaluate += 1
        return board
    else:
        board.child = MorrisGame.genMoveOpening(board.position)

        maxValue = float('-inf')
        retBoard = None
        for child in board.child:
            result = MinMaxOpeningImproved(child, depth - 1)
            if maxValue < result.value:
                maxValue = result.value
                retBoard = child
                retBoard.value = maxValue
        return retBoard


def MinMaxOpeningImproved(board, depth):
    """ use MINIMAX algorithm and an improved estimation to choose the move for 'MIN' """

    if depth == 0:
        board.value = openingStaticImproved(board.position)
        MorrisGame.numEvaluate += 1
        return board
    else:
        board.child = MorrisGame.genMoveOpeningBlack(board.position)

        minValue = float('inf')
        retBoard = None
        for child in board.child:
            result = MaxMinOpeningImproved(child, depth - 1)
            if minValue > result.value:
                minValue = result.value
                retBoard = child
                retBoard.value = minValue
        return retBoard


def openingStaticImproved(position):
    """ improve the static estimation by adding the number of potential mills and number of double mills """

    piecesDiff = MorrisGame.openingStatic(position)
    num2PiecesConf = count2PiecesConf(position)
    if num2PiecesConf >= 2:
        num3PiecesConf = num2PiecesConf - 1
    else:
        num3PiecesConf = 0

    # staticEs = 6 * piecesDiff + 12 * num2PiecesConf + 7 * num3PiecesConf + 26 * countMills(position)
    # staticEs = piecesDiff + 6 * num2PiecesConf
    staticEs = piecesDiff + 2 * num2PiecesConf + 10 * num3PiecesConf
    return staticEs


def isMill(position, loc, locList):
    if position[loc] == position[locList[0]] and position[loc] == position[locList[1]]:
        return True


def countMills(position):
    pos = position[:]
    length = len(pos)
    numMills = 0
    for i in range(length):
        if position[i] == 'W':
            millPos = MorrisGame.mills[i]
            for mill in millPos:
                # if the current move is in a mill which is not visited, increase the num,
                # and change the moves on the mill into '*' to denoted the mill is visited.
                if isMill(position, i, mill) and (pos[i] != '*' or pos[mill[0]] != '*' or pos[mill[1]] != '*'):
                    numMills += 1
                    pos = pos[:i] + '*' + pos[i+1:]
                    pos = pos[:mill[0]] + '*' + pos[mill[0]+1:]
                    pos = pos[:mill[1]] + '*' + pos[mill[1]+1:]

    pos2 = position[:]
    num2 = 0
    for i in range(length):
        if position[i] == 'B':
            millPos = MorrisGame.mills[i]
            for mill in millPos:
                # if the current move is in a mill which is not visited, increase the num,
                # and change the moves on the mill into '*' to denoted the mill is visited.
                if isMill(position, i, mill) and (pos2[i] != '*' or pos2[mill[0]] != '*' or pos2[mill[1]] != '*'):
                    num2 += 1
                    pos2 = pos2[:i] + '*' + pos2[i+1:]
                    pos2 = pos2[:mill[0]] + '*' + pos2[mill[0]+1:]
                    pos2 = pos2[:mill[1]] + '*' + pos2[mill[1]+1:]

    return numMills - num2


def count2PiecesConf(position):
    """ count the number of potential mills (2 white pieces and an empty slot) """

    # num = 0
    # length = len(position)
    # for i in range(length):
    #     if position[i] == 'x':
    #         millPos = MorrisGame.mills[i]
    #         for m in millPos:
    #             if position[m[0]] == 'W' and position[m[1]] == 'W':
    #                 num += 1
    # return num
    return count2PiecesW(position) - count2PiecesB(position)


def count2PiecesW(position):
    num = 0
    length = len(position)
    for i in range(length):
        if position[i] == 'x':
            millPos = MorrisGame.mills[i]
            for m in millPos:
                if position[m[0]] == 'W' and position[m[1]] == 'W':
                    num += 1

    return num

def count2PiecesB(position):
    num = 0
    length = len(position)
    for i in range(length):
        if position[i] == 'x':
            millPos = MorrisGame.mills[i]
            for m in millPos:
                if position[m[0]] == 'B' and position[m[1]] == 'B':
                    num += 1
    return num


def main():
    inFileName, outFileName, depth = sys.argv[1], sys.argv[2], int(sys.argv[3])
    root = MorrisGame.readFromFile(inFileName)

    result = MaxMinOpeningImproved(root, depth)

    print('Initial position:', root.position, 'Output position: ', result.position)
    print('Position evaluated by static estimation: ', MorrisGame.numEvaluate)
    print('MINIMAX estimate: ', result.value)

    MorrisGame.write2File(outFileName, result.position)


if __name__ == '__main__':
    main()
