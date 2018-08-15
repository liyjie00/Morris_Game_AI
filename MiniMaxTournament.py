import time
import sys

# from BoardNode import *


numEvaluate = 0
mills = {0: [[2, 4], [6, 18]],
         1: [[11, 20]],
         2: [[0, 4], [7, 15]],
         3: [[10, 17]],
         4: [[0, 2], [8, 12]],
         5: [[9, 14]],
         6: [[0, 18], [7, 8]],
         7: [[2, 15], [6, 8]],
         8: [[4, 12], [6, 7]],
         9: [[5, 14], [10, 11]],
         10: [[9, 11], [3, 17]],
         11: [[1, 20], [9, 10]],
         12: [[13, 14], [4, 8]],
         13: [[16, 19], [12, 14]],
         14: [[12, 13], [5, 9]],
         15: [[16, 17], [2, 7]],
         16: [[15, 17], [13, 19]],
         17: [[15, 16], [3, 10]],
         18: [[0, 6], [19, 20]],
         19: [[18, 20], [13, 16]],
         20: [[1, 11], [18, 19]],
         }

neighbor = {
         0: [1, 2, 6],
         1: [0, 11],
         2: [0, 3, 4, 7],
         3: [2, 10],
         4: [2, 5, 8],
         5: [4, 9],
         6: [0, 7, 18],
         7: [2, 6, 8, 15],
         8: [4, 7, 12],
         9: [5, 10, 14],
         10: [3, 9, 11, 17],
         11: [1, 10, 20],
         12: [8, 13],
         13: [12, 14, 16],
         14: [9, 13],
         15: [7, 16],
         16: [13, 15, 17, 19],
         17: [10, 16],
         18: [6, 19],
         19: [16, 18, 20],
         20: [11, 19],
         }


class BoardNode(object):
    # __slots__ = ('value', 'position', 'child')

    def __init__(self, position='', lastMove = -1):
        self.value = None
        self.position = position
        self.child = []
        self.lastMove = lastMove

    def __str__(self):
        list = []
        tree = ''
        list.append(self)
        for node in list:
            tree = tree + node.position + ' ' + str(node.value)  + '\n'
            list += node.child
        return tree


def genMoveOpening(position):
    boardList = genAdd(position)
    return boardList


def genAdd(position):
    posList = []
    length = len(position)
    for loc in range(length):
        if position[loc] == 'x':
            newPosition = position[:loc] + 'W' + position[loc + 1:]
            if closeMill(loc, newPosition):
                posList = genRemove(newPosition, posList, loc)
            else:
                posList.append(BoardNode(newPosition, lastMove=loc))
    return posList


def genMoveOpeningBlack(position):
    revPosition = reverse(position)
    posList = genAdd(revPosition)

    for b in posList:
        b.position = reverse(b.position)
    return posList


def reverse(board):
    tempBoard = ''
    for loc in range(len(board)):
        move = board[loc]
        if move == 'W':
            tempBoard += 'B'
        elif move == 'B':
            tempBoard += 'W'
        else:
            tempBoard += move
    return tempBoard


def genRemove(board, posList, loc):
    closeMillFlag = True
    for loc in range(len(board)):
        if board[loc] == 'B':
            if not closeMill(loc, board):
                newBoardPosition = board[:loc] + 'x' + board[loc + 1:]
                posList.append(BoardNode(newBoardPosition, lastMove=loc))
                closeMillFlag = False

    if closeMillFlag:
        posList.append(BoardNode(board, lastMove=loc))

    return posList


def genMoveMidEndBlack(board):
    revPosition = reverse(board)
    posList = genMoveMidEnd(revPosition)

    for b in posList:
        b.position = reverse(b.position)
    return posList


def genMoveMidEnd(position):
    numWhite, numBlack = countNums(position)

    if numWhite == 3:
        return genHopping(position)
    else:
        return genMove(position)


def genHopping(position):
    posList = []
    length = len(position)
    for loc_a in range(length):
        if position[loc_a] == 'W':
            for loc_b in range(length):
                if position[loc_b] == 'x':
                    newPosition = position[:loc_a] + 'x' + position[loc_a + 1:]
                    newPosition = newPosition[:loc_b] + 'W' + newPosition[loc_b + 1:]
                    if closeMill(loc_b, newPosition):
                        posList = genRemove(newPosition, posList, loc_b)
                    else:
                        posList.append(BoardNode(newPosition, lastMove=loc_b))
    return posList


def genMove(position):
    posList = []
    length = len(position)
    for loc in range(length):
        if position[loc] == 'W':
            nList = neighbors(loc)
            for loc_b in nList:
                if position[loc_b] == 'x':
                    newPosition = position[:loc] + 'x' + position[loc+1:]
                    newPosition = newPosition[:loc_b] + 'W' + newPosition[loc_b+1:]
                    if closeMill(loc_b, newPosition):
                        posList = genRemove(newPosition, posList, loc_b)
                    else:
                        posList.append(BoardNode(newPosition, lastMove=loc_b))
    return posList


def neighbors(loc):
    return neighbor[loc]


def readFromFile(fileName):
    file = open(fileName, 'r')
    boardPosition = file.read()
    file.close()
    return BoardNode(boardPosition)


def write2File(newFileName, result):
    newFile = open(newFileName, 'w')
    newFile.write(result)
    newFile.close()


def closeMill(loc, position):
    hasMill = False
    move = position[loc]
    for pos in mills[loc]:
        hasMill = hasMill or (position[pos[0]] == move and position[pos[1]] == move)
    return hasMill


# def openingStatic(position):
#     numWhite, numBlack = countNums(position)
#     return numWhite - numBlack


def countNums(position):
    numWhite = 0
    numBlack = 0
    for pos in position:
        if pos == 'W':
            numWhite += 1
        elif pos == 'B':
            numBlack += 1
    return numWhite, numBlack


# def staticMidEnd(position):
#     revPos = reverse(position)
#     list = genMoveMidEnd(revPos)
#
#     # list = genMoveMidEndBlack(position)
#     numBlackMoves = len(list)
#     numWhite, numBlack = countNums(position)
#
#     if numBlack <= 2:
#         return 10000
#     elif numWhite <= 2:
#         return -10000
#     elif numBlackMoves == 0:
#         return 10000
#     else:
#         return 1000 * (numWhite - numBlack) - numBlackMoves


def getMill(loc):
    return mills[loc]


def isMill(position, loc, locList):
    if position[loc] == position[locList[0]] and position[loc] == position[locList[1]]:
        return True


def closeMorris(loc, position):
    # print(loc)
    # print(position)
    if closeMill(loc, position):
        return 1
    return 0


def countMills(position):
    pos = position[:]
    length = len(pos)
    numMills = 0
    for i in range(length):
        if position[i] == 'W':
            millPos = getMill(i)
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
            millPos = getMill(i)
            for mill in millPos:
                # if the current move is in a mill which is not visited, increase the num,
                # and change the moves on the mill into '*' to denoted the mill is visited.
                if isMill(position, i, mill) and (pos2[i] != '*' or pos2[mill[0]] != '*' or pos2[mill[1]] != '*'):
                    num2 += 1
                    pos2 = pos2[:i] + '*' + pos2[i+1:]
                    pos2 = pos2[:mill[0]] + '*' + pos2[mill[0]+1:]
                    pos2 = pos2[:mill[1]] + '*' + pos2[mill[1]+1:]

    return numMills - num2


def countBlockedOpp(position):
    num = 0
    length = len(position)
    for i in range(length):
        if position[i] == 'B':
            neighborList = neighbor[i]
            isBlock = 1
            for j in neighborList:
                if position[j] == 'W':
                    isBlock = isBlock and True
                else:
                    isBlock = False
            if isBlock:
                num += 1
    num2 = 0
    for i in range(length):
        if position[i] == 'W':
            neighborList = neighbor[i]
            isBlock = 1
            for j in neighborList:
                if position[j] == 'B':
                    isBlock = isBlock and True
                else:
                    isBlock = False
            if isBlock:
                num2 += 1
    return num - num2


def piecesNumber(position):
    numWhite, numBlack = countNums(position)
    return numWhite - numBlack


def count2PiecesConf(position):

    return count2PiecesW(position) - count2PiecesB(position)


def count2PiecesW(position):
    num = 0
    length = len(position)
    for i in range(length):
        if position[i] == 'x':
            millPos = getMill(i)
            for m in millPos:
                if position[m[0]] == 'W' and position[m[1]] == 'W':
                    num += 1

    return num


def count2PiecesB(position):
    num = 0
    length = len(position)
    for i in range(length):
        if position[i] == 'x':
            millPos = getMill(i)
            for m in millPos:
                if position[m[0]] == 'B' and position[m[1]] == 'B':
                    num += 1
    return num


def count3PiecesConf(position):
    num = count2PiecesW(position)
    if num >= 2:
        num -= 1

    num2 = count2PiecesB(position)
    if num2 >= 2:
        num2 -= 1
    return num - num2


def doubleMills(position):
    num = 0
    length = len(position)
    for i in range(length):
        if position[i] == 'W':
            if closeMill(i, position):
                neList = neighbor[i]
                for n in neList:
                    if position[n] == 'x':
                        pos = position[:n] + 'W' + position[n+1:]
                        if closeMill(n, pos):
                            num += 1

    num2 = 0
    for i in range(length):
        if position[i] == 'B':
            if closeMill(i, position):
                neList = neighbor[i]
                for n in neList:
                    if position[n] == 'x':
                        pos = position[:n] + 'B' + position[n+1:]
                        if closeMill(n, pos):
                            num2 += 1

    return num - num2


def winConf(position):
    numWhite, numBlack = countNums(position)
    if numBlack < 3:
        return 1
    elif numWhite < 3:
        return -1
    return 0


def midEndStaticImprove(loc, position):
    numWhite = countNums(position)[0]
    if numWhite > 3:
        return midStaticImprove(loc, position)
    else:
        return endStaticImprove(loc, position)


def openStaticImprove(loc, position):
    num = 18 * closeMorris(loc, position) + 26 * countMills(position) + 1 * countBlockedOpp(position) + 9 * piecesNumber(position) + 10 * count2PiecesConf(position) + 7 * count3PiecesConf(position)
    # num = 14 * closeMorris(loc, position) + 37 * countMills(position) + 4 * countBlockedOpp(position) + 14 * piecesNumber(position) + 20 * count2PiecesConf(position) + 2 * count3PiecesConf(position)
    return num


def midStaticImprove(loc, position):
    num = 16 * closeMorris(loc, position) + 43 * countMills(position) + 10 * countBlockedOpp(position)  + 11 * piecesNumber(position) + 8 * doubleMills(position) + 1086 * winConf(position)
    # num = 16 * closeMorris(loc, position) + 43 * countMills(position) + 11 * countBlockedOpp(position) + 8 * piecesNumber(position) + 7 * count2PiecesConf(position) + 42 * doubleMills(position) + 1086 * winConf(position)
    return num


def endStaticImprove(loc, position):
    num = 10 * count2PiecesConf(position) + 1 * count3PiecesConf(position) + 16 * closeMorris(loc, position) + 1190 * winConf(position)
    return num


def MaxMinOpening(board, depth):
    global numEvaluate
    if depth == 0:
        # board.value = openingStatic(board.position)
        board.value = openStaticImprove(board.lastMove, board.position)
        numEvaluate += 1
        return board
    else:
        board.child = genMoveOpening(board.position)

        maxValue = float('-inf')
        retBoard = None
        for child in board.child:
            result = MinMaxOpening(child, depth - 1)
            if maxValue < result.value:
                # retBoard = result
                maxValue = result.value

                retBoard = child
                retBoard.value = maxValue
        return retBoard


def MinMaxOpening(board, depth):
    global numEvaluate
    if depth == 0:
        # board.value = openingStatic(board.position)
        board.value = openStaticImprove(board.lastMove, board.position)
        numEvaluate += 1
        return board
    else:
        board.child = genMoveOpeningBlack(board.position)

        minValue = float('inf')
        retBoard = None
        for child in board.child:
            result = MaxMinOpening(child, depth - 1)
            if minValue > result.value:
                # retBoard = result
                minValue = result.value

                retBoard = child
                retBoard.value = minValue
        return retBoard


def MaxMin2(count, board, depth, alpha, beta):
    global numEvaluate
    if count < 18:
        con = eval('depth == 0')
    else:
        numWhite = countNums(board.position)[0]
        con = eval('depth == 0 or numWhite < 3')

    if con:
        if count < 18:
            board.value = openStaticImprove(board.lastMove, board.position)
        else:
            board.value = midEndStaticImprove(board.lastMove, board.position)

        numEvaluate += 1
        return board
    else:
        if count < 18:
            board.child = genMoveOpening(board.position)
        else:
            board.child = genMoveMidEnd(board.position)

    if board.child == []:
        if board.lastMove == -1:
            return board
        board.value = midEndStaticImprove(board.lastMove, board.position)
        return board

    maxValue = float('-inf')
    retBoard = None
    for child in board.child:
        result = MinMax2(count+1, child, depth - 1, alpha, beta)
        if maxValue < result.value:
            # retBoard = result
            maxValue = result.value

            retBoard = child
            retBoard.value = maxValue
        if maxValue >= beta:
            return retBoard
        else:
            if maxValue > alpha:
                alpha = maxValue
    return retBoard


def MinMax2(count, board, depth, alpha, beta):
    global numEvaluate
    if count < 18:
        con = eval('depth == 0')
    else:
        numBlack = countNums(board.position)[1]
        con = eval('depth == 0 or numBlack < 3')

    if con:
        if count < 18:
            board.value = openStaticImprove(board.lastMove, board.position)
        else:
            board.value = midEndStaticImprove(board.lastMove, board.position)

        numEvaluate += 1
        return board
    else:
        if count < 18:
            board.child = genMoveOpeningBlack(board.position)
        else:
            board.child = genMoveMidEndBlack(board.position)

    if board.child == []:
        board.value = midEndStaticImprove(board.lastMove, board.position)
        return board

    minValue = float('inf')
    retBoard = None
    for child in board.child:
        result = MaxMin2(count+1, child, depth - 1, alpha, beta)
        if minValue > result.value:
            # retBoard = result
            minValue = result.value

            retBoard = child
            retBoard.value = minValue
        if minValue <= alpha:
            return retBoard
        elif minValue < beta:
            beta = minValue

    return retBoard

def MaxMinMid(board, depth):
    global numEvaluate
    numWhite = countNums(board.position)[0]
    if depth == 0 or numWhite < 3:
        board.value = midStaticImprove(board.lastMove, board.position)
        numEvaluate += 1
        return board
    else:
        board.child = genMoveMidEnd(board.position)

        maxValue = float('-inf')
        retBoard = None
        for child in board.child:
            result = MinMaxMid(child, depth - 1)
            if maxValue < result.value:
                # retBoard = result
                maxValue = result.value

                retBoard = child
                retBoard.value = maxValue
        return retBoard


def MinMaxMid(board, depth):
    global numEvaluate
    numBlack = countNums(board.position)[1]
    if depth == 0 or numBlack < 3:
        board.value = midStaticImprove(board.lastMove, board.position)
        numEvaluate += 1
        return board
    else:
        board.child = genMoveMidEndBlack(board.position)

        minValue = float('inf')
        retBoard = None
        for child in board.child:
            result = MaxMinMid(child, depth - 1)
            if minValue > result.value:
                # retBoard = result
                minValue = result.value

                retBoard = child
                retBoard.value = minValue
        return retBoard


def main():
    inFileName, outFileName, depth = 'board1.txt', 'board2.txt', 1
    # root = readFromFile(inFileName)
    # root = BoardNode('WxBxWxxxWxxBWxxxxxWxB')
    # root = BoardNode('xxxxxxxxxxWWxWWxBBBxx')
    root = BoardNode('WBBBxxWWBBWWBBxBWWBWW')

    tStart = time.time()
    # result = MinMaxOpening(root, depth)
    # result = MaxMinMid(root, depth)
    result = MaxMin2(19, root, depth)
    tEnd = time.time()
    t = tEnd - tStart

    print('Initial position:', root.position, 'Output position: ', result.position)
    print('Position evaluated by static estimation: ', numEvaluate)
    print('MINIMAX estimate: ', result.value)

    print('time = ', t)

    # print(root)


if __name__ == '__main__':
    main()