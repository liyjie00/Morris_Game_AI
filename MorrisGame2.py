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
    __slots__ = ('value', 'position', 'child')

    def __init__(self, position=''):
        self.value = None
        self.position = position
        self.child = []

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
                posList = genRemove(newPosition, posList)
            else:
                posList.append(BoardNode(newPosition))
    return posList


def genMoveOpeningBlack(position):
    # print('=='*30)
    revPosition = reverse(position)
    # print(position)

    # print(revPosition)

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


def genRemove(board, posList):
    closeMillFlag = True
    for loc in range(len(board)):
        if board[loc] == 'B':
            # print('remove', loc, len(board))
            if not closeMill(loc, board):
                newBoardPosition = board[:loc] + 'x' + board[loc + 1:]
                posList.append(BoardNode(newBoardPosition))
                closeMillFlag = False

    if closeMillFlag:
        posList.append(BoardNode(board))

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
                        posList = genRemove(newPosition, posList)
                    else:
                        posList.append(BoardNode(newPosition))
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
                        posList = genRemove(newPosition, posList)
                    else:
                        posList.append(BoardNode(newPosition))
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
    # print(loc)
    move = position[loc]
    for pos in mills[loc]:
        hasMill = hasMill or (position[pos[0]] == move and position[pos[1]] == move)
    return hasMill


def openingStatic(position):
    numWhite, numBlack = countNums(position)
    return numWhite - numBlack


def countNums(position):
    numWhite = 0
    numBlack = 0
    for pos in position:
        if pos == 'W':
            numWhite += 1
        elif pos == 'B':
            numBlack += 1
    return numWhite, numBlack


def staticMidEnd(position):
    revPos = reverse(position)
    list = genMoveMidEnd(revPos)

    # list = genMoveMidEndBlack(position)
    numBlackMoves = len(list)
    numWhite, numBlack = countNums(position)
    # print(position)
    # print(numBlackMoves)
    if numBlack <= 2:
        return 10000
    elif numWhite <= 2:
        return -10000
    elif numBlackMoves == 0:
        return 10000
    else:
        return 1000 * (numWhite - numBlack) - numBlackMoves


# def play(count, position):
#     if count <10:
#         genAdd(position)
#     else:
#         genMoveMidEnd(position)