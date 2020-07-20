from globe import *

# ----- Game vars -----

board = [[0 for j in range(AMOUNT)] for i in range(AMOUNT)]
'''
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
'''
rows = [{x: False for x in range(1, AMOUNT + 1)} for k in range(AMOUNT)]
cols = [{x: False for x in range(1, AMOUNT + 1)} for k in range(AMOUNT)]
sqrs = [{x: False for x in range(1, AMOUNT + 1)} for k in range(AMOUNT)]

rows_win = [AMOUNT for i in range(AMOUNT)]  # for each row how many items are missing
number_of_full = 0

# ----- GUI vars -----

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")
length = int(WIDTH / AMOUNT)

active_square = None

# ----- Game methods -----


def write(i, j, number):
	global number_of_full
	sqr = find_square(i, j)
	if rows[i][number] or cols[j][number] or sqrs[sqr][number]:
		return False
	rows[i][number] = True
	rows_win[i] -= 1
	if rows_win[i] == 0:
		number_of_full += 1
	cols[j][number] = True
	sqrs[sqr][number] = True
	board[i][j] = number
	return True


def find_square(i, j):
	if i < 3 and j < 3:
		return 0
	if 6 > i >= 3 > j:
		return 1
	if 9 > i >= 6 and j < 3:
		return 2
	if i < 3 <= j < 6:
		return 3
	if 6 > i >= 3 and 3 <= j < 6:
		return 4
	if 9 > i >= 6 > j >= 3:
		return 5
	if i < 3 and 6 <= j < 9:
		return 6
	if 3 <= i < 6 <= j < 9:
		return 7
	if 9 > i >= 6 and 6 <= j < 9:
		return 8


def contains(i, j):
	return board[i][j] != 0


# assuming i,j isn't empty
def erase(i, j):
	global number_of_full
	sqr = find_square(i, j)
	number = board[i][j]
	if number == 0:
		return False
	board[i][j] = 0
	rows[i][number] = False
	if rows_win[i] == 0:
		number_of_full -= 1
	rows_win[i] += 1
	cols[j][number] = False
	sqrs[sqr][number] = False
	return True


def win():
	return number_of_full == AMOUNT


def enter(event, x, y):
	number = NUMBERS.index(event.key) + 1
	# Game:
	i, j = int((y / WIDTH) * AMOUNT), int((x / WIDTH) * AMOUNT)
	num = None
	if contains(i, j):
		num = board[i][j]
		erase(i, j)
	flag = write(i, j, number)
	if not flag and num is not None:  # We over wrote on a number with an invalid one
		flag = True
		number = num
		write(i, j, number)
	return flag, number


def main():
	global active_square
	pygame.init()
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
					if active_square is not None:
						pygame.draw.rect(screen, BACKGROUND_COLOR, active_square, 3)
					draw_board()
					x, y = event.pos
					if x < WIDTH and y < WIDTH:
						pos = (int(int((x / WIDTH) * AMOUNT) * length), int(int((y / WIDTH) * AMOUNT) * length))
						active_square = pygame.Rect(pos[0], pos[1], length, length)
						pygame.draw.rect(screen, (255, 0, 0), active_square, 3)
						pygame.display.update()

			if event.type == pygame.KEYDOWN:
				if event.key in NUMBERS and active_square is not None:
					x, y = int(active_square.x + (length / 2.4)), int(active_square.y + (length / 3.5))
					if x < WIDTH and y < WIDTH:
						# Game:
						flag, number = enter(event, x, y)

						# GUI:
						if flag:
							draw_number(x, y, number)


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


def draw_number(x, y, number):
	if active_square is not None:
		pygame.draw.rect(screen, BACKGROUND_COLOR, active_square, 3)
		screen.fill(BACKGROUND_COLOR, active_square)
	draw_board()
	pygame.draw.rect(screen, (255, 0, 0), active_square, 3)
	word_surface = pygame.font.SysFont("microsoftjhengheimicrosoftjhengheiuilight", 20).render(str(number), 0,
	                                                                                           MAIN_COLOR)
	screen.blit(word_surface, (x, y))
	pygame.display.update()


if __name__ == "__main__":
	main()

