from multiprocessing import Process, Queue
import time
import sys

import MorrisGame2
import MiniMaxOpeningImproved
import MiniMaxGameImproved
import MiniMaxTournament
import S_MiniMaxOpeningImproved, S_MiniMaxGameImproved


def read(fileName):
    f = open(fileName)
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


def write(fileName, l, mode):
    file = open(fileName, mode)
    l = '\n' + l
    file.write(l)
    file.close()


def playBlack(depth):
    file1 = '/Users/jie/Desktop/board.txt'
    file2 = '/Users/jie/Desktop/board3.txt'
    move = read(file1)[1]
    write(file2, move, 'a')
    count = read(file2)[0]

    if move == 'black win' or move == 'white win':
        print(move)
        exit(0)

    t1 = time.time()
    root = MiniMaxTournament.BoardNode(move)

    result = MiniMaxTournament.MinMax2(count - 1, root, depth, float('-inf'), float('inf'))
    t2 = time.time()
    if result.position == move:
        print("black no move")
        print('white win')
        write(file2, "white win", 'a')
        exit(0)

    print(result.position, count, 'black', result.value, t2-t1)

    write(file1, result.position, 'w')

    if count > 18:
        numWhite = MorrisGame2.countNums(result.position)[0]
        if numWhite < 3:
            print('black win')
            write(file2, 'black win', 'a')

    write(file2, result.position, 'a')


if __name__ == '__main__':
    playBlack(int(sys.argv[1]))