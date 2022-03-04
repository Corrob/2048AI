from PIL import ImageGrab
import copy
#import easyocr
import pyautogui
import random
import time
import sys
from index import Index, Chain
from algo import Algo

BOARD = "board.png"
#chain = Chain()
#index = Index()

def quit():
    #chain.save(index)
    #index.save()
    sys.exit()

def print_board(board):
    for row in board:
        for num in row:
            print("{:<5}".format(num), end='')
        print()

def pix_diff(one, two):
    return abs(one[0] - two[0]) + abs(one[1] - two[1]) + abs(one[2] - two[2]) + abs(one[3] - two[3])

PIX_THRESH = 15

def pix_to_num(pix):
    if pix_diff(pix, (207, 193, 178, 255)) < PIX_THRESH:
        return 0
    elif pix_diff(pix, (240, 228, 217, 255)) < PIX_THRESH:
        return 2
    elif pix_diff(pix, (239, 225, 197, 255)) < PIX_THRESH:
        return 4
    elif pix_diff(pix, (251, 176, 108, 255)) < PIX_THRESH:
        return 8
    elif pix_diff(pix, (255, 145, 82, 255)) < PIX_THRESH:
        return 16
    elif pix_diff(pix, (255, 115, 79, 255)) < PIX_THRESH:
        return 32
    elif pix_diff(pix, (255, 78, 16, 255)) < PIX_THRESH:
        return 64
    elif pix_diff(pix, (240, 210, 96, 255)) < PIX_THRESH:
        return 128
    elif pix_diff(pix, (240, 207, 72, 255)) < PIX_THRESH:
        return 256
    elif pix_diff(pix, (241, 204, 42, 255)) < PIX_THRESH:
        return 512
    elif pix_diff(pix, (241, 201, 0, 255)) < 3:
        return 1024
    elif pix_diff(pix, (242, 198, 0, 255)) < 3:
        return 2048
    elif pix_diff(pix, (238, 227, 207, 255)) < PIX_THRESH:
        print('Game over!')
        quit()
    else:
        print('Unsupported pixel: ')
        print(pix)
        quit()

def read_board_new(image):
    board = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    x_pix = [40, 160, 280, 400]
    y_pix = [30, 150, 270, 400]
    for x in range(0, 4):
        for y in range(0, 4):
            board[y][x] = pix_to_num(image.getpixel((x_pix[x], y_pix[y])))

    return board

class MoveMaker:
    def __init__(self):
        self.moves = ['down', 'right', 'left', 'up']

    def make_move(self, board):
        #chain.boards.append(board)
        #best_move = index.get_move(board)
        best_move = Algo(board).get_move()
        #chain.add_move(best_move)
        print('Pressing %s' % self.moves[best_move])
        pyautogui.press(self.moves[best_move])

def main():
    #index.load()
    #print("Index size: %d" % len(index.boards))
    time.sleep(1)
    move_maker = MoveMaker()
    while True:
        screen = ImageGrab.grab((28, 288, 530, 790))
        screen.save("board.png")
        board = read_board_new(screen)
        print_board(board)
        move_maker.make_move(board)
        time.sleep(0.15)

if __name__ == "__main__":
    main()
