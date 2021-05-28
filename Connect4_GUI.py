import pygame
import numpy as np


BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7


EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = -1



def draw_board(board, rew, ep):
    board_flipped = np.flip(board, 0)
    img1 = font.render('Running Reward: {:.2f}'.format(rew), True, YELLOW)
    img2 = font.render('Episodes: {}'.format(ep), True, YELLOW)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board_flipped[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), heigh-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            if board_flipped[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), heigh-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

    screen.blit(img1, (50, 20))
    screen.blit(img2, (400, 20))
    pygame.display.update()
    screen.fill(pygame.Color("black"))


pygame.init()
SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
heigh = (ROW_COUNT+1) * SQUARESIZE
font = pygame.font.Font(None, 40)
size = (width, heigh)
RADIUS = int(SQUARESIZE/2 - 5)
screen = pygame.display.set_mode(size)
