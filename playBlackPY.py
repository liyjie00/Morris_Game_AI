import sys

from multiprocessing import Process, Queue
import time

import MorrisGame2
import MiniMaxOpeningImproved
import MiniMaxGameImproved
import MiniMaxTournament
import S_MiniMaxOpeningImproved, S_MiniMaxGameImproved


def read():
    f = open('/Users/jie/Desktop/board.txt')
    count = 0
    lines = f.readline()

    l = None
    while lines:
        l = lines
        # print(l)
        count += 1
        lines = f.readline()
    f.close()
    return count, l


def write(l):
    file = open('/Users/jie/Desktop/board.txt', 'a')
    l = '\n' + l
    file.write(l)
    file.close()


def MaxMin(count, board, depth):
    if count < 18:
        con = eval('depth == 0')
    else:
        numWhite = MorrisGame2.countNums(board.position)[0]
        con = eval('depth == 0 or numWhite < 3')

    if con:
        if count < 18:
            board.value = MorrisGame2.openingStatic(board.position)
        else:
            board.value = MorrisGame2.staticMidEnd(board.position)
        MorrisGame2.numEvaluate += 1
        return board
    else:
        if count < 18:
            board.child = MorrisGame2.genMoveOpening(board.position)
        else:
            board.child = MorrisGame2.genMoveMidEnd(board.position)

        if board.child == []:
            board.value = -10000
            return board

        maxValue = float('-inf')
        retBoard = None
        for child in board.child:
            result = MinMax(count+1, child, depth - 1)

            if maxValue < result.value:
                # retBoard = result
                maxValue = result.value

                retBoard = child
                retBoard.value = maxValue
        return retBoard


def MinMax(count, board, depth):
    if count < 18:
        con = eval('depth == 0')
    else:
        numBlack = MorrisGame2.countNums(board.position)[1]
        con = eval('depth == 0 or numBlack < 3')

    if con:
        if count < 18:
            board.value = MorrisGame2.openingStatic(board.position)
        else:
            board.value = MorrisGame2.staticMidEnd(board.position)
        MorrisGame2.numEvaluate += 1
        return board
    else:
        if count < 18:
            board.child = MorrisGame2.genMoveOpeningBlack(board.position)
        else:
            board.child = MorrisGame2.genMoveMidEndBlack(board.position)

        if board.child == []:
            board.value = 10000
            return board

        minValue = float('inf')
        retBoard = None
        for child in board.child:
            result = MaxMin(count+1, child, depth - 1)

            if minValue > result.value:
                # retBoard = result
                minValue = result.value

                retBoard = child
                retBoard.value = minValue
        return retBoard



def MaxMinIM(count, board, depth, alpha, beta):
    if count < 18:
        con = eval('depth == 0')
    else:
        numWhite = MorrisGame2.countNums(board.position)[0]
        con = eval('depth == 0 or numWhite < 3')

    if con:
        if count < 18:
            board.value = MiniMaxOpeningImproved.openingStaticImproved(board.position)
        else:
            board.value = MiniMaxGameImproved.staticMidEndImproved(board.position, depth)
        MorrisGame2.numEvaluate += 1
        return board
    else:
        if count < 18:
            board.child = MorrisGame2.genMoveOpening(board.position)
        else:
            board.child = MorrisGame2.genMoveMidEnd(board.position)

        if board.child == []:
            board.value = MiniMaxGameImproved.staticMidEndImproved(board.position, depth)
            return board

        maxValue = float('-inf')
        retBoard = None
        for child in board.child:
            result = MinMaxIM(count+1, child, depth - 1, alpha, beta)

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


def MinMaxIM(count, board, depth, alpha, beta):
    if count < 18:
        if depth == 0:
            board.value = MiniMaxOpeningImproved.openingStaticImproved(board.position)
            return board
        else:
            board.child = MorrisGame2.genMoveOpeningBlack(board.position)
    else:
        numBlack = MorrisGame2.countNums(board.position)[1]
        if depth == 0 or numBlack < 3:
            board.value = MiniMaxGameImproved.staticMidEndImproved(board.position, depth)
        else:
            board.child = MorrisGame2.genMoveMidEndBlack(board.position)

    if board.child == []:
        board.value = MiniMaxGameImproved.staticMidEndImproved(board.position, depth)
        return board

    minValue = float('inf')
    retBoard = None
    for child in board.child:
        result = MaxMinIM(count+1, child, depth - 1, alpha, beta)

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




def playWhite(q):
    while True:
        move = q.get()
        # print('read: ', move)

        count = read()[0]
        if move == 'white win' or move == 'black win':
            print(move)
            break
        root = MorrisGame2.BoardNode(move)
        # print('read: ', root.position)

        result = MaxMin(count-1, root, 4)
        if result.position == move:
            print('white no move')
            q.put('black win')
            break

        print(result.position, count, result.value)
        write(result.position)

        if count > 18:
            numBlack = MorrisGame2.countNums(result.position)[1]
            if numBlack < 3:
                q.put('white win')
                break
        q.put(result.position)


def playWhiteImproved(q):
    while True:
        move = q.get()
        # print('read: ', move)

        count = read()[0]
        if move == 'white win' or move == 'black win':
            print(move)
            break
        root = MorrisGame2.BoardNode(move)
        # print('read: ', root.position)

        result = MaxMinIM(count-1, root, 3)
        # if result.position == 'no move':
        #     print('white no move')
        #     q.put('black win')
        #     break

        print(result.position, count, result.value)
        write(result.position)

        if count > 18:
            numBlack = MorrisGame2.countNums(result.position)[1]
            if numBlack < 3:
                q.put('white win')
                break
        q.put(result.position)


def playBlackImproved(q):
    while True:
        move = q.get()
        # print('read: ', move)

        count = read()[0]
        if move == 'white win' or move == 'black win':
            print(move)
            break
        t1 = time.time()
        root = MorrisGame2.BoardNode(move)
        # print('read: ', root.position)

        root.position = MorrisGame2.reverse(root.position)
        result = MaxMinIM(count-1, root, 3, float('-inf'), float('inf'))
        root.position = MorrisGame2.reverse(root.position)
        result.position = MorrisGame2.reverse(result.position)
        t2 = time.time()
        if result.position == move:
            print('black no move')
            q.put('white win')
            break

        print(result.position, count, result.value, 'black', t2-t1)
        write(result.position)

        if count > 18:
            numBlack = MorrisGame2.countNums(result.position)[1]
            if numBlack < 3:
                q.put('white win')
                break
        q.put(result.position)



def playBlack(q):
    while True:
        move = q.get()
        # print('read: ', move)

        count = read()[0]
        if move == 'white win' or move == 'black win':
            print(move)
            break
        root = MorrisGame2.BoardNode(move)
        # print('read: ', root.position)

        # root.position = MorrisGame2.reverse(root.position)

        # result = MaxMin(count-1, root, 3)
        result = MinMax(count-1, root, 3)
        if result.position == move:
            print('black no move')
            q.put('white win')
            break
        # result.position = MorrisGame2.reverse(result.position)

        print(result.position, count, result.value * -1, 'black')
        write(result.position)

        if count > 18:
            numWhite = MorrisGame2.countNums(result.position)[0]
            if numWhite < 3:
                q.put('black win')
                break
        q.put(result.position)


def pBlack(depth):
    move = read()[1]
    # print('read: ', move)

    count = read()[0]
    if move == 'white win' or move == 'black win':
        print(move)
        exit(0)
    root = MorrisGame2.BoardNode(move)
    # print('read: ', root.position)

    # root.position = MorrisGame2.reverse(root.position)

    # result = MaxMin(count-1, root, 3)
    result = MinMax(count-1, root, depth)
    if result.position == move:
        print('black no move')
        print('white win')
    # result.position = MorrisGame2.reverse(result.position)

    print(result.position, count, result.value * -1, 'black')
    write(result.position)

    if count > 18:
        numWhite = MorrisGame2.countNums(result.position)[0]
        if numWhite < 3:
            print('black win')


if __name__ == '__main__':
    pBlack(int(sys.argv[1]))
