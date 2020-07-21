from globe import *
from PyUI import *

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


def enter(x, y, number):
	# Game:
	i, j = int(y / length), int(x / length)
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


def solve_backtracking():
	global active_square
	for num in range(1, AMOUNT + 1):
		x, y = active_square.x, active_square.y
		if x + length < WIDTH:
			x += length
		elif y + length < WIDTH:
			x = 0
			y += length
		elif win():
			return True
		else:
			return False
		active_square = pygame.Rect(x, y, length, length)
		flag, number = enter(x, y, num)
		if flag:
			draw_number(int(active_square.x + (length / 2.4)), int(active_square.y + (length / 3.5)), number, True)
			draw_square(x, y, (0, 255, 0))
			# print("rows:")
			# for i in range(AMOUNT):
			# 	print(rows[i])
			if solve_backtracking():
				return True
			i, j = int(y / length), int(x / length)
			print("got here")
			erase(i, j)  # j * length = x, i * length = y
			if active_square is not None:
				pygame.draw.rect(screen, BACKGROUND_COLOR, active_square, 3)
				screen.fill(BACKGROUND_COLOR, active_square)
			draw_board()
			draw_square(active_square.x, active_square.y, (255, 0, 0))
			x, y = active_square.x, active_square.y
			if x - length >= 0:
				x -= length
			elif y - length >= WIDTH:
				x = WIDTH - length
				y -= length
			active_square.x, active_square.y = x, y
	return False


def back_track(i, j):
	if contains(i, j):
		next_place = next_square(i, j)
		if type(next_place) is bool:
			return
		else:
			i, j = next_place[0], next_place[1]
		print(i, ", ", j)
	for num in range(1, AMOUNT + 1):
		if write(i, j, num):
			naive_board_print(i, j)
			print("rows:")
			for k in range(AMOUNT):
				print(rows[k])
			if back_track(i, j):
				return True
			erase(i, j)
	return False


def next_square(i, j):
	j += 1
	if j > 8:
		j = 0
		i += 1
	if i > 8:
		return True
	return i, j


def last_square(i, j):
	j -= 1
	if j < 0:
		j = 8
		i -= 1
	if i < 0:
		return False
	return i, j


def on_click(view):
	global active_square
	# active_square = pygame.Rect(0, 0, length, length)
	# solve_backtracking()
	back_track(0, 0)


def main():
	global active_square
	pygame.init()
	solve = Button(WIDTH - 80, WIDTH + length / 9, 75, 35) \
		.set_text("solve")\
		.set_on_click_listener(on_click) \
		.set_on_hover_listener(on_hover) \
		.set_on_unhover_listener(on_unhover) \
		.set_color(Color(0, 0, 0))

	redraw_screen()
	draw_board()
	clock = pygame.time.Clock()

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
	# - || inserting some elements || -
	'''
	inserts = [(0, 0, 7), (0, 1, 8), (0, 3, 4), (0, 6, 1), (0, 7, 2),
	           (1, 0, 6), (1, 4, 7), (1, 5, 5), (1, 8, 9),
	           (2, 3, 6), (2, 5, 1), (2, 7, 7), (2, 8, 8),
	           (3, 2, 7), (3, 4, 4), (3, 6, 2), (3, 7, 6),
	           (4, 2, 1), (4, 4, 5), (4, 6, 9), (4, 7, 3),
	           (5, 0, 9), (5, 2, 4), (5, 4, 6), (5, 8, 5),
	           (6, 1, 7), (6, 3, 3), (6, 7, 1), (6, 8, 2),
	           (7, 0, 1), (7, 1, 2), (7, 5, 7), (7, 6, 4),
	           (8, 1, 4), (8, 2, 9), (8, 3, 2), (8, 5, 6), (8, 8, 7)]
	for i, j, number in inserts:
		active_square = pygame.Rect(j * length, i * length, length, length)
		x, y = int(active_square.x + (length / 2.4)), int(active_square.y + (length / 3.5))

		# Game:
		flag, number = enter(x, y, number)

		# GUI:
		if flag:
			draw_number(x, y, number)
	'''
	run = True
	while run:
		events = pygame.event.get()
		for event in events:
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
					else:
						active_square = None

			if event.type == pygame.KEYDOWN:
				if event.key in NUMBERS and active_square is not None:
					x, y = int(active_square.x + (length / 2.4)), int(active_square.y + (length / 3.5))
					if x < WIDTH and y < WIDTH:
						# Game:
						flag, number = enter(x, y, NUMBERS.index(event.key) + 1)

						# GUI:
						if flag:
							draw_number(x, y, number)

		ViewHandler.handle_view_events(events)

		ViewHandler.render_views(screen)
		pygame.display.update()
		clock.tick(60)


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


def draw_square(x, y, color):
	pygame.draw.rect(screen, color, (x, y, length, length), 3)
	pygame.display.update()


def draw_number(x, y, number, no_board_draw=False, override=False):
	if active_square is not None:
		pygame.draw.rect(screen, BACKGROUND_COLOR, active_square, 3)
		screen.fill(BACKGROUND_COLOR, active_square)
	if not no_board_draw:
		draw_board()
	if number != 0:
		if active_square is not None and not override:
			pygame.draw.rect(screen, (255, 0, 0), active_square, 3)
		word_surface = pygame.font.SysFont("microsoftjhengheimicrosoftjhengheiuilight", 20).render(str(number), 0,
		                                                                                           MAIN_COLOR)
		screen.blit(word_surface, (x, y))
	pygame.display.update(active_square)


def naive_board_print(i, j):
	global active_square
	while i < AMOUNT and j < AMOUNT:
		x, y = j * length, i * length
		# pos = (int(int((x / WIDTH) * AMOUNT) * length), int(int((y / WIDTH) * AMOUNT) * length))
		active_square = pygame.Rect(x, y, length, length)
		x, y = int(x + (length / 2.4)), int(y + (length / 3.5))
		if contains(i, j):
			draw_number(x, y, 0, False, True)
		draw_number(x, y, board[i][j], False, True)
		next_place = next_square(i, j)
		if type(next_place) is bool:
			return
		i, j = next_place[0], next_place[1]


def on_hover(view):
	view.text.set_color(Color(255, 0, 0))


def on_unhover(view):
	view.text.set_color(Color(0, 0, 0))


if __name__ == "__main__":
	main()
