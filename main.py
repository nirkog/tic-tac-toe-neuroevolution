import copy
import time
import pickle
from operator import attrgetter, itemgetter

from Board import *
from Player import *
from RandomAI import *

NUM_PLAYERS = 100
ITERATIONS = 100
GAMES_EACH_ROUND = 150
SELECT_PERCENTAGE = 0.35
MUTATION_CHANCE = 0.03
MUTATION_DELTA = 0.1
MUTATION_RATE = 0.8

players = []
wins = {}

def generate_players():
    init_len = len(players)
    to_generate = NUM_PLAYERS - init_len

    #print(to_generate)

    for i in range(to_generate):
        players.append(Player())
        wins[i + init_len] = 0

def compete_players():
    board = Board()

    for i in range(NUM_PLAYERS):
        player1 = players[i]
        player1.set_sign('X')

        turn = 1

        player2 = RandomAI('O')

        for j in range(GAMES_EACH_ROUND):
            while not board.check_for_win() and not board.is_full():
                if turn == 1:
                    player1.play(board)
                    turn = 2
                elif turn == 2:
                    player2.play(board)
                    turn = 1
                
                #board.print_state()
            
            if board.is_full():
                wins[i] += 0.25
                #print('TIE!')
            elif board.check_for_win() == 'X':
                wins[i] += 1
            
            board.clear()

def select_players():
    global wins, players

    wins_sorted = sorted(wins.items(), key=itemgetter(1), reverse=True)
    selected_players = []

    for i in range(int(NUM_PLAYERS * SELECT_PERCENTAGE)):
        selected_players.append(players[wins_sorted[i][0]])
    
    players = []
    wins = {}

    for i in range(int(NUM_PLAYERS * SELECT_PERCENTAGE)):
        players.append(selected_players[i])
        wins[i] = 0

def mutate_players():
    init_len = len(players)

    for i in range(len(players)):
        players.append(players[i])
        wins[i + init_len] = 0
        if np.random.rand(1, 1)[0][0] < MUTATION_RATE:
            players[i + init_len - 1].mutate(MUTATION_CHANCE, MUTATION_DELTA)

def select_best():
    global wins, players

    wins_sorted = sorted(wins.items(), key=itemgetter(1), reverse=True)
    selected_players = []

    best_player = players[wins_sorted[0][0]]

    return best_player

def main():
    best_player = None

    for i in range(ITERATIONS):
        start_time = time.process_time()

        generate_players()
        compete_players()

        if i % 10 == 0:
            print(sorted(wins.items(), key=itemgetter(1), reverse=True))

        if i < ITERATIONS - 1:
            select_players()
            mutate_players()

            end_time = time.process_time()
            elapsed_time = end_time - start_time

            print("ITERATION NUMBER " + str(i + 1) + " TOOK " + str(elapsed_time) + " SECONDS.")
        else:
            print('last round')
            best_player = select_best()

            out = open('save.pickle', 'wb')
            pickle.dump(best_player, out)
            out.close()

    best_player.set_sign('X')
    board = Board()
        
    while not board.check_for_win() and not board.is_full():
        best_player.play(board)

        board.print_state()

        if not board.check_for_win() and not board.is_full():
            pos = input("Enter posotion: ")
            pos = list(map(int, pos.split(',')))

            board.mark_O(pos)
    
    if board.is_full():
        print("TIE!")
    elif not board.check_for_win() == False:
        winner = board.check_for_win()

        if winner == 'X':
            print("YOU LOSE!")
        else:
            print("YOU WIN!")
    

if __name__ == '__main__':
    main()