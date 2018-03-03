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
	#check for wall
	if (x == 0):
		return True
	#check for snakes
	return is_obstacle(x-1, y, board)

#check if obstacles are to the right of point
def check_right(x, y, board):
	#check for wall
	if (x == len(board[0])-1):
		return True
	#check for snakes
	return is_obstacle(x+1, y, board)

#check if obstacles are above point
def check_up(x, y, board):
	#check for wall
	if (y == 0):
		return True
	#check for snakes
	return is_obstacle(x, y-1, board)

#check if obstacles are below point
def check_down(x, y, board):
	#check for wall
	if (y == len(board)-1):
		return True
	#check for snakes
	return is_obstacle(x, y+1, board)

#check if obstacle is above and to the left of point
def check_upleft(x, y, board):
	if (x == 0 or y == 0):
		return True
	return is_obstacle(x-1, y-1, board)

#check if obstacle is below and to the left of point
def check_downleft(x, y, board):
	if (x == 0 or y == len(board)-1):
		return True
	return is_obstacle(x-1, y+1, board)

#check if obstacle is above and to the right of point
def check_upright(x, y, board):
	if (x == len(board[0])-1 or y == 0):
		return True
	return is_obstacle(x+1, y-1, board)

#check if obstacle is below and to the right of point
def check_downright(x, y, board):
	if (x == len(board[0])-1 or y == len(board)-1):
		return True
	return is_obstacle(x+1, y+1, board)

#calculates distance between point 1 and point 2
def calc_distance(x1, y1, x2, y2):
	horizontal_distance = x1 - x2
	vertical_distance = y1 - y2
	total_distance = abs(horizontal_distance) + abs(vertical_distance)
	return total_distance

#returns the shortest path from point A to point B in a_star. Returns a list containing a list and the length of the path.
def reconstruct_path(parent, current):
    total_path = [current]
    while current in parent.keys():
        current = parent[current]
        total_path.append(current)
    return [list(reversed(total_path)), len(total_path)]

#use this method to find a path from point A to point B
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

	g_score = [[10000 for x in xrange(len(board[y]))] for y in xrange(len(board))]
	g_score[start[0]][start[1]] = 0

	f_score = [[10000 for x in xrange(len(board[y]))] for y in xrange(len(board))]
	f_score[start[0]][start[1]] = calc_distance(x0, y0, x1, y1)

	while(len(open_set) > 0):
		current = min(open_set, key=lambda p: f_score[p[0]][p[1]])

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
			tentative_g_score = g_score[current[0]][current[1]] + calc_distance(current[0], current[1] ,neighbour[0], neighbour[1])
			if neighbour not in open_set:
				open_set.append(neighbour)
			elif tentative_g_score >= g_score[neighbour[0]][neighbour[1]]:
				continue

			parent[neighbour] = current
			g_score[neighbour[0]][neighbour[1]] = tentative_g_score
			f_score[neighbour[0]][neighbour[1]] = tentative_g_score + calc_distance(neighbour[0], neighbour[1], x1, y1)
	return 0
"""
def search_hor(self, start, end, hor_dir, dist, board, HORVERT_COST):
	
	Search in horizontal direction, return the newly added open nodes

	@param start: Start position of the horizontal scan.
	@param end: Destination.
	@param hor_dir: Horizontal direction (+1 or -1).
	@param dist: Distance traveled so far.
	@param board: the board
	@param HORVERT_COST: total cost of horizontal and vertical movement
	@return: New jump point nodes (which need a parent).
	
	x0, y0 = start['x'], start['y']
	while True:
		x1 = x0 + hor_dir
		#check if there is an obstacle in the direction.
		if (hor_dir < 0):
			if (check_left(x0, y0, board)):
				return [] # Off-map or obstacle, done.

		if (hor_dir > 0):
			if (check_right(x0, y0, board)):
				return [] # Off-map or obstacle, done.

		if (x1, y0) == (end['x'], end['y']):
			return [self.add_node(x1, y0, None, dist + HORVERT_COST)]

		# Open space at (x1, y0).
		dist = dist + HORVERT_COST
		x2 = x1 + hor_dir

		nodes = []
		if self.obstacle(x1, y0 - 1) and not self.obstacle(x2, y0 - 1):
			nodes.append(self.add_node(x1, y0, (hor_dir, -1), dist))

		if self.obstacle(x1, y0 + 1) and not self.obstacle(x2, y0 + 1):
			nodes.append(self.add_node(x1, y0, (hor_dir, 1), dist))

		if len(nodes) > 0:
			nodes.append(self.add_node(x1, y0, (hor_dir, 0), dist))
			return nodes

		# Process next tile.
		x0 = x1
"""


#returns False if nothing is in between the shortest path from point 1 to point 2.
#returns True if cuts off the shortest path from point 1 to point 2.
#Check between is obsolete. We a_star now.
def check_between(board, x1, y1, x2, y2):
	#first, find the bounds of the shortest path from point 1 to point 2.
	lower_x = x1
	higher_x = x2
	lower_y = y2
	higher_y = y1
	if (x1 > x2):
		lower_x = x2
		higher_x = x1
	if (y1 > y2):
		lower_y = y1
		higher_y = y2

	#first case: if, shortest path from point 1 to point 2 is a horizontal line,
	#check if there is something in that line.
	if (y1 == y2):
		return all(
			is_obstacle(x, y1, board) == True
			for x in range(lower_x+1, higher_x)
		)

	#second case: if, shortest path from point 1 to point 2 is a vertical line,
	#check if there is something in that line.
	if (x1 == x2):
		return all(
			is_obstacle(x1, y, board) == True
			for y in range(higher_y+1, lower_y)
		)

	slope = find_slope(x1, y1, x2, y2)
	#third case: the points are connectable by a negative slope (top left to bottom right)
	
	if (slope < 0):
		#look for a cut-off path starting from the top. In this case, a cut-off path is made if it reaches the bottom or left.
		for x in range(lower_x+1, higher_x+1):
			if (is_obstacle(x, higher_y, board)):
				stack, path = [[x, higher_y]], []
				while stack:
					point = stack.pop()
					if point in path:
						continue
					if (point[0] == lower_x or point[1] ==lower_y):
						return True
					path.append(point)
					#don't add the top left point
					if (check_left(point[0], point[1], board) and (point[0] != lower_x+1 and point[1] != higher_y)):
						stack.append([point[0]-1, point[1]])
					if (check_downleft(point[0], point[1], board)):
						stack.append([point[0]-1, point[1]+1])
					#don't add the bottom right point
					if (check_down(point[0], point[1], board) and (point[0] != higher_x and point[1]+1 != lower_y)):
						stack.append([point[0], point[1]+1])
					#don't add the bottom right point and stay within bounds
					if (check_downright(point[0], point[1], board) and (point[0]+1 != higher_x and point[1]+1 != lower_y) and point[0]+1 <= higher_x): 
						stack.append([point[0]+1, point[1]+1])
					#don't add the bottom right point and stay within bounds
					if (check_right(point[0], point[1], board) and (point[0]+1 != higher_x and point[1] != lower_y) and point[0]+1 <= higher_x):
						stack.append([point[0]+1, point[1]])
		#look for a cut-off path starting from the left. In this case, a cut-off path is made if it reaches the top or right.
		for y in range(higher_y+1, lower_y+1):
			if (is_obstacle(lower_x, y, board)):
				stack, path = [[lower_x, y]], []
				while stack:
					point = stack.pop()
					if point in path:
						continue
					if (point[0] == higher_x or point[1] == higher_y):
						return True
					path.append(point)
					#don't add the top left point
					if (check_up(point[0], point[1], board) and (point[0] != lower_x and point[1]-1 != higher_y)):
						stack.append([point[0], point[1]-1])
					if (check_upright(point[0], point[1], board)):
						stack.append([point[0]+1, point[1]-1])
					#don't add the bottom right point
					if (check_right(point[0], point[1], board) and (point[0]+1 != higher_x and point[1] != lower_y)):
						stack.append([point[0]+1, point[1]])
					#don't add the bottom right point and stay within bounds
					if (check_downright(point[0], point[1], board) and (point[0]+1 != higher_x and point[1]+1 != lower_y) and point[1]+1 <= lower_y):
						stack.append([point[0]+1, point[1]+1])
					#don't add the bottom right point and stay within bounds
					if (check_down(point[0], point[1], board) and (point[0] != higher_x and point[1]+1 != lower_y) and point[1]+1 <= lower_y):
						stack.append([point[0], point[1]+1])

	#fourth case: the points are connectable by a positive slope (bottom left to top right)
	if (slope > 0):
		#look for a cut-off path starting from the top. In this case, a cut-off path is made it reaches the right or bottom.
		for x in range(lower_x, higher_x):
			if (is_obstacle(x, higher_y, board)):
				stack, path = [[x, higher_y]], []
				while stack:
					point = stack.pop()
					if point in path:
						continue
					if (point[0] == higher_x or point[1] ==lower_y):
						return True
					path.append(point)
					#don't add the bottom left point and stay within bounds
					if (check_downleft(point[0], point[1], board) and (point[0]-1 != lower_x and point[1]+1 != lower_y) and point[0]-1 >= lower_x):
						stack.append([point[0]-1, point[1]+1])
					#don't add the bottom left point
					if (check_down(point[0], point[1], board) and (point[0] != lower_x and point[1]+1 != lower_y)):
						stack.append([point[0], point[1]+1])
					if (check_downright(point[0], point[1], board)): 
						stack.append([point[0]+1, point[1]+1])
		#look for a cut-off path starting from the left. In this case, a cut-off path is made it reaches the right or bottom.
		for y in range(higher_y, lower_y):
			if (is_obstacle(lower_x, y, board)):
				stack, path = [[lower_x, y]], []
				while stack:
					point = stack.pop()
					if point in path:
						continue
					if (point[0] == higher_x or point[1] == lower_y):
						return True
					path.append(point)
					#don't add the upper right point and stay within bounds
					if (check_upright(point[0], point[1], board) and (point[0]+1 != higher_x and point[1]-1 != higher_y) and point[1]-1 <= lower_y):
						stack.append([point[0]+1, point[1]-1])
					#don't add the upper right point
					if (check_right(point[0], point[1], board) and (point[0]+1 != higher_x and point[1] != higher_y)):
						stack.append([point[0]+1, point[1]])
					if (check_downright(point[0], point[1], board)):
						stack.append([point[0]+1, point[1]+1])
	
	return False #return False if no cut-off path is found.
