import pygame
from globe import *

# ----- Game vars -----

amount = 10
# board = [[0 for j in range(amount)] for i in range(amount)]

# ----- GUI vars -----

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

board = [
	[7, 8, 0, 4, 0, 0, 1, 2, 0],
	[6, 0, 0, 0, 7, 5, 0, 0, 9],
	[0, 0, 0, 6, 0, 1, 0, 7, 8],
	[0, 0, 7, 0, 4, 0, 2, 6, 0],
	[0, 0, 1, 0, 5, 0, 9, 3, 0],
	[9, 0, 4, 0, 6, 0, 0, 0, 5],
	[0, 7, 0, 3, 0, 0, 0, 1, 2],
	[1, 2, 0, 0, 0, 7, 4, 0, 0],
	[0, 4, 9, 2, 0, 6, 0, 0, 7]
]

rows = [{i: False} for i in range(amount) for k in range(amount)]
cols = [{i: False} for i in range(amount) for r in range(amount)]

# ----- Game methods -----


def write(i, j, number):
	if rows[i][number] or cols[j][number]:
		return False
	rows[i][number] = True
	cols[j][number] = True
	board[i][j] = number
	return True


def contains(i, j):
	return board[i][j] != 0


def erase(i, j):
	number = board[i][j]
	if number == 0:
		return False
	board[i][j] = 0
	rows[i][number] = False
	cols[j][number] = False
	return True


def win():
	for i, j in range(amount), range(amount):
		if board[i][j] == 0:
			return False
	return True


# ----- GUI methods -----

def redraw_screen(screen):
	screen.fill(BACKGROUND_COLOR)
	draw_board()
	pygame.display.update()


def draw_board(window):
	length = WIDTH / amount
	for i in range(amount + 1):
		pygame.draw.line()

