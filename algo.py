import copy

class Algo:
    def __init__(self, board):
        self.board = board

    def get_move(self):
        down = self.get_down(self.board)
        right = self.get_right(self.board)
        left = self.get_left(self.board)
        up = self.get_up(self.board)
        change = [down, right, left, up]
        scores = [self.get_score(b, i) for i, b in enumerate(change)]
        print(scores)
        return scores.index(max(scores))

    def get_score(self, board, direction):
        equal = True
        score = 0
        most = 0
        for row in range(0, 4):
            for col in range(0, 4):
                if board[row][col] > most:
                    most = board[row][col]
                if board[row][col] != self.board[row][col]:
                    equal = False
                if board[row][col] > 0:
                    score += board[row][col] * row + board[row][col] * col
                else:
                    score += 200
                if row + 1 < 4 and board[row][col] == board[row + 1][col]:
                    score += board[row][col] * row + board[row][col] * col
                if col + 1 < 4 and board[row][col] == board[row][col + 1]:
                    score += board[row][col] * row + board[row][col] * col
                if row + 1 < 4 and board[row][col] == board[row + 1][col] * 2:
                    score += board[row][col] + row + col
                if col + 1 < 4 and board[row][col] == board[row][col + 1] * 2:
                    score += board[row][col] + row + col
                if row + 1 < 4 and board[row][col] * 2 == board[row + 1][col]:
                    score += board[row][col] + row + col
                if col + 1 < 4 and board[row][col] * 2 == board[row][col + 1]:
                    score += board[row][col] + row + col
        PENALTY = 100
        if board[1][0] > board[0][0] and board[0][1] > board[0][0]:
            score -= PENALTY
        if board[2][3] > board[3][3] and board[3][2] > board[3][3]:
            score -= PENALTY
        if board[0][2] > board[0][3] and board[1][3] > board[0][3]:
            score -= PENALTY
        if board[2][0] > board[3][0] and board[3][1] > board[3][0]:
            score -= PENALTY
        if board[0][0] > board[0][1] and board[0][2] > board[0][1] and board[1][1] > board[0][1]:
            score -= PENALTY
        if board[0][1] > board[0][2] and board[0][3] > board[0][2] and board[1][2] > board[0][2]:
            score -= PENALTY
        if board[0][0] > board[1][0] and board[2][0] > board[1][0] and board[1][1] > board[1][0]:
            score -= PENALTY
        if board[1][0] > board[2][0] and board[3][0] > board[2][0] and board[2][1] > board[2][0]:
            score -= PENALTY
        if board[0][3] > board[1][3] and board[2][3] > board[1][3] and board[1][2] > board[1][3]:
            score -= PENALTY
        if board[1][3] > board[2][3] and board[3][3] > board[2][3] and board[2][2] > board[2][3]:
            score -= PENALTY
        if board[3][0] > board[3][1] and board[3][2] > board[3][1] and board[2][1] > board[3][1]:
            score -= PENALTY
        if board[3][1] > board[3][2] and board[3][3] > board[3][2] and board[2][2] > board[3][2]:
            score -= PENALTY

        if board[0][0] == most:
            score += 4000
        if board[3][3] == most:
            score += 4000
        if board[0][3] == most:
            score += 4000
        if board[3][0] == most:
            score += 4000
        return -10000 if equal else score

    def get_left(self, board):
        done = False
        combined = [False, False, False, False]
        new_board = copy.deepcopy(board)
        while not done:
            done = True
            for row_pos in range(0, 4):
                row = new_board[row_pos]
                for x in range(1, 4):
                    if row[x] > 0:
                        if row[x - 1] == 0:
                            row[x - 1] = row[x]
                            row[x] = 0
                            done = False
                        elif row[x - 1] == row[x] and not combined[row_pos]:
                            row[x - 1] = row[x] * 2
                            row[x] = 0
                            done = False
                            combined[row_pos] = True
        return new_board

    def get_right(self, board):
        done = False
        combined = [False, False, False, False]
        new_board = copy.deepcopy(board)
        while not done:
            done = True
            for row_pos in range(0, 4):
                row = new_board[row_pos]
                for x in range(0, 3):
                    if row[x] > 0:
                        if row[x + 1] == 0:
                            row[x + 1] = row[x]
                            row[x] = 0
                            done = False
                        elif row[x + 1] == row[x] and not combined[row_pos]:
                            row[x + 1] = row[x] * 2
                            row[x] = 0
                            done = False
                            combined[row_pos] = True
        return new_board

    def get_up(self, board):
        done = False
        combined = [False, False, False, False]
        new_board = copy.deepcopy(board)
        while not done:
            done = True
            for col in range(0, 4):
                for row in range(1, 4):
                    if new_board[row][col] > 0:
                        if new_board[row - 1][col] == 0:
                            new_board[row - 1][col] = new_board[row][col]
                            new_board[row][col] = 0
                            done = False
                        elif new_board[row - 1][col] == new_board[row][col] and not combined[col]:
                            new_board[row - 1][col] = new_board[row][col] * 2
                            new_board[row][col] = 0
                            done = False
                            combined[col] = True
        return new_board

    def get_down(self, board):
        done = False
        combined = [False, False, False, False]
        new_board = copy.deepcopy(board)
        while not done:
            done = True
            for col in range(0, 4):
                for row in range(0, 3):
                    if new_board[row][col] > 0:
                        if new_board[row + 1][col] == 0:
                            new_board[row + 1][col] = new_board[row][col]
                            new_board[row][col] = 0
                            done = False
                        elif new_board[row + 1][col] == new_board[row][col] and not combined[col]:
                            new_board[row + 1][col] = new_board[row][col] * 2
                            new_board[row][col] = 0
                            done = False
                            combined[col] = True
        return new_board
