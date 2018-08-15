size = 21
count = 0

def GenerateMoveOpening(board):
    L = GenerateAdd(board)
    return L


def GenerateMovesMidgameEndgame(board):
    count = 0
    for each in board:
        if each == "W":
            count += 1
    if count == 3:
        return GenerateHopping(board)
    else:
        return GenerateMove(board)


def GenerateAdd(board):
    L = []
    for each in range(size):
        if board[each] == "x":
            b = board[:]
            b[each] = "W"
            if closeMill(each, b):
                GenerateRemove(b, L)
            else:
                L.append(b)
    return L


def GenerateHopping(board):
    L = []
    for location_a in range(size):
        if board[location_a] == "W":
            for location_b in range(size):
                if board[location_b] == "x":
                    b = board[:]
                    b[location_a] = "x"
                    b[location_b] = "W"
                    if closeMill(location_b, b):
                        GenerateRemove(b, L)
                    else:
                        L.append(b)
    return L


def GenerateMove(board):
    L = []
    for each in range(size):
        if board[each] == "W":
            n = close_neighbors(each)
            for j in n:
                if board[j] == "x":
                    b = board[:]
                    b[each] = "x"
                    b[j] = "W"
                    if closeMill(j, b):
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


def close_neighbors(j):
    switcher = {
        0: [6, 1, 2],
        1: [11, 0],
        2: [0, 4, 7, 3],
        3: [10, 2],
        4: [8, 5, 2],
        5: [9, 4],
        6: [0, 18, 7],
        7: [2, 15, 6, 8],
        8: [7, 4, 12],
        9: [5, 14, 10],
        10: [3, 17, 9, 11],
        11: [1, 20, 10],
        12: [8, 13],
        13: [16, 12, 14],
        14: [13, 9],
        15: [7, 16],
        16: [15, 17, 13, 19],
        17: [16, 10],
        18: [6, 19],
        19: [18, 20, 16],
        20: [19, 11],
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
    for each in board:
        if each == "W":
            count_W += 1
        if each == "B":
            count_B += 1
    count_half_mill = 0
    for each in range(size):
        if board[each] == "W" and halfMill(each, board):
            count_half_mill += 1
    return 100 * (count_W - count_B) + 10 * count_half_mill


def MaxMin(Node, depth, alpha, beta):
    if Node.depth == depth or Node.children_node.__len__() == 0:
        if Node.positions.__len__() == 0:
            Node.estimation = 10000
        elif CountB(Node.board) <= 2:
            Node.estimation = 10000
        elif CountW(Node.board) <= 2:
            Node.estimation = -10000
        else:
            Node.estimation = 10 * Static_Estimation(Node.board) - Node.positions.__len__()
        global count
        count += 1
        return Node
    else:
        v = -10000000000
        for each in Node.children_node:
            a = MinMax(each, depth, Node.alpha, Node.beta)
            if a.estimation > v:
                temp_Node = a
                v = a.estimation
            if v >= beta:
                return temp_Node
            elif v > alpha:
                Node.alpha = v
        return temp_Node


def MinMax(Node, depth, alpha, beta):
    if Node.depth == depth or Node.children_node.__len__() == 0:
        if Node.positions.__len__() == 0:
            Node.estimation = 10000
        elif CountB(Node.board) <= 2:
            Node.estimation = 10000
        elif CountW(Node.board) <= 2:
            Node.estimation = -10000
        else:
            Node.estimation = 10 * Static_Estimation(Node.board) - Node.positions.__len__()
        global count
        count += 1
        return Node
    else:
        v = 10000000000
        for each in Node.children_node:
            b = MaxMin(each, depth, Node.alpha, Node.beta)
            if b.estimation < v:
                temp_Node = b
                v = b.estimation
            if v <= alpha:
                return temp_Node
            elif v < beta:
                Node.beta = v
        return temp_Node


def CountW(board):
    count = 0
    for each in board:
        if each == "W":
            count += 1
    return count


def CountB(board):
    count = 0
    for each in board:
        if each == "B":
            count += 1
    return count


# construct the TreeNode
# color = 1 represents "W" which is a max node, color = 0 represents "B" which is a min node
class TreeNode:
    def __init__(self, parent, board, depth, color):
        self.parent = parent
        self.board = board
        self.children_node = []
        self.depth = depth
        self.color = color
        self.positions = 0
        self.estimation = 0  # 1000*Static_Estimation(board)-self.positions
        self.alpha = -10000000000
        self.beta = 10000000000


def BuildTree(Node, depth):
    if Node.depth >= depth + 1:
        return
    if Node.color == 1:
        L = GenerateMovesMidgameEndgame(Node.board)
    else:
        if Node.color == 0:
            tempb = Node.board[:]
            L = GenerateMovesMidgameEndgame(SwapColor(tempb))
            for each in L:
                each = SwapColor(each)
    Node.positions = L

    if Node.positions.__len__() == 0:
        return
    else:
        for each in L:
            temp = TreeNode(Node, each, Node.depth + 1, (Node.color + 1) % 2)
            Node.children_node.append(temp)
            BuildTree(temp, depth)


def FindNextStep(Board):
    while (Board.depth > 1):
        Board = Board.parent
    return Board


# if __name__ == '__main__':
#     # read the data from the input
#
#     input = "board3.txt"
#     output = "board3_result.txt"
#     d = 4
#
#     # input, output, depth = raw_input().split()
#     # depth = int(depth)
#
#     f = open(input)
#     # data = f.read()
#     data = 'xxxxxxxxxxWWxWWxBBBxx'
#     board = list(data)
#     f.close()
#     size = board.__len__()
#
#     root = TreeNode(None, board, 0, 1)
#     BuildTree(root, d)
#
#     count = 0
#     result = MaxMin(root, d, -10000000000, 10000000000)
#
#     NextStep = FindNextStep(result)
#
#     str_input = ''.join(root.board)
#     str_output = ''.join(NextStep.board)
#     print("input position: " + str_input)
#     print("output position: " + str_output)
#     print("Positions evaluated by static estimation: " + str(count))
#     print("MINIMAX estimate: " + str(result.estimation))
#     # text_file = open(output, "w")
#     # # text_file.write(str_output)
#     # text_file.close()
