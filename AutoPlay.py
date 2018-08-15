from multiprocessing import Process, Queue
import time


import S_MiniMaxOpeningImproved, S_MiniMaxGameImproved


def read():
    f = open('board.txt')
    count = 0
    lines = f.readline()

    l = None
    while lines:
        l = lines
        count += 1
        lines = f.readline()
    f.close()
    return count, l


def write(l):
    file = open('board.txt', 'a')
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


def playWhite(q, depth):
    while True:
        move = q.get()
        count= read()[0]

        if move == 'black win' or move == 'white win':
            print(move)
            break

        t1 = time.time()

        if count - 2 + depth <= 18:
            root = S_MiniMaxOpeningImproved.TreeNode(None, list(move), 0, 1)
            S_MiniMaxOpeningImproved.BuildTree(root, depth)
        else:
            root = S_MiniMaxGameImproved.TreeNode(None, list(move), 0, 1)
            S_MiniMaxGameImproved.BuildTree(root, depth)

        if count - 1 < 18:
            result = S_MiniMaxOpeningImproved.MaxMin(depth, count - 1, root, -10000000000, 10000000000)
            NextStep = S_MiniMaxOpeningImproved.FindNextStep(result)
        else:
            result = S_MiniMaxGameImproved.MaxMin(root, depth, -10000000000, 10000000000)
            NextStep = S_MiniMaxGameImproved.FindNextStep(result)

        rMove = ''.join(NextStep.board)

        t2 = time.time()

        if rMove == move:
            print("white no move")
            print('black win')
            q.put('black win')
            break

        print(rMove, count, ' white ', result.estimation, '\t', round((t2 - t1),2), 's')
        write(rMove)

        if count > 18:
            numBlack = countNums(rMove)[1]
            if numBlack < 3:
                q.put('white win')
                break
        q.put(rMove)


def playBlack(q, depth):
    while True:
        move = q.get()
        count= read()[0]

        if move == 'black win' or move == 'white win':
            print(move)
            break

        t1 = time.time()

        if count-2 + depth <= 18:
            root = S_MiniMaxOpeningImproved.TreeNode(None, list(move), 0, 1)
            root.board = S_MiniMaxGameImproved.SwapColor(root.board)
            S_MiniMaxOpeningImproved.BuildTree(root, depth)
        else:
            root = S_MiniMaxGameImproved.TreeNode(None, list(move), 0, 1)
            root.board = S_MiniMaxGameImproved.SwapColor(root.board)
            S_MiniMaxGameImproved.BuildTree(root, depth)

        if count-1 < 18:
            result = S_MiniMaxOpeningImproved.MaxMin(depth, count-1, root, -10000000000, 10000000000)
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
            q.put('white win')
            break

        print(rMove, count, ' black ', result.estimation*-1, '\t', round((t2 - t1),2), 's')
        write(rMove)

        if count > 18:
            numWhite = countNums(rMove)[0]
            if numWhite < 3:
                q.put('black win')
                break
        q.put(rMove)


if __name__ == '__main__':
    q = Queue()
    q1 = Queue()
    move = read()[1]
    q.put(move)

    whiteDepth = 3
    blackDepth = 3

    pw = Process(target=playWhite, args=(q, whiteDepth,))
    pb = Process(target=playBlack, args=(q, blackDepth, ))

    pw.start()
    pb.start()

    pw.join()
    pb.join()
    print('finish')

