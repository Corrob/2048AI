from enum import Enum
import pickle
import copy
import os.path
import random

GUESSING = 10

class Move(Enum):
    DOWN = 1
    RIGHT = 2
    LEFT = 3
    UP = 4

class Chain:
    def __init__(self):
        self.boards = []
        self.moves = []

    def add_move(self, num):
        if num == 0:
            self.moves.append(Move.DOWN)
        elif num == 1:
            self.moves.append(Move.RIGHT)
        elif num == 2:
            self.moves.append(Move.LEFT)
        elif num == 3:
            self.moves.append(Move.UP)

    def save(self, index):
        score = len(self.boards)
        if score > 0:
            index.boards.append(Board(self.boards[0], score))
            for x in range(len(self.moves)):
                if x < len(self.boards) - 1:
                    index.add_move(self.moves[x], self.boards[x], self.boards[x + 1], score - x)

class Board:
    def __init__(self, board, score):
        self.board = board
        self.boards_down = [] if self.can_down(board) else None
        self.boards_right = [] if self.can_right(board) else None
        self.boards_left = [] if self.can_left(board) else None
        self.boards_up = [] if self.can_up(board) else None
        self.score = score

    def get_move(self, index, other):
        scores = [0.0, 0.0, 0.0, 0.0]
        if not self.can_down(other):
            scores[0] = 0.0
        elif self.boards_down:
            down_scores = [index.get_board(b).score for b in self.boards_down]
            scores[0] = sum(down_scores) / len(down_scores)
        else:
            scores[0] = random.randrange(GUESSING)

        if not self.can_right(other):
            scores[1] = 0.0
        elif self.boards_right:
            right_scores = [index.get_board(b).score for b in self.boards_right]
            scores[1] = sum(right_scores) / len(right_scores)
        else:
            scores[1] = random.randrange(GUESSING)

        if not self.can_left(other):
            scores[2] = 0.0
        elif self.boards_left:
            left_scores = [index.get_board(b).score for b in self.boards_left]
            scores[2] = sum(left_scores) / len(left_scores)
        else:
            scores[2] = random.randrange(GUESSING)

        if not self.can_up(other):
            scores[3] = 0.0
        elif self.boards_up:
            up_scores = [index.get_board(b).score for b in self.boards_up]
            scores[3] = sum(up_scores) / len(up_scores)
        else:
            scores[3] = random.randrange(GUESSING)

        print(scores)
        return scores.index(max(scores))

    def can_left(self, board):
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
        return not self.arb_matches(board, new_board)

    def can_right(self, board):
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
        return not self.arb_matches(board, new_board)

    def can_up(self, board):
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
        return not self.arb_matches(board, new_board)

    def can_down(self, board):
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
        return not self.arb_matches(board, new_board)

    def add_move(self, move, other):
        if move == Move.DOWN and self.boards_down != None:
            self.boards_down.append(other.board)
        elif move == Move.RIGHT and self.boards_right != None:
            self.boards_right.append(other.board)
        elif move == Move.LEFT and self.boards_left != None:
            self.boards_left.append(other.board)
        elif move == Move.UP and self.boards_up != None:
            self.boards_up.append(other.board)

    def arb_matches(self, one, two):
        for row in range(0, 4):
            for col in range(0, 4):
                if one[row][col] != two[row][col]:
                    return False
        return True


    def matches(self, other):
        return self.arb_matches(self.board, other)

    def get_distance(self, other):
        dist = 0
        for row in range(0, 4):
            for col in range(0, 4):
                dist += abs(other[row][col] - self.board[row][col])
        return dist


    def print(self):
        print(self.score)
        for row in self.board:
            for num in row:
                print("{:<5}".format(num), end='')
            print()
        print()


class Index:
    def __init__(self):
        self.boards = []

    def print(self):
        for board in self.boards:
            board.print()

    def get_move(self, board):
        if not self.boards:
            return random.randrange(4)
        dists = [b.get_distance(board) for b in self.boards]
        nearest_board = self.boards[dists.index(min(dists))]
        return nearest_board.get_move(self, board)

    def add_move(self, move, old_board, new_board, score):
        old = self.get_board(old_board)
        new = self.get_board(new_board)
        if old == None:
            old = Board(old_board, score)
            self.boards.append(old)
        elif score > old.score:
            old.score = score
        if new == None:
            new = Board(new_board, score)
            self.boards.append(new)
        elif score > new.score:
            new.score = score

        old.add_move(move, new)

    def get_board(self, board):
        for b in self.boards:
            if b.matches(board):
                return b
        return None

    def save(self):
        with open('index.dat', 'wb') as fh:
            pickle.dump(self.boards, fh)

    def load(self):
        if os.path.isfile("index.dat"):
            pickle_off = open("index.dat", "rb")
            self.boards = pickle.load(pickle_off)

