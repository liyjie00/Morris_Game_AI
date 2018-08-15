import sys
from copy import deepcopy

numWhite = 0
numBlack = 0
numEvaluate = 0

mills = {0: [[2, 4], [6, 18]],
         1: [(11, 20)],
         2: [[0, 4], [7, 15]],
         3: [[10, 17]],
         4: [[2, 0], [8, 12]],
         5: [[9, 14]],
         6: [[0, 18], [7, 8]],
         7: [[2, 15], [6, 8]],
         8: [[12, 4], [6, 7]],
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
         19: [[18, 20], [16, 13]],
         20: [[1, 11], [19, 18]],
         }


class BoardNode(object):
    __slots__ = ('value', 'position', 'parent', 'child')

    def __init__(self, position='', parent=None):
        self.value = None
        self.position = position
        self.parent = parent
        self.child = []

    def __str__(self):
        return self.position


def generateMovesOpening(inBoard, depth):
    boardList = []
    boardList.append(inBoard)

    global numEvaluate
    numEvaluate = 0

    for i in range(depth):
        length = len(boardList)
        for index in range(length):
            if i % 2 == 0:
                boardList[0].child = generateAdd(boardList[0])
                boardList += boardList[0].child
            else:
                boardList[0].child = generateAddBlack(boardList[0])
                boardList += boardList[0].child

            boardList.remove(boardList[0])

    numEvaluate = len(boardList)

    for board in boardList:
        board.value = openingStatic(board.position)

    # find the max static value of the positions
    moveResult = findMaxMove(boardList, depth)
    maxValue = moveResult.value

    # return the final decision
    return getParent(moveResult, depth, maxValue)


def getParent(move, depth, maxValue):
    i = 1
    outBoard = move
    while i < depth:
        print('get parent', (depth - 1))
        outBoard = outBoard.parent
        i += 1
    outBoard.value = maxValue
    return outBoard


def findMaxMove(boradList):
    max = float('-inf')
    moveLeaf = None

    # choose the leaf having the max static value
    for i in range(len(boradList)):
        boradList[i].value = openingStatic(boradList[i].position)
        if max < boradList[i].value:
            max = boradList[i].value
            moveLeaf = boradList[i]
        # print(boradList[i], boradList[i].parent)
    moveLeaf.value = max
    # print('max = ', max, moveLeaf, moveLeaf.parent, moveLeaf.value)
    return moveLeaf


def findMaxMove(boardList, depth):
    max = float('-inf')
    min = float('inf')
    move = None
    parent = None
    count = deepcopy(depth)
    for board in boardList:
        if count == 0:
            break
        if board.parent != parent:
            parent = board.parent
            boardList.append(parent)
            if count - 1 % 2 == 0:
                for child in parent.child:
                    if max < child.value:
                        max = child.value
                move = parent
                parent.value = max
                count -= 1
            else:
                for child in parent.child:
                    if min > child.value:
                        min = child.value
                move = parent
                parent.value = min
                count -= 1
    return move



def generateAdd(inBoard):
    posList = []
    length = len(inBoard.position)
    for loc in range(length):
        if inBoard.position[loc] == 'x':
            newBoard = BoardNode(parent=inBoard)
            newBoard.position = inBoard.position[:loc] + 'W' + inBoard.position[loc + 1:]

            if closeMill(loc, newBoard):
                posList = generateRemove(newBoard, posList)
            else:
                # newBoard.value = openingStatic(newBoard.position)
                posList.append(newBoard)
    # inBoard.child = posList
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


def generateAddBlack(inBoard):
    revB = deepcopy(inBoard)
    revB.position = reverse(revB.position)
    result = generateAdd(revB)

    for board in result:
        board.position = reverse(board.position)
        board.parent = inBoard

    return result


def generateRemove(board, posList):
    closeMillFlag = True
    for loc in range(len(board.position)):
        if board.position[loc] == 'B':
            if not closeMill(loc, board):
                newBoard = BoardNode(parent=board.parent)
                newBoard.position = board.position[:loc] + 'x' + board.position[loc + 1:]
                # newBoard.value = openingStatic(newBoard.position)
                posList.append(newBoard)
                closeMillFlag = False

    if closeMillFlag:
        # board.value = openingStatic(board.position)
        posList.append(board)

    return posList


def closeMill(loc, board):
    hasMill = False
    move = board.position[loc]
    for pos in mills[loc]:
        hasMill = hasMill or (board.position[pos[0]] == move and board.position[pos[1]] == move)
    return hasMill


def openingStatic(boardPosition):
    countNums(boardPosition)
    return numWhite - numBlack


def countNums(boardPosition):
    global numWhite, numBlack
    numWhite = 0
    numBlack = 0
    for pos in boardPosition:
        if pos == 'W':
            numWhite += 1
        elif pos == 'B':
            numBlack += 1


def readFromFile(fileName):
    file = open(fileName, 'r')
    boardPosition = file.read()
    return boardPosition


def write2File(newFileName, result):
    newFile = open(newFileName, 'w')
    newFile.write(result)


def main():
    # inFileName, outFileName, searchDepth = sys.argv[0], sys.argv[1], int(sys.argv[2])

    inFileName, outFileName, searchDepth = 'board1.txt', 'board2.txt', 4
    inputState = readFromFile(inFileName)

    inputBoard = BoardNode(inputState)
    inputBoard.value = openingStatic(inputBoard.position)

    print('Initial position:', inputBoard, end=' ')

    result = generateMovesOpening(inputBoard, searchDepth)
    # print('=+' * 30)

    print('Output position:', result)

    # print(result, result.value)
    print('Position evaluated by static estimation: ', numEvaluate)
    print('MINIMAX estimate: ', result.value)
    # print(result.parent)

    # for a in result.child:
    #     print(a)


if __name__ == '__main__':
    main()
