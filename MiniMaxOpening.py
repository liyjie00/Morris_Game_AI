# coding: utf-8
import sys
from copy import deepcopy

numWhite = 0
numBlack = 0
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


def generateMovesOpening(boardPosition):
    boardList = generateAdd(boardPosition)

    # find the max static value of the positions

    # return the final decision


# def generateMoveMidgameEndgame():
#     pass


def generateAdd(boardPosition):
    posList = []
    for loc in range(0, len(boardPosition)):
        if loc == 'x':
            newBoard = deepcopy(boardPosition)
            newBoard[loc] = 'W'

            if closeMill(loc, newBoard):
                generateRemove(newBoard, posList)
            else:
                posList.append(newBoard)
    return posList


# def generateHopping():
#     pass


# def generateMove():
#     pass


def generateRemove():
    pass


# def neighbors():
#     pass


def closeMill(loc, board):
    hasMill = False
    move = board[loc]
    for pos in mills[loc]:
        hasMill = hasMill or (board[pos[0]] == move and board[pos[1]] == move)
    return hasMill

def openingStatic(boardPosition):
    countNums(boardPosition)
    return numWhite - numBlack


# def midEndStatic():
#     pass


def countNums(boardPosition):
    global numWhite, numBlack
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
    # inCommand = input('Please type in the file names and depth:')
    # fileNames = inCommand.split(' ')

    # inFile, outFile, searchDepth = sys.argv[0], sys.argv[1], int(sys.argv[2])
    inFileName, outFileName, searchDepth = 'board1.txt', 'board2.txt', 2

    inboardPosition = readFromFile(inFileName)
    static = openingStatic(inboardPosition)

    # print(static)
    # print('num of white:', numWhite)
    # print('num of black:', numBlack)


def test():
    fileName = 'test.txt'
    board = readFromFile(fileName)

    print(closeMill(0, board))


if __name__ == '__main__':
    # main()
    test()
