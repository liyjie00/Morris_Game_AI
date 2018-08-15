import sys, time

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


def countNums(position):
    numWhite = 0
    numBlack = 0
    for pos in position:
        if pos == 'W':
            numWhite += 1
        elif pos == 'B':
            numBlack += 1
    return numWhite, numBlack


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

    if count - 2 + depth <= 18:
        root = S_MiniMaxOpeningImproved.TreeNode(None, list(move), 0, 1)
        root.board = S_MiniMaxGameImproved.SwapColor(root.board)
        S_MiniMaxOpeningImproved.BuildTree(root, depth)
    else:
        root = S_MiniMaxGameImproved.TreeNode(None, list(move), 0, 1)
        root.board = S_MiniMaxGameImproved.SwapColor(root.board)
        S_MiniMaxGameImproved.BuildTree(root, depth)

    if count - 1 < 18:
        result = S_MiniMaxOpeningImproved.MaxMin(depth, count - 1, root, -10000000000, 10000000000)
        NextStep = S_MiniMaxOpeningImproved.FindNextStep(result)

    else:
        result = S_MiniMaxGameImproved.MaxMin(root, depth, -10000000000, 10000000000)
        NextStep = S_MiniMaxGameImproved.FindNextStep(result)

    NextStep.board = S_MiniMaxGameImproved.SwapColor(NextStep.board)
    rMove = ''.join(NextStep.board)

    t2 = time.time()

    if rMove == move:
        print("black no move")
        print('white win')
        write(file2, "white win", 'a')
        exit(0)

    print(rMove, count, ' black ', result.estimation * -1, '\t', round((t2 - t1), 2), 's')

    write(file1, rMove, 'w')

    if count > 18:
        numWhite = countNums(rMove)[1]
        if numWhite < 3:
            print('black win')
            write(file2, 'black win', 'a')

    write(file2, rMove, 'a')


if __name__ == '__main__':
    playBlack(int(sys.argv[1]))
