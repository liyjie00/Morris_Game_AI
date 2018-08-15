size = 21
count = 0
import S_MiniMaxGameImproved


def GenerateMoveOpening(board):
    L = GenerateAdd(board)
    return L


def GenerateAdd(board):
    L = []
    for each in range(size):
        if board[each] == "x":
            b = board[:]
            b[each] = "W"
            # b = b[:each] + "W" + b[each+1:]
            if closeMill(each, b):
                GenerateRemove(b, L)
            else:
                L.append(b)
    return L


def neighbors(j):
    switcher = {
        0: [6, 18, 2, 4],
        1: [11, 20],
        2: [0, 4, 7, 15],
        3: [10, 17],
        4: [8, 12, 0, 2],
        5: [9, 14],
        6: [0, 18, 7, 8],
        7: [2, 15, 6, 8],
        8: [6, 7, 4, 12],
        9: [5, 14, 10, 11],
        10: [3, 17, 9, 11],
        11: [1, 20, 9, 10],
        12: [4, 8, 13, 14],
        13: [16, 19, 12, 14],
        14: [12, 13, 9, 5],
        15: [2, 7, 16, 17],
        16: [15, 17, 13, 19],
        17: [15, 16, 3, 10],
        18: [0, 6, 19, 20],
        19: [18, 20, 16, 13],
        20: [18, 19, 11, 1],
    }
    return switcher.get(j)


def closeMill(j, b):
    C = b[j]
    L_neighbors = neighbors(j)
    i = 0
    judge = False
    while i < L_neighbors.__len__():
        if b[L_neighbors[i]] == C and b[L_neighbors[i + 1]] == C:
            judge = True
            break
        else:
            i = i + 2
    return judge


def halfMill(j, b):
    C = b[j]
    L_neighbors = neighbors(j)
    i = 0
    judge = False
    while i < L_neighbors.__len__():
        if (b[L_neighbors[i]] == "x" and b[L_neighbors[i + 1]] == C) or (
                b[L_neighbors[i]] == C and b[L_neighbors[i + 1]] == "x"):
            judge = True
            break
        else:
            i = i + 2
    return judge


def GenerateRemove(board, L):
    judge = False
    for each in range(size):
        if board[each] == "B":
            if closeMill(each, board) == False:
                judge = True
                b = board[:]
                b[each] = "x"
                L.append(b)
    if judge == False:
        L.append(board)


def SwapColor(board):
    for each in range(size):
        if board[each] == "W":
            board[each] = "B"
        else:
            if board[each] == "B":
                board[each] = "W"

    return board


def Static_Estimation(board):
    count_W = 0
    count_B = 0
    for each in range(size):
        if board[each] == "W":
            count_W += 1
        if board[each] == "B":
            count_B += 1

    count_half_mill = 0
    for each in range(size):
        if board[each] == "W" and halfMill(each, board):
            count_half_mill += 1
    return 10 * (count_W - count_B) + count_half_mill


def MaxMin(depth, c, Node, alpha, beta):
    if Node.children_node.__len__() == 0:
        global count
        Node.estimation = Static_Estimation(Node.board)
        count += 1
        return Node
    else:
        v = -10000000000
        for each in Node.children_node:
            if c > 18:
                a = S_MiniMaxGameImproved.MinMax(Node, depth, Node.alpha, Node.beta)
            else:
                a = MinMax(depth, c+1, each, Node.alpha, Node.beta)
            if a.estimation > v:
                temp_Node = a
                v = a.estimation
            if v >= beta:
                return temp_Node
            elif v > alpha:
                Node.alpha = v
        return temp_Node


def MinMax(depth, c, Node, alpha, beta):
    if Node.children_node.__len__() == 0:
        global count
        Node.estimation = Static_Estimation(Node.board)
        count += 1
        return Node
    else:
        v = 10000000000
        for each in Node.children_node:
            if c > 18:
                b = S_MiniMaxGameImproved.MaxMin(depth, each, Node.alpha, Node.beta)
            else:
                b = MaxMin(depth, c+1,each, Node.alpha, Node.beta)
            if b.estimation < v:
                temp_Node = b
                v = b.estimation
            if v <= alpha:
                return temp_Node
            elif v < beta:
                Node.beta = v
        return temp_Node


# construct the TreeNode
# color = 1 represents "W" which is a max node, color = 0 represents "B" which is a min node
class TreeNode:
    def __init__(self, parent, board, depth, color):
        self.parent = parent
        self.board = board
        self.children_node = []
        self.depth = depth
        self.color = color
        self.estimation = None
        self.alpha = -10000000000
        self.beta = 10000000000
        # self.positions = []


def BuildTree(Node, depth):
    if Node.depth >= depth:
        return
    if Node.color == 1:
        L = GenerateMoveOpening(Node.board)
    else:
        if Node.color == 0:
            tempb = Node.board[:]
            L = GenerateMoveOpening(SwapColor(tempb))
            for each in L:
                each = SwapColor(each)
    for each in L:
        temp = TreeNode(Node, each, Node.depth + 1, (Node.color + 1) % 2)
        Node.children_node.append(temp)
        BuildTree(temp, depth)


def FindNextStep(Board):
    while (Board.depth > 1):
        Board = Board.parent
    return Board


# if __name__ == '__main__':
    # # read the data from the input
    #
    # input = "board.txt"
    # output = "board1_result.txt"
    # # depth = 1
    # # input, output, depth = raw_input().split()
    # # depth = int(depth)
    #
    # f = open(input)
    # # data = f.read()
    # data = 'xxxxxxxxxWxxxxxxBxxxx'
    # board = list(data)
    # f.close()
    # size = board.__len__()
    #
    # root = TreeNode(None, board, 0, 1)
    # BuildTree(root, 5)
    #
    # result = MaxMin(root, -10000000000, 10000000000)
    #
    # NextStep = FindNextStep(result)
    #
    # str_input = ''.join(root.board)
    # str_output = ''.join(NextStep.board)
    # print("input position: " + str_input)
    # print("output position: " + str_output)
    # print("Positions evaluated by static estimation: " + str(count))
    # print("MINIMAX estimate: " + str(result.estimation))
    # text_file = open(output, "w")
    # # text_file.write(str_output)
    # text_file.close()
