import Arena
from MCTS import MCTS
from alquerque.AlquerqueGame import AlquerqueGame
from alquerque.AlquerquePlayers import *
from alquerque.keras.NNet import NNetWrapper as NNet

import sys
sys.setrecursionlimit(199999)

import tensorflow.compat.v2 as tf
physical_devices = tf.config.list_physical_devices('GPU') 
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

human_vs_cpu = True

g = AlquerqueGame()

# all players
rp = RandomPlayer(g).play
hp = HumanAlquerquePlayer(g).play



# nnet players
n1 = NNet(g)
n1.load_checkpoint('./alquerque/Best_models/', 'pesado.h5')

args1 = dotdict({'numMCTSSims': 150, 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

if human_vs_cpu:
    player2 = hp
else:
    n2 = NNet(g)
    n2.load_checkpoint('./temp_3/', 'best.h5')
    args2 = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
    mcts2 = MCTS(g, n2, args2)
    n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

    player2 = n2p  # Player 2 is neural network if it's cpu vs cpu.

arena = Arena.Arena(n1p, player2, g, display=AlquerqueGame.display)

print(arena.playGames(2, verbose=True))
