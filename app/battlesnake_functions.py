import heapq
import numpy as np
import math
#create a board and fill it with food, snakes, and our snake
def init_board(food_list, snake_list, width, height):
	#initialize a 2d list of 0's with width columns and height rows.
	board = [([0] * width) for row in xrange(height)]
	#fill in food locations
	for food in food_list['data']:
		x = food['x']
		y = food['y']
		board[y][x] = 'food'
	#fill in snake body locations with their id
	for snake in snake_list['data']: #snake contains all info within a snake's 'data'
		for index in range(0, len(snake['body']['data'])):
			x = snake['body']['data'][index]['x']
			y = snake['body']['data'][index]['y']
			board[y][x] = [snake['id'], index]
	return board

#to refer an x,y point on the board, type it as board[y][x]
#checks if point xy is an obstacle
def is_obstacle(x, y, board):
	if (x < 0 or x >= len(board[0]) or y < 0 or y >= len(board)):
		return True
	if (board[y][x] != 'food' and board[y][x] != 0):
		return True
	return False

#find slope between two points. Keep in mind for battlesnake the 
#top left tile of the board is [0,0] and the bottom right tile
#of the board is [width-1, height-1]
def find_slope(x1, y1, x2, y2):
	rise = y1 - y2
	run = (x1 - x2)
	return (float(rise)/float(run))*-1.0 #we need to multiply by -1 because y values become larger when you go down the board.
	#returns a positive or negative float, which will be our slope.

#Takes in the board and our snakes head location
#Goes through each tile location 2 tiles away and checks
#what is in it.
#Throw in other fucntions depending on what is present
def checkTwoTilesAway(board, x, y):
	#checks for if the locations 2 tiles away are out of the board
	rowMinus1 = False
	rowMinus2 = False
	rowPlus1 = False
	rowPlus2 = False
	colMinus1 = False
	colMinus2 = False
	colPlus1 = False
	colPlus2 = False
	if(x - 2 < 0):
		rowMinus2 = True
	if(x - 1 < 0):
		rowMinus1 = True
	if(y - 2 < 0):
		colMinus2 = True
	if(y - 1 < 0):
		colMinus2 = True
	if(x + 1 > len(board)):
		rowPlus1 = True
	if(x + 2 > len(board)):
		rowPlus2 = True
	if(y + 2 > len(board[0])):
		colPlus2 = True
	if(y + 1 > len(board[0])):
		colPlus1 = True
	#Goes through each location 2 tiles away and sets
	#it's var to waht is at the board at that point
	# x - 2 and y - 2
	if(rowMinus2 and colMinus2):
		atLocation = board[y - 2][x - 2]
	# x - 2 and y - 1
	if(rowMinus2 and colMinus1):
		atLocation = board[y - 2][x - 1]
	# x - 2 and y
	if(rowMinus2):
		atLocation = board[y - 2][x]
	# x - 2 and y + 1
	if(rowMinus2 and colPlus1):
		atLocation = board[y - 2][x + 1]
	# x - 2 and y + 2
	if(rowMinus2 and colPlus2):
		atLocation = board[y - 2][x + 2]		 
	# x - 1 and y - 2
	if(rowMinus1 and colMinus2):
		atLocation = board[y - 1][x - 2]
	# x - 1 and y - 1
	if(rowMinus1 and colMinus1):
		atLocation = board[y - 1][x - 1]
	# x - 1 and y
	if(rowMinus1):
		atLocation = board[y - 1][x]
	# x - 1 and y + 1
	if(rowMinus1 and colPlus1):
		atLocation = board[y - 1][x + 1]
	# x - 1 and y + 2
	if(rowMinus1 and colPlus2):
		atLocation = board[y - 1][x + 2]
	# x and y - 2
	if(colMinus2):
		atLocation = board[y][x - 2]
	# x and y - 1
	if(colMinus1):
		atLocation = board[y][x - 1]
	# x and y + 1
	if(colPlus1):
		atLocation = board[y][x + 1]
	# x and y + 2
	if(colPlus2):
		atLocation = board[y][x + 2]
	# x + 1 and y - 2
	if(rowPlus1 and colMinus2):
		atLocation = board[y + 1][x - 2]
	# x + 1 and y - 1
	if(rowPlus1 and colMinus1):
		atLocation = board[y + 1][x - 1]
	# x + 1 and y
	if(rowPlus1):
		atLocation = board[y + 1][x]
	# x + 1 and y + 1
	if(rowPlus1 and colPlus1):
		atLocation = board[y + 1][x + 1]
	# x + 1 and y + 2
	if(rowPlus1 and colPlus2):
		atLocation = board[y + 1][x + 2]
	# x + 2 and y - 2
	if(rowPlus2 and colMinus2):
		atLocation = board[y + 2][x - 2]
	# x + 2 and y - 1
	if(rowPlus2 and colMinus1):
		atLocation = board[y + 2][x - 1]
	# x + 2 and y
	if(rowPlus2):
		atLocation = board[y + 2][x]
	# x + 2 and y + 1
	if(rowPlus2 and colPlus1):
		atLocation = board[y + 2][x + 1]
	# x + 2 and y + 2
	if(rowPlus2 and colPlus2):
		atLocation = board[y + 2][x + 2]

#check if obstacles are to the left of point. Returns True
#if something is to the left, and False if something isn't to the left.
def check_left(x, y, board):
	return is_obstacle(x-1, y, board)

#check if obstacles are to the right of point
def check_right(x, y, board):
	return is_obstacle(x+1, y, board)

#check if obstacles are above point
def check_up(x, y, board):
	return is_obstacle(x, y-1, board)

#check if obstacles are below point
def check_down(x, y, board):
	return is_obstacle(x, y+1, board)

#check if obstacle is above and to the left of point
def check_upleft(x, y, board):
	return is_obstacle(x-1, y-1, board)

#check if obstacle is below and to the left of point
def check_downleft(x, y, board):
	return is_obstacle(x-1, y+1, board)

#check if obstacle is above and to the right of point
def check_upright(x, y, board):
	return is_obstacle(x+1, y-1, board)

#check if obstacle is below and to the right of point
def check_downright(x, y, board):
	return is_obstacle(x+1, y+1, board)

#calculates distance between point 1 and point 2
def calc_distance(x1, y1, x2, y2):
	horizontal_distance = x1 - x2
	vertical_distance = y1 - y2
	total_distance = abs(horizontal_distance) + abs(vertical_distance)
	return total_distance

#returns the shortest path from point A to point B in a_star. Returns a list containing a list and the length of the path.
#The path list begins with the starting node and ends in the goal node.
def reconstruct_path(parent, current):
	total_path = [current]
	while current in parent.keys():
		current = parent[current]
		total_path.append(current)
	return [list(reversed(total_path)), len(total_path)]

#use this method to find a path from point A to point B. Returns None if there is no path.
def a_star(start, goal, board):
	#start and goal should be (x,y) objects
	#to call this function: a_star((x0, y0), (x1, y1), board)
	start = tuple(start)
	goal = tuple(goal)
	x0, y0 = start[0], start[1]
	x1, y1 = goal[0], goal[1]

	closed_set = []
	open_set   = [start]
	parent = {} #empty map

	#g_score should be distance from starting point to another point (ex: a neighbour).
	g_score = [[10000 for x in xrange(len(board[y]))] for y in xrange(len(board))]
	#Obviously, the G score from the starting point to itself is 0.
	g_score[y0, x0] = 0

	f_score = [[10000 for x in xrange(len(board[y]))] for y in xrange(len(board))]
	f_score[y0, x0] = calc_distance(x0, y0, x1, y1)

	while(len(open_set) > 0):
		current = min(open_set, key=lambda p: f_score[p[1]][p[0]])

		if (current == goal):
			return reconstruct_path(parent, goal)

		open_set.remove(current)
		closed_set.append(current)

		neighbours = []
		if (check_up(x0, y0, board) == False):
			neighbours.append((x0, y0-1))
		if (check_right(x0, y0, board) == False):
			neighbours.append((x0+1, y0))
		if (check_down(x0, y0, board) == False):
			neighbours.append((x0, y0+1))
		if (check_left(x0, y0, board) == False):
			neighbours.append((x0-1, y0))

		for neighbour in neighbours:
			if neighbour in closed_set:
				continue
			tentative_g_score = g_score[current[1]][current[0]] + calc_distance(current[0], current[1] ,neighbour[0], neighbour[1])
			if neighbour not in open_set:
				open_set.append(neighbour)
			elif tentative_g_score >= g_score[neighbour[1]][neighbour[0]]:
				continue

			parent[neighbour] = current
			g_score[neighbour[1]][neighbour[0]] = tentative_g_score
			f_score[neighbour[1]][neighbour[0]] = tentative_g_score + calc_distance(neighbour[0], neighbour[1], x1, y1)
	return None

def norm_dir(cX, cY, pX, pY):
	dX = int(math.copysign(1, cX - pX))
	dY = int(math.copysign(1, cY - pY))
	if cX-pX == 0:
		dX = 0
	if cY-pY == 0:
		dY = 0
	return (dX, dY)

def find_neighbours(cX, cY, parent, board):
	#parent should be an (x, y) object
	neighbours = [] # a list of tuples aka (x, y) object
	
	if type(parent) != tuple:
		for i,j in [(-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
			if (not is_obstacle(cX+i, cY+j, board)):
				neighbours.append((cX+i, cY+j))
		return neighbours
	dX,dY = norm_dir(cX,cY,parent[0],parent[1])

	#Check if moved diagonally from parent
	if (dX != 0 and dY != 0):
		if (not is_obstacle(cX, cY+dY, board)):
			neighbours.append((cX, cY+dY))
		if (not is_obstacle(cX+dX, cY, board)):
			neighbours.append((cX+dX, cY))
		if ((not is_obstacle(cX, cY+dY, board) or not is_obstacle(cX+dX, cY, board)) and not is_obstacle(cX+dX, cY+dY, board)):
			neighbours.append((cX+dX, cY+dY))
		if (is_obstacle(cX-dX, cY, board) and not is_obstacle(cX, cY+dY, board)):
			neighbours.append((cX-dX, cY+dY))
		if (is_obstacle(cX, cY-dY, board) and not is_obstacle(cX+dX, cY, board)):
			neighbours.append((cX+dX, cY-dY))

	if (dX == 0 and dY != 0):
		if not is_obstacle(cX+dX, cY, board):
			if not is_obstacle(cX, cY+dY, board):
				neighbours.append((cX, cY+dY))
			if check_right(cX, cY, board):
				neighbours.append((cX+1, cY+dY))
			if check_left(cX, cY, board):
				neighbours.append((cX+dX, cY-1))

	if (dX != 0 and dY == 0):
		if not is_obstacle(cX+dX, cY, board):
			if not is_obstacle(cX+dX, cY, board):
				neighbours.append((cX+dX, cY))
			if check_down(cX, cY, board):
				neighbours.append((cX+dX,cY+1))
			if check_up(cX, cY, board):
				neighbours.append((cX+dX,cY-1))
	return neighbours


def jump(cX, cY, dX, dY, goal, board):
	#goal should be an (x, y) object
	#cX, cY = current point coords
	#dX, dY = direction vectors
	nextX = cX + dX
	nextY = cY + dY
	nextX2 = nextX + dX
	nextY2 = nextY + dY
	#check if next point is obstacle or out of bounds
	if (is_obstacle(nextX, nextY, board)):
		return None 

	#check if next point is the goal when moving diagonally
	if (dX != 0 and dY != 0):
		if (nextX == goal[0] and nextY == goal[1]):
			if (is_obstacle(nextX, cY, board) == False or is_obstacle(cX, nextY, board) == False):
				return (nextX, nextY)
	#else if the next point is the goal when moving orthogonally
	elif (nextX == goal[0] and nextY == goal[1]):
		return (nextX, nextY)

	#check if direction is diagonal
	if (dX != 0 and dY != 0):
		#check if goal is adjacent to next
		if ((nextX+dX, nextY) == goal or (nextX, nextY+dY) == goal):
			return (nextX, nextY)
		if ((not is_obstacle(nextX-dX, nextY+dY, board) and is_obstacle(nextX-dX, nextY, board)) or (not is_obstacle(nextX+dX, nextY-dY, board) and is_obstacle(nextX, nextY-dY, board))):
			return (nextX, nextY)
		if (jump(nextX, nextY, dX, 0, goal, board) != None or jump(nextX, nextY, 0, dY, goal, board) != None):
			return (nextX, nextY)
		if (is_obstacle(nextX2, nextY2, board)):
			return None
		if (is_obstacle(nextX2+dX, nextY2, board) and is_obstacle(nextX2, nextY2+dY, board)):
			return None
		if (nextX2, nextY2) == goal:
			return (nextX2, nextY2)

	#check if direction is horizontal
	if (dX != 0 and dY == 0):
		#check if goal is above or below the next point. If it is, return next point as a jump point.
		if ((nextX, nextY-1) == goal or (nextX, nextY-1) == goal):
			return (nextX, nextY)
		if check_up(nextX, nextY, board) and not check_up(nextX+dX, nextY, board):
			return (nextX, nextY)
		if check_down(nextX, nextY, board) and not check_down(nextX+dX, nextY, board):
			return (nextX, nextY)
		if (is_obstacle(nextX2, nextY, board)):
			return None
		if ((nextX2, nextY) == goal):
			return (nextX2, nextY)

	#check if direction is vertical
	if (dX == 0 and dY != 0):
		#check if goal is to the left or right of the next point. If it is, return next point as a jump point.
		if ((nextX-1, nextY) == goal or (nextX+1, nextY) == goal):
			return (nextX, nextY)
		if check_left(nextX, nextY, board) and not check_left(nextX, nextY+dY, board):
			return (nextX, nextY)
		if check_right(nextX, nextY, board) and not check_right(nextX, nextY+dY, board):
			return (nextX, nextY)
		if (is_obstacle(nextX, nextY2, board)):
			return None
		if ((nextX, nextY2) == goal):
			return (nextX, nextY2)
	
	return jump(nextX, nextY, dX, dY, goal, board)

#finds successors for jump point search.
def find_successors(cX, cY, parent, goal, board):
	successors = []
	#find non-obstacle neighbours
	print "current: (%i, %i)" % (cX, cY)
	print "parent: "
	print parent.get((cX, cY), 0)
	neighbours = find_neighbours(cX, cY, parent.get((cX, cY), 0), board)
	print "neighbours: "
	print neighbours

	for neighbour in neighbours:
		dX = neighbour[0] - cX
		dY = neighbour[1] - cY
		
		print "direction: (%i, %i)" % (dX, dY)

		jumpPoint = jump(cX, cY, dX, dY, goal, board)
		if jumpPoint:
			successors.append(jumpPoint)
			print "jumpPoint"
			print jumpPoint
	return successors #should return a list of (x, y) objects


#jump point search algorithm. Rather than examining every neighbour, find jump points
#to cut down on path symmetry and significantly speed up the process of path searching.
#Returns None if no path found.
def jps(start, goal, board):
	#start and goal should be (x,y) objects
	#to call this function: a_star((x0, y0), (x1, y1), board)
	start = tuple(start)
	goal = tuple(goal)
	x0, y0 = start[0], start[1]
	x1, y1 = goal[0], goal[1]

	if (is_obstacle(x0, y0, board) or is_obstacle(x1, y1, board)):
		return None

	closed_set = set()
	parent = {} #empty map
	gscore = {start:0}
	fscore = {start:calc_distance(x0, y0, x1, y1)}
	pqueue = []

	heapq.heappush(pqueue, (fscore[start], start))
	while(pqueue):
		current = tuple(heapq.heappop(pqueue)[1])
		simple_grid[current[1]][current[0]] = 3
		print "updated simple grid"
		print_grid()
		
		if (current == goal):
			return reconstruct_path(parent, goal)

		closed_set.add(current)
		successors = find_successors(current[0], current[1], parent, goal, board)
		
		for successor in successors:
			jumpPoint = successor

			if jumpPoint in closed_set:
				continue
			tentative_gscore = gscore[current] + calc_distance(current[0], current[1], jumpPoint[0], jumpPoint[1])
			print "tentative_gscore: %i" % tentative_gscore
			if (tentative_gscore < gscore.get(jumpPoint, 0) or jumpPoint not in [j[1] for j in pqueue]):
				parent[jumpPoint] = current
				gscore[jumpPoint] = tentative_gscore
				fscore[jumpPoint] = tentative_gscore + calc_distance(jumpPoint[0], jumpPoint[1], goal[0], goal[1])
				heapq.heappush(pqueue, (fscore[jumpPoint], jumpPoint))

	return None

def print_grid():
	for row in simple_grid:
		for e in row:
			print e,
		print
"""
food_spawn= {'data': 
			[
				{
				'object': 'point',
				'x': 0,
				'y': 9

				}
			],	
			'object': 'list'
			}
snake_spawn= {
	"data": [
	  {
		"body": {
		  "data": [
			{
			  "object": "point",
			  "x": 1,
			  "y": 8
			},
			{
			  "object": "point",
			  "x": 1,
			  "y": 9
			},
			{
			  "object": "point",
			  "x": 1,
			  "y": 10
			}
		  ],
		  "object": "list"
		},
		"health": 100,
		"id": "58a0142f-4cd7-4d35-9b17-815ec8ff8e70",
		"length": 3,
		"name": "Sonic Snake",
		"object": "snake",
		"taunt": "Gotta go fast"
	  },
	  {
		"body": {
		  "data": [
			{
			  "object": "point",
			  "x": 6,
			  "y": 15
			},
			{
			  "object": "point",
			  "x": 7,
			  "y": 15
			},
			{
			  "object": "point",
			  "x": 8,
			  "y": 15
			}
		  ],
		  "object": "list"
		},
		"health": 100,
		"id": "48ca23a2-dde8-4d0f-b03a-61cc9780427e",
		"length": 3,
		"name": "Typescript Snake",
		"object": "snake",
		"taunt": ""
	  }
	],
	"object": "list"
  }
grid = init_board(food_spawn, snake_spawn, 20, 20)

simple_grid = np.zeros((20, 20), dtype=int)
for h in range(0, 20):
	for w in range(0, 20):
		if grid[h][w] == 'food':
			simple_grid[h][w] = 2
		if (grid[h][w] != 'food' and grid[h][w] != 0):
			simple_grid[h][w] = 1

simple_grid[9][19] = 3

#print_grid()
print 

print jps((19, 9), (0, 9), grid)
"""