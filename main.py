import time, os, random

SIZE = 0

#####################################################################################

def main():
	global SIZE, COLUMN_WIDTH, SCREEN_WIDTH

	while True:
		SIZE = int(input("What size map? (1 to 60) "))
		print("....Loading.")
		map = [[random.choice([True, True, False]) for i in range(SIZE)]
		       for i in range(SIZE)]
		while path_find(
		    (random.randint(0, SIZE - 1), random.randint(0, SIZE - 1)),
		    (random.randint(0, SIZE - 1), random.randint(0, SIZE - 1)),
		    map)[0] == (-1, -1):
			print("....Loading.")
		input("=== Press Enter to generate new map ===")
		clear_console()
		time.sleep(1)

#####################################################################################

def clear_console():
	# For Windows
	if os.name == 'nt':
		_ = os.system('cls')
	# For macOS and Linux
	else:
		_ = os.system('clear')


#####################################################################################


def path_find(start, goal, map):
	closedset = []
	openset = [start]
	route_map = [[(-1, -1) for i in range(SIZE)] for j in range(SIZE)]
	tcost = [[9999999 for i in range(SIZE)]
	         for j in range(SIZE)]  # Current Travel Cost from Start
	hcost = [[9999999 for i in range(SIZE)]
	         for j in range(SIZE)]  # Heuristic Travel Cost  to  End

	tcost[start[1]][start[0]] = 0
	hcost[start[1]][start[0]] = calc_heuristic(
	    start, goal) + tcost[start[1]][start[0]]

	while openset:
		next = 0
		x = openset[0][0]
		y = openset[0][1]
		for i in range(1, len(openset)):
			x1 = openset[i][0]
			y1 = openset[i][1]
			if hcost[y1][x1] < hcost[y][x]:
				x = x1
				y = y1
				next = i

		if openset[next] == goal:
			print_route(start, goal, map, route_map,
			            path_route(route_map, goal))
			return path_route(route_map, goal)

		neighbors = []
		if x > 0: neighbors.append((x - 1, y))
		if y > 0: neighbors.append((x, y - 1))
		if x < SIZE - 1: neighbors.append((x + 1, y))
		if y < SIZE - 1: neighbors.append((x, y + 1))

		for neighbor in neighbors:
			x1 = neighbor[0]
			y1 = neighbor[1]
			if not map[y1][x1]:
				closedset.append(neighbor)
				continue
			try:
				closedset.index(neighbor)
				continue
			except ValueError:
				new_tcost = tcost[y][x] + 1
				try:
					openset.index(neighbor)
					if new_tcost > tcost[y1][x1]: continue
				except ValueError:
					openset.append(neighbor)
				route_map[y1][x1] = openset[next]
				tcost[y1][x1] = new_tcost
				hcost[y1][x1] = new_tcost + calc_heuristic(neighbor, goal)

		closedset.append(openset.pop(next))
	return [(-1, -1)]


#####################################################################################


def calc_heuristic(node, goal):
	return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


#####################################################################################


def path_route(route, next):
	final_route = []
	while next != (-1, -1):
		x = next[0]
		y = next[1]
		final_route.append(next)
		next = route[y][x]
	return final_route


#####################################################################################


def print_route(start, goal, map, route_map, final_route):
	graphic = '\n'
	for i in range(SIZE):
		for j in range(SIZE):
			en_route = False
			try:
				final_route.index(route_map[i][j])
				en_route = True
			except ValueError:
				False
			if start == (j, i) or goal == (j, i): graphic += "× "
			elif not map[i][j]: graphic += "██"
			elif route_map[i][j] == (j - 1, i): graphic += "← "
			elif route_map[i][j] == (j + 1, i): graphic += "→ "
			elif route_map[i][j] == (j, i - 1): graphic += "↑ "
			elif route_map[i][j] == (j, i + 1): graphic += "↓ "
			else: graphic += "  "
		graphic += '\n'

	for i in range(len(graphic)):
		print(graphic[i], end='')
		time.sleep(0.00001)

	print('\nROUTE: ×', end=' ')
	for i in range(1, len(final_route) - 1):
		x1 = final_route[i][0]
		y1 = final_route[i][1]
		x2 = final_route[i + 1][0]
		y2 = final_route[i + 1][1]
		if x2 - x1 == 1: print('→', end=' ')
		elif x1 - x2 == 1: print('←', end=' ')
		elif y2 - y1 == 1: print('↓', end=' ')
		elif y1 - y2 == 1: print('↑', end=' ')
	print('×')


#####################################################################################

main()
