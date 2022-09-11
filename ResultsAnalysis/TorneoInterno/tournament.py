# %% [markdown]
# # Tournament to evaluate ELO

# %% [markdown]
# ##  Library imports

# %%
import numpy as np
import pandas as pd
from glob import glob


import sys
sys.setrecursionlimit(199999)

# %% [markdown]
# ## Path variables

# %%
path = "best_models/*/*[!best][!temp].h5"

# %%
players = glob(path)

# %%
len(players)

# %% [markdown]
# ## DataFrame Creation

# %%
games_df = (
    pd.merge(
        pd.Series(players).rename("Player_1"),
        pd.Series(players).rename("Player_2"),
        how = "cross"
    )
    .loc[lambda a: 
        (a.Player_1 != a.Player_2) & # Eliminar partidas contra uno mismo
        ~a.apply(frozenset, axis=1).duplicated() # Eliminar duplicados ab == ba
    ]
)
games_df

# %% [markdown]
# ## Player function

# %% [markdown]
# ### Librerías

# %%
import Arena
from MCTS import MCTS
from alquerque.AlquerqueGame import AlquerqueGame
from alquerque.AlquerquePlayers import *
from alquerque.keras.NNet import NNetWrapper as NNet

import tensorflow.compat.v2 as tf
physical_devices = tf.config.list_physical_devices('GPU') 
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)


from utils import *

# %% [markdown]
# ### Juegos

# %%
def pit(players):
    
    # Game

    g = AlquerqueGame()

    # Jugadores

    print(f"{players[0]} VS {players[1]}")

    n1 = NNet(g)
    n1.load_checkpoint("/".join(players[0].split("/")[:-1]), players[0].split("/")[-1])
    args1 = dotdict({'numMCTSSims': 25, 'cpuct':1.0})
    mcts1 = MCTS(g, n1, args1)
    n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

    n2 = NNet(g)
    n2.load_checkpoint("/".join(players[1].split("/")[:-1]), players[1].split("/")[-1])
    args2 = dotdict({'numMCTSSims': 25, 'cpuct': 1.0})
    mcts2 = MCTS(g, n2, args2)
    n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

    #Juego

    arena = Arena.Arena(n1p, n2p, g, display=AlquerqueGame.display)
    
    player_1, player_2, _ =  arena.playGames(2, verbose=True)

    if player_1 > player_2:
        res = 1
    elif player_1 < player_2:
        res = 2
    else:
        res = 0

    return res

# %% [markdown]
# ## Cálculo de ELO

# %% [markdown]
# ### Aplicación de partidas

# %%
games_df = (
    games_df
    .assign(
        res = lambda a: a.apply(pit, axis = 1)
    )
)
games_df

# %% [markdown]
# ### Cálculo de ELO

# %%
elo_dict = (
    pd.DataFrame(
        pd.Series(
            np.concatenate(
                [
                    games_df.Player_1, 
                    games_df.Player_2
                ]
            )
        )
        .rename("Player")
        .drop_duplicates()
    )
    .assign(
        ELO = 0
    )
    .set_index("Player")
    .to_dict('index')
)
elo_dict

# %%
for _, row in games_df.iterrows():

    K = 20 # Development coefficient

    rat_1 = elo_dict[row["Player_1"]]["ELO"]
    rat_2 = elo_dict[row["Player_2"]]["ELO"]

    expected_score_1 = 1 / (1 + 10**((rat_2 - rat_1)/400))
    expected_score_2= 1 / (1 + 10**((rat_1 - rat_2)/400))

    if row["res"] == 1:

        rat_1_new = rat_1 + K * (1 - expected_score_1)
        rat_2_new = rat_2 + K * (0 - expected_score_2)

    elif row["res"] == 2:
        
        rat_2_new = rat_2 + K * (1 - expected_score_2)
        rat_1_new = rat_1 + K * (0 - expected_score_1)
        
    else:
        
        rat_2_new = rat_2 + K * (0.5 - expected_score_2)
        rat_1_new = rat_1 + K * (0.5 - expected_score_1)

    # Actualizar valores ELO

    elo_dict[row["Player_1"]]["ELO"] = rat_1_new
    elo_dict[row["Player_2"]]["ELO"] = rat_2_new

# %%
elo_df = pd.DataFrame.from_dict(elo_dict, orient = "index")
elo_df

# %%
elo_df.to_csv("ELO.csv", sep = ";")


