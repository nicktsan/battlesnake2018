import heapq
import numpy as np
import math
#create a board and fill it with food, snakes, and our snake
def init_board(food_list, snake_list, width, height, myhead):
	#initialize a 2d list of 0's with width number of columns and height number of rows.
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

	#check for dead-ends, starting with our head. Dead ends are any space
	#with three orthogonal obstacles.
	"""
	free = []
	visited = []
	for i,j in [(-1,0),(0,-1),(1,0),(0,1)]:
		#start with our snake head
		if (not is_obstacle(myhead['x']+i, myhead['y']+j, board)):
			free.append((myhead['x']+i, myhead['y']+j))
	while len(free) == 1:
		cX, cY = free[0][0], free[0][1]
		visited.append([cX, cY])
		del free[:]
		for i,j in [(-1,0),(0,-1),(1,0),(0,1)]:
			if (not is_obstacle(cX+i, cY+j, board)):
				free.append((cX+i, cY+j))
	for x in range(0, width):
		for y in range(0, height):
			del free[:]
			if (not is_obstacle(x, y, board) and [x, y] not in visited):
				for i,j in [(-1,0),(0,-1),(1,0),(0,1)]:
					if (not is_obstacle(x+i, y+j, board)):
						free.append((x+i, y+j))
				visited.append([x, y])
				if len(free) == 1:
					board[y][x] = 'dead end'
				while len(free) == 1:
					cX, cY = free[0][0], free[0][1]
					visited.append([x, y])
					board[cY][cX] = 'dead end'
					del free[:]
					for i,j in [(-1,0),(0,-1),(1,0),(0,1)]:
						if (not is_obstacle(cX+i, cY+j, board)):
							free.append((cX+i, cY+j))
	"""
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

#calculates the vector between start and end points
def calc_vec(startX, startY, endX, endY):
	return (endX-startX, endY-startY)

#calculates distance between point 1 and point 2
def calc_distance(x1, y1, x2, y2):
	horizontal_distance = x1 - x2
	vertical_distance = y1 - y2
	total_distance = abs(horizontal_distance) + abs(vertical_distance)
	return total_distance

#returns true if the position is a snake head
def checkIfSnakeHead(boardLocation):
	if isinstance(boardLocation, list):
		if (boardLocation[1] == 0):
			return True
	return False

def ifSnakeisBiggerAtLocation(boardLocation, mylength, snake_list):
	#boardLocation is what is in board[y][x]
	for snake in snake_list['data']:
		if(snake['id'] == boardLocation[0]):
			snakelength = snake['length']
			break
	#if your snake is larger, return true. Otherwise, return false.
	if(mylength > snakelength):
		return True
	return False

#Takes in the board and our snakes head location
#Goes through each tile location 2 tiles away and checks
#what is in it.
#Throw in other fucntions depending on what is present
def checkOneTileAway(board, x, y, mylength, snake_list):
	#checks for if the locations 2 tiles away are out of the board
	#records how many obstacles there is in our next move
	numberObstacles = 0
	#Goes through each location 2 tiles away and sets
	#it's var to what is at the board at that point
	# x-1 and y
	if(x - 1 >= 0):
		atLocation = board[y][x - 1]
		if checkIfSnakeHead(atLocation):
			if(ifSnakeisBiggerAtLocation(atLocation, mylength, snake_list) == False):
				numberObstacles += 1
		elif (is_obstacle(x-1, y, board)):
				numberObstacles = numberObstacles + 1
	#x and y - 1
	if(y - 1 >= 0):
		atLocation = board[y-1][x]
		if checkIfSnakeHead(atLocation):
			if(ifSnakeisBiggerAtLocation(atLocation, mylength, snake_list) == False):
				numberObstacles += 1
		elif(is_obstacle(x, y - 1, board)):
				numberObstacles = numberObstacles + 1
	# x and y+1
	if(y + 1 < len(board)):
		atLocation = board[y + 1][x]
		if checkIfSnakeHead(atLocation):
			if(ifSnakeisBiggerAtLocation(atLocation, mylength, snake_list) == False):
				numberObstacles += 1
		elif(is_obstacle(x, y + 1, board)):
				numberObstacles = numberObstacles + 1
	# x + 1 and y
	if(x + 1 < len(board[0])):
		atLocation = board[y][x + 1]
		if checkIfSnakeHead(atLocation):
			if(ifSnakeisBiggerAtLocation(atLocation, mylength, snake_list) == False):
				numberObstacles += 1
		elif(is_obstacle(x + 1, y, board)):
				numberObstacles = numberObstacles + 1
	#Check if the next turn is a trap
	return numberObstacles


def seek_food(mysnake_head, food_list, snake_list, mysnake):
	x2 = mysnake_head['x']
	y2 = mysnake_head['y']
	coordinate = []
	
	for food in food_list['data']:    # Find a food
		x1 = food['x']
		y1 = food['y']
		food_ok = True
		distance = calc_distance(x1,y1,x2,y2)
		# get the coordinate of all other snakes
		for other_snake in snake_list['data']:
			if (other_snake['id'] != mysnake['id']): 
				othersnake_head = other_snake['body']['data'][0]
				x3 = othersnake_head['x']
				y3 = othersnake_head['y']
				other_distance = calc_distance(x1,y1,x3,y3)
				if (distance < other_distance):
					continue
				elif (distance > other_distance):
					food_ok = False
				else:
					other_length = other_snake['length']
					our_length = mysnake['length']
					if (other_length >= our_length):
						food_ok = False
					elif (our_length > other_length):
						continue
		
		if (food_ok == True):
			coordinate.append([distance, x1, y1])       #store distancea and coordinatea in list
	
	if not coordinate:
		for other_snake in snake_list['data']:
			if (other_snake['id'] != mysnake['id']):
				othersnake_tail = other_snake['body']['data'][-1]
				x3 = othersnake_tail['x']
				y3 = othersnake_tail['y']
				coordinate.append([distance, x3, y3])
	
	else:
		
		coordinate = sorted(coordinate, key=lambda x:x[0]) #sort all the coordinate base on distance

	return coordinate


#The path list begins with the starting node and ends in the goal node.
def reconstruct_path(parent, current):
	total_path = [current]
	num_turns = 0
	while current in parent.keys():
		prev = current
		current = parent[current]
		#simple_grid[current[1]][current[0]] = 5
		num_turns += calc_distance(prev[0], prev[1], current[0], current[1])
		total_path.append(current)
	#simple_grid[total_path[0][1]][total_path[0][0]] = 5
	
	#print "finished:"
	#print_grid()
	
	return [list(reversed(total_path)), num_turns]

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
		for i,j in [(-1,0),(0,-1),(1,0),(0,1)]:
			if (not is_obstacle(cX+i, cY+j, board)):
				neighbours.append((cX+i, cY+j))
		for i,j in [(-1,-1),(-1,1),(1,-1),(1,1)]:
			if (not is_obstacle(cX+i, cY+j, board) and (not is_obstacle(cX+i, cY, board) or not is_obstacle(cX, cY+j, board))):
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
				neighbours.append((cX-1, cY+dY))

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
	# "dX, dY = %i, %i" % (dX, dY)
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
	
	return jump(nextX, nextY, dX, dY, goal, board)

#finds successors for jump point search.
def find_successors(cX, cY, parent, goal, board):
	successors = []
	#find non-obstacle neighbours
	# "finding successors for current: (%i, %i)" % (cX, cY)
	# "parent: "
	# parent.get((cX, cY), 0)
	neighbours = find_neighbours(cX, cY, parent.get((cX, cY), 0), board)
	#print "neighbours"
	#print neighbours
	for neighbour in neighbours:
		dX = neighbour[0] - cX
		dY = neighbour[1] - cY
		jumpPoint = jump(cX, cY, dX, dY, goal, board)
		

		if jumpPoint:
			#simple_grid[jumpPoint[1]][jumpPoint[0]] = 3
			#print "new grid"
			#print_grid()
			successors.append(jumpPoint)
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
	closed_set = set()
	parent = {} #empty map
	gscore = {start:0}
	fscore = {start:calc_distance(x0, y0, x1, y1)}
	pqueue = []

	heapq.heappush(pqueue, (fscore[start], start))
	while(pqueue):
		current = tuple(heapq.heappop(pqueue)[1])
		#print "current:"
		#print current
		#simple_grid[current[1]][current[0]] = 3
		
		if (current == goal):
			return reconstruct_path(parent, goal)

		closed_set.add(current)
		successors = find_successors(current[0], current[1], parent, goal, board)
		
		for successor in successors:
			jumpPoint = successor

			if jumpPoint in closed_set:
				continue
			tentative_gscore = gscore[current] + calc_distance(current[0], current[1], jumpPoint[0], jumpPoint[1])
			if (tentative_gscore < gscore.get(jumpPoint, 0) or jumpPoint not in [j[1] for j in pqueue]):
				parent[jumpPoint] = current
				gscore[jumpPoint] = tentative_gscore
				fscore[jumpPoint] = tentative_gscore + calc_distance(jumpPoint[0], jumpPoint[1], goal[0], goal[1])
				heapq.heappush(pqueue, (fscore[jumpPoint], jumpPoint))

	return None
"""
def print_grid():
	for row in simple_grid:
		for e in row:
			print e,
		print
		


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
			  "x": 0,
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
			},
						{
			  "object": "point",
			  "x": 2,
			  "y": 10
			}
		  ],
		  "object": "list"
		},
		"health": 100,
		"id": "58a0142f-4cd7-4d35-9b17-815ec8ff8e70",
		"length": 4,
		"name": "Sonic Snake",
		"object": "snake",
		"taunt": "Gotta go fast"
	  },
	  {
		"body": {
		  "data": [
			{
			  "object": "point",
			  "x": 4,
			  "y": 8
			},
			{
			  "object": "point",
			  "x": 3,
			  "y": 8
			},
			{
			  "object": "point",
			  "x": 3,
			  "y": 9
			},
			{
			  "object": "point",
			  "x": 3,
			  "y": 10
			},
						{
			  "object": "point",
			  "x": 3,
			  "y": 11
			}
		  ],
		  "object": "list"
		},
		"health": 100,
		"id": "58a0142f-4cd7-4d35-9b17-815ec8ff8e70",
		"length": 4,
		"name": "Sonic Snake",
		"object": "snake",
		"taunt": "Gotta go fast"
	  },
	  {
		"body": {
		  "data": [
			{
			  "object": "point",
			  "x": 5,
			  "y": 8
			},
			{
			  "object": "point",
			  "x": 5,
			  "y": 9
			},
			{
			  "object": "point",
			  "x": 5,
			  "y": 10
			},
						{
			  "object": "point",
			  "x": 5,
			  "y": 11
			}
		  ],
		  "object": "list"
		},
		"health": 100,
		"id": "58a0142f-4cd7-4d35-9b17-815ec8ff8e70",
		"length": 4,
		"name": "Sonic Snake",
		"object": "snake",
		"taunt": "Gotta go fast"
	  },
	  {
		"body": {
		  "data": [
			{
			  "object": "point",
			  "x": 15,
			  "y": 13
			},
			{
			  "object": "point",
			  "x": 15,
			  "y": 12
			},
			{
			  "object": "point",
			  "x": 15,
			  "y": 11
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
	  },
	],
	"object": "list"
  }
myhead = {'x':15, 'y':13}
grid = init_board(food_spawn, snake_spawn, 20, 20, myhead)

simple_grid = np.zeros((20, 20), dtype=int)
for h in range(0, 20):
	for w in range(0, 20):
		if grid[h][w] == 'food':
			simple_grid[h][w] = 2
		if (grid[h][w] != 'food' and grid[h][w] != 0):
			simple_grid[h][w] = 1
		if grid[h][w] == 'dead end':
			simple_grid[h][w] = 9

begin = (15, 13)
dest = (15, 18)
simple_grid[begin[1]][begin[0]] = 3
simple_grid[dest[1]][dest[0]] = 2
print "starting grid: "
print_grid()

print jps(begin, dest, grid)
"""
