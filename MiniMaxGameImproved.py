"""
Generate a move for black in the MidGame and Endgame Phases
by using MINIMAX algorithm and an improved static estimation
@author: Yuanjie Li, yxl174431@utdallas.edu
"""

import sys, time

import MorrisGame


def MaxMinMidEndImproved(board, depth):
    numWhite = MorrisGame.countNums(board.position)[0]
    if depth == 0 or numWhite < 3:
        board.value = staticMidEndImproved(board.position, depth)
        MorrisGame.numEvaluate += 1
        return board
    else:
        board.child = MorrisGame.genMoveMidEnd(board.position)

        maxValue = float('-inf')
        retBoard = None
        for child in board.child:
            result = MinMaxMidEndImproved(child, depth - 1)
            if maxValue < result.value:
                maxValue = result.value
                retBoard = child
                retBoard.value = maxValue
        return retBoard


def MinMaxMidEndImproved(board, depth):
    numBlack = MorrisGame.countNums(board.position)[1]
    if depth == 0 or numBlack < 3:
        board.value = staticMidEndImproved(board.position, depth)
        MorrisGame.numEvaluate += 1
        return board
    else:
        board.child = MorrisGame.genMoveMidEndBlack(board.position)

        minValue = float('inf')
        retBoard = None
        for child in board.child:
            result = MaxMinMidEndImproved(child, depth - 1)
            if minValue > result.value:
                minValue = result.value
                retBoard = child
                retBoard.value = minValue
        return retBoard


# def staticMidEndImproved(position, depth):
#     """ improved the static estimation by adding the number of potential mills and number of double mills """
#     static = MorrisGame.staticMidEnd(position)
#     numWhite, numBlack = MorrisGame.countNums(position)
#
#     num2PiecesConf = count2PiecesConf(position)
#     if static == 10000:
#         static *= (depth + 1)
#     staticEs = static + 3000 * doubleMills(position) + 500 * num2PiecesConf
#     # staticEs = static + 2000 * num2PiecesConf + 3000 * num3PiecesConf
#     return staticEs
#
#
def doubleMills(position):
    num = 0
    length = len(position)
    for i in range(length):
        if position[i] == 'W':
            if MorrisGame.closeMill(i, position):
                neList = MorrisGame.neighbor[i]
                for n in neList:
                    if position[n] == 'x':
                        pos = position[:n] + 'W' + position[n+1:]
                        if MorrisGame.closeMill(n, pos):
                            num += 1
    return num


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
    return numMills


def staticMidEndImproved(position, depth):
    """ improved the static estimation by adding the number of potential mills and number of double mills """
    static = MorrisGame.staticMidEnd(position)

    num2PiecesConf = count2PiecesConf(position)
    if num2PiecesConf >= 2:
        num3PiecesConf = num2PiecesConf - 1
    else:
        num3PiecesConf = 0
    if static == 10000:
        static *= (depth + 1)
    # # staticEs = static + 200 * num2PiecesConf
    # # staticEs = static + 200 * countMills(position) + 200 * num2PiecesConf + 100 * num3PiecesConf + 400 * doubleMills(position)
    staticEs = static + 100 * countMills(position) + 300 * doubleMills(position)
    # staticEs = static + 200 * num2PiecesConf + 300 * num3PiecesConf
    return staticEs


def count2PiecesConf(position):
    """ count the number of potential mills (2 white pieces and an empty slot) """

    num = 0
    length = len(position)
    for i in range(length):
        # if position[i] == 'x':
        #     millPos = MorrisGame.mills[i]
        #     for m in millPos:
        #         if position[m[0]] == 'W' and position[m[1]] == 'W':
        #             num += 1
        if position[i] == 'W':
            millPos = MorrisGame.mills[i]
            for m in millPos:
                if (position[m[0]] == 'x' and position[m[1]] == 'W') or (position[m[1]] == 'x' and position[m[0]] == 'W'):
                    num += 1
    return num


def main():
    inFileName, outFileName, depth = sys.argv[1], sys.argv[2], int(sys.argv[3])
    root = MorrisGame.readFromFile(inFileName)

    result = MaxMinMidEndImproved(root, depth)

    print('Initial position:', root.position, 'Output position: ', result.position)
    print('Position evaluated by static estimation: ', MorrisGame.numEvaluate)
    print('MINIMAX estimate: ', result.value)

    MorrisGame.write2File(outFileName, result.position)


if __name__ == '__main__':
    main()
