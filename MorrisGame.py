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
    __slots__ = ('value', 'position', 'child')

    def __init__(self, position=''):
        self.position = position
        self.child = []

    def __str__(self):
        list = []
        tree = ''
        list.append(self)
        for node in list:
            tree = tree + node.position + '\n'
            list += node.child
        return tree


def genMoveOpening(board):
    boardList = genAdd(board.position)
    return boardList


def genAdd(position):
    posList = []
    length = len(position)
    for loc in range(length):
        if position[loc] == 'x':
            newPosition = position[:loc] + 'W' + position[loc + 1:]
            newBoard = BoardNode(newPosition)
            if closeMill(loc, newBoard):
                posList = genRemove(newBoard, posList)
            else:
                posList.append(newBoard)
    return posList


def genMoveOpeningBlack(board):
    revPosition = reverse(board.position)
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
    for loc in range(len(board.position)):
        if board.position[loc] == 'B':
            if not closeMill(loc, board):
                newBoard = BoardNode()
                newBoard.position = board.position[:loc] + 'x' + board.position[loc + 1:]
                posList.append(newBoard)
                closeMillFlag = False

    if closeMillFlag:
        posList.append(board)

    return posList


def closeMill(loc, board):
    hasMill = False
    move = board.position[loc]
    for pos in mills[loc]:
        hasMill = hasMill or (board.position[pos[0]] == move and board.position[pos[1]] == move)
    return hasMill


def readFromFile(fileName):
    file = open(fileName, 'r')
    boardPosition = file.read()
    file.close()
    return boardPosition


def write2File(newFileName, result):
    newFile = open(newFileName, 'w')
    newFile.write(result)
    newFile.close()
