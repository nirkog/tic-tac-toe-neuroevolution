import sys
import pickle

from Player import *
from Board import *

file_name = sys.argv[1]

save_file = open(file_name, 'rb')
player = pickle.load(save_file)
save_file.close()

board = Board()
player.set_sign('X')
turn = 1

while not board.check_for_win() and not board.is_full():
    if turn == 1:
        player.play(board)
        turn = 2

        board.print_state_grid()
    else:
        pos_valid = False

        while not pos_valid:
            pos = []
            pos_str = input("Enter position: ")
            pos.append(int(pos_str[0]) - 1)
            pos.append(int(ord(pos_str[1]) - ord('a')))

            print(pos)

            if board.is_empty(pos):
                pos_valid = True

        board.mark_O(pos)
        turn = 1

if board.check_for_win() != False:
    if board.check_for_win() == 'X':
        print("YOU LOSE!")
    elif board.check_for_win() == 'O':
        print("YOU WIN!")
else:
    print("TIE!")