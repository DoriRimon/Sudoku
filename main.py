import pygame
from globe import *

# ----- Game vars -----

# board = [[0 for j in range(amount)] for i in range(amount)]
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

rows = [{i: False} for i in range(AMOUNT) for k in range(AMOUNT)]
cols = [{i: False} for i in range(AMOUNT) for r in range(AMOUNT)]

# ----- GUI vars -----

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")
length = int(WIDTH / AMOUNT)

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
	for i, in range(AMOUNT):
		for j in range(AMOUNT):
			if board[i][j] == 0:
				return False
	return True


def main():
	redraw_screen()
	draw_board()
	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					redraw_screen()
					draw_board()
					x, y = event.pos
					if x < WIDTH and y < WIDTH:
						pos = (int(int((x / WIDTH) * AMOUNT) * length), int(int((y / WIDTH) * AMOUNT) * length))
						pygame.draw.rect(screen, (255, 0, 0), (pos[0], pos[1], length, length), 3)
						pygame.display.update()

# ----- GUI methods -----


def redraw_screen():
	screen.fill(BACKGROUND_COLOR)
	pygame.display.update()


def draw_board():
	for i in range(AMOUNT + 1):
		width = 1
		if i % 3 == 0 and i != 0:
			width = 3
		pygame.draw.line(screen, MAIN_COLOR, (0, length * i), (WIDTH, length * i), width)
		if i != AMOUNT:
			pygame.draw.line(screen, MAIN_COLOR, (length * i, 0), (length * i, WIDTH), width)
	pygame.display.update()


if __name__ == "__main__":
	main()

