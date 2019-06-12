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
GAMES_EACH_ROUND = 100
MUTATION_CHANCE = 0.035

players = []

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
            
            if board.is_full():
                players[i].score += 0.25
            elif board.check_for_win() == 'X':
                players[i].score += 1
            
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
    best_player = Player()
    best_player.score = 0

    num_iterations = ITERATIONS

    if len(sys.argv) > 1:
        num_iterations = int(sys.argv[1])
    
    print("STARTING " + str(num_iterations) + " ITERATIONS!")

    generate_players()

    for i in range(num_iterations):
        start_time = time.process_time()

        compete_players()

        generation_best = pick_best_player()
        if generation_best.score > best_player.score:
            best_player = Player(generation_best.get_nn())
            best_player.score = generation_best.score

        generate_next_generation()

        end_time = time.process_time()
        elapsed_time = end_time - start_time

        print("ITERATION NUMBER " + str(i + 1) + " TOOK " + str(elapsed_time) + " SECONDS.")
    
    print("BEST PLAYER SCORE " + str(best_player.score) + "/" + str(GAMES_EACH_ROUND))

    with open('save.pickle', 'wb') as save_file:
        pickle.dump(best_player, save_file)
    

if __name__ == '__main__':
    main()