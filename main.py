import time
import pickle
from operator import attrgetter, itemgetter
import matplotlib.pyplot as plt
import sys
import threading

from Board import *
from Player import *
from RandomAI import *
from GoodAI import *


NUM_PLAYERS = 50
ITERATIONS = 100
RANDOM_WIN_SCORE = 1
RANDOM_TIE_SCORE = 0
#SMART_WIN_SCORE = 100
SMART_TIE_SCORE = 35
GAMES_EACH_ROUND_RANDOM = 90
GAMES_EACH_ROUND_SMART = 1
BEST_SCORE_POSSIBLE = GAMES_EACH_ROUND_RANDOM * RANDOM_WIN_SCORE + GAMES_EACH_ROUND_SMART * SMART_TIE_SCORE
MUTATION_CHANCE = 0.035

players = []

def compete_players():
    board = Board()

    for i in range(NUM_PLAYERS):
        player1 = players[i]
        player1.set_sign('X')

        turn = 1

        player2 = RandomAI('O')

        ai_type = 'rand'

        for j in range(GAMES_EACH_ROUND_RANDOM + GAMES_EACH_ROUND_SMART):
            while not board.check_for_win() and not board.is_full():
                if turn == 1:
                    player1.play(board)
                    turn = 2
                elif turn == 2:
                    player2.play(board)
                    turn = 1
            
            if board.is_full():
                if ai_type == 'rand': 
                    players[i].score += RANDOM_TIE_SCORE
                elif ai_type == 'good': 
                    players[i].score += SMART_TIE_SCORE
                    #print(i)
                    #print('awesome')
            elif board.check_for_win() == 'X':
                if ai_type == 'rand': players[i].score += RANDOM_WIN_SCORE
                # elif ai_type == 'good': players[i].score += SMART_WIN_SCORE
            
            if j == GAMES_EACH_ROUND_RANDOM - 1:
                player2 = GoodAI('O')
                ai_type = 'good'
            
            board.clear()

def generate_players():
    for i in range(NUM_PLAYERS):
        players.append(Player())

def calculate_fitness():
    sum_score = 0

    for i in range(NUM_PLAYERS):
        sum_score += players[i].score

    for i in range(NUM_PLAYERS):
        players[i].fitness = players[i].score / sum_score

def pick_player():
    num = np.random.rand(1, 1)[0][0]
    index = 0

    while num > 0:
        num -= players[index].fitness
        index += 1
    
    index -= 1

    child = Player(players[index].get_nn())
    child.mutate(MUTATION_CHANCE)

    return child

def generate_next_generation():
    global players

    calculate_fitness()

    next_generation = []

    for i in range(NUM_PLAYERS):
        next_generation.append(pick_player())
    
    players = []

    for i in range(NUM_PLAYERS):
        players.append(next_generation[i])

def pick_best_player():
    best = players[0]

    for i in range(1, NUM_PLAYERS):
        if players[i].score > best.score:
            best = players[i]
    
    return best

def main():
    global players

    best_player = Player()
    best_player.score = 0
    best_generation = 0

    num_iterations = ITERATIONS

    if len(sys.argv) > 1:
        num_iterations = int(sys.argv[1])
    
    if len(sys.argv) > 2:
        generation_file = sys.argv[2]
        with open(generation_file, 'rb') as f:
            players = pickle.load(f)

    print("STARTING " + str(num_iterations) + " ITERATIONS!")

    generate_players()

    for i in range(num_iterations):
        start_time = time.process_time()

        compete_players()

        generation_best = pick_best_player()
        if generation_best.score > best_player.score:
            best_player = Player(generation_best.get_nn())
            best_player.score = generation_best.score
            best_generation = i

        generate_next_generation()

        end_time = time.process_time()
        elapsed_time = end_time - start_time

        print("ITERATION NUMBER " + str(i + 1) + " TOOK " + str(elapsed_time) + " SECONDS. BEST SCORE WAS " + str(best_player.score) + "/" + str(BEST_SCORE_POSSIBLE) + " FROM GENERATION " + str(best_generation))
    
    print("BEST PLAYER SCORE " + str(best_player.score) + "/" + str(BEST_SCORE_POSSIBLE))

    with open('save.pickle', 'wb') as save_file:
        pickle.dump(best_player, save_file)
    
    with open('save_generation.pickle', 'wb') as save_file:
        for i in range(NUM_PLAYERS):
            players[i].score = 0
            players[i].fitness = 0
        pickle.dump(players, save_file)
    

if __name__ == '__main__':
    main()