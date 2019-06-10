import copy
import time
import pickle
from operator import attrgetter, itemgetter
import matplotlib.pyplot as plt
import sys

from Board import *
from Player import *
from RandomAI import *

NUM_PLAYERS = 100
ITERATIONS = 100
GAMES_EACH_ROUND = 150
SELECT_PERCENTAGE = 0.15
MUTATION_CHANCE = 0.15
MUTATION_DELTA = 0.2
MUTATION_ROUNDS = 5

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
                
                #moves_played += 1
                #board.print_state()
            
            if board.is_full():
                wins[i] += 0.4
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

    for x in range(MUTATION_ROUNDS):
        base_len = init_len * (x + 1)
        for i in range(int(SELECT_PERCENTAGE * NUM_PLAYERS)):
            players.append(players[i])
            wins[i + base_len] = 0
            players[-1].mutate(MUTATION_CHANCE, MUTATION_DELTA)

def select_best():
    global wins, players

    wins_sorted = sorted(wins.items(), key=itemgetter(1), reverse=True)
    selected_players = []

    best_player = players[wins_sorted[0][0]]

    return best_player

def get_average_wins():
    win_sum = 0
    for count in wins.values():
        win_sum += count
    
    return win_sum / len(wins)

def main():
    best_player = None
    iterations = []
    wins_average = []
    most_wins = []

    num_iterations = ITERATIONS

    if len(sys.argv) > 1:
        num_iterations = int(sys.argv[1])
    
    print("STARTING " + str(num_iterations) + " ITERATIONS!")

    for i in range(num_iterations):
        start_time = time.process_time()

        generate_players()
        compete_players()

        iterations.append(i)
        wins_average.append(get_average_wins())
        most_wins.append(sorted(wins.items(), key=itemgetter(1), reverse=True)[0][1])
        #if i % 10 == 0:
            #print(sorted(wins.items(), key=itemgetter(1), reverse=True))


        if i < num_iterations - 1:
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

    plt.plot(iterations, wins_average, 'r-')
    plt.plot(iterations, most_wins, 'b-')
    plt.show()

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