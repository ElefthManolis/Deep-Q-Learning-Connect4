import gym
from gym.spaces import Discrete, Box
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
from Connect4_GUI import *
from Connect4_MinMax import *
import random

AGENT_WINS = 0
MINMAX_WINS = 0


def doAction(action, board, turn):
    for i in range(5, -1, -1):
        if board[i][action] == 0:
            if turn == -1:
                board[i][action] = -1
                return board
            else:
                board[i][action] = 1
                return board


def checkIfValid(action, board):
    for i in range(0, 6):
        if board[i][action] == 0:
            return True
    return False


def checkForWin(board):
    # Check the rows
    check = False
    for i in range(0, board.shape[0]):
        for j in range(0, board.shape[1]-3):
            if (board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] == -1) or (board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3] == 1):
                check = True

    # Check the columns
    for i in range(0, board.shape[1]):
        for j in range(0, board.shape[0]-3):
            if (board[j][i] == board[j+1][i] == board[j+2][i] == board[j+3][i] == -1) or (board[j][i] == board[j+1][i] == board[j+2][i] == board[j+3][i] == 1):
                check = True

    # Check the diagonals
    for i in range(0, 3):
        for j in range(0, 4):
            if (board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] == -1) or (board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] == 1):
                check = True

    # Check the diagonals
    for i in range(3, board.shape[0]):
        for j in range(0, 4):
            if (board[i][j] == board[i-1][j+1] == board[i-2][j+2] == board[i-3][j+3] == -1) or (board[i][j] == board[i-1][j+1] == board[i-2][j+2] == board[i-3][j+3] == 1):
                check = True
    return check


class Connect4Env(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.action_space = Discrete(7)
        self.turn = -1
        self.observation_space = Box(low=np.array([[-1, -1, -1, -1, -1, -1, -1],
                                                   [-1, -1, -1, -1, -1, -1, -1],
                                                   [-1, -1, -1, -1, -1, -1, -1],
                                                   [-1, -1, -1, -1, -1, -1, -1],
                                                   [-1, -1, -1, -1, -1, -1, -1],
                                                   [-1, -1, -1, -1, -1, -1, -1]]), high=np.array([[1, 1, 1, 1, 1, 1, 1],
                                                                                                  [1, 1, 1, 1,
                                                                                                   1, 1, 1],
                                                                                                  [1, 1, 1, 1,
                                                                                                   1, 1, 1],
                                                                                                  [1, 1, 1, 1,
                                                                                                   1, 1, 1],
                                                                                                  [1, 1, 1, 1,
                                                                                                   1, 1, 1],
                                                                                                  [1, 1, 1, 1, 1, 1, 1]]))
        # Initialize the board of the game with 6 rows and 7 columns
        self.state = np.zeros((6, 7))
        self.game_length = 42

    def step(self, action, board):
        global MINMAX_WINS, AGENT_WINS

        if not checkIfValid(action, board):
            info = {}
            return board, -100, True, info

        self.state = doAction(action, board, self.turn)

        self.game_length -= 1
        self.turn *= -1

        # Calculate reward
        reward = score_position(board, -1)*2

        if checkForWin(board):
            reward = 1000
            AGENT_WINS += 1
            print('AGENT wins are: ', AGENT_WINS)

        # Check if the game is ended
        if self.game_length <= 0 or checkForWin(board):
            done = True
            info ={}
            return self.state, reward, done, info
        else:
            done = False



        bot_action = random.randint(0, 6)
        while not checkIfValid(bot_action, board):
            bot_action = random.randint(0, 6)
        #move , re = MinMax(board, 2, -math.inf, math.inf, True)


        self.state = doAction(bot_action, board, self.turn)
        #self.state = doAction(move, board, self.turn)


        self.game_length -= 1
        self.turn *= -1

        if checkForWin(board):
            reward = -1000
            MINMAX_WINS += 1
            print('MINIMAX wins are: ', MINMAX_WINS)


        # Check if the game id ended
        if self.game_length <= 0 or checkForWin(board):
            done = True
        else:
            done = False


        info ={}
        return board, reward, done, info

    def reset(self):
        self.state = np.zeros((6, 7))
        self.game_length = 42
        self.turn = -1
        return self.state

    def render(self, board, rew, ep):
        draw_board(board, rew, ep)

    def close(self):
        pass

    def getTurn(self):
        return self.turn
