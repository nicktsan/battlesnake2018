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
	return (float(rise)/float(run))*-1.0 #we need to multiply by -1 because y values become larger when you go down the grid.
	#returns a positive or negative float, which will be our slope.

#returns true if the position is a snake head that is 
#connected to a smaller body than ours
def checkIfSnakeHead(boardLocation):
	if(isinstance(boardLocation, list):
		if(boardLocation[1] == 0):
			snakelength = 0
			for snake in snake_list['data']:
				if(snake['id'] == boardLocation[0]):
					snakelength = snake['length']
			if(mysnake[length] > snakelength):
				return True
			#else
			return False

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
	#it's var to what is at the board at that point
	# x - 2 and y
	if(rowMinus2):
		atLocation = board[y - 2][x]
	# x - 1 and y - 1
	if(rowMinus1 and colMinus1):
		atLocation = board[y - 1][x - 1]
	# x - 1 and y
	if(rowMinus1):
		atLocation = board[y - 1][x]
		if(checkIfSnakeHead(atLocation):
			#this is a good move
	# x - 1 and y + 1
	if(rowMinus1 and colPlus1):
		atLocation = board[y - 1][x + 1]
	# x and y - 2
	if(colMinus2):
		atLocation = board[y][x - 2]
	# x and y - 1
	if(colMinus1):
		atLocation = board[y][x - 1]
		if(checkIfSnakeHead(atLocation):
			#this is a good move
	# x and y + 1
	if(colPlus1):
		atLocation = board[y][x + 1]
		if(checkIfSnakeHead(atLocation):
			#this is a good move
	# x and y + 2
	if(colPlus2):
		atLocation = board[y][x + 2]
	# x + 1 and y - 1
	if(rowPlus1 and colMinus1):
		atLocation = board[y + 1][x - 1]
	# x + 1 and y
	if(rowPlus1):
		atLocation = board[y + 1][x]
		if(checkIfSnakeHead(atLocation):
			#this is a good move
	# x + 1 and y + 1
	if(rowPlus1 and colPlus1):
		atLocation = board[y + 1][x + 1]
	# x + 2 and y
	if(rowPlus2):
		atLocation = board[y + 2][x]

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

#returns False if nothing is in between the shortest path from point 1 to point 2.
#returns True if something is in between the shortest path from point 1 to point 2.
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
		#look for a cut-off path starting from the top. In this case, a cut-off path is made if it reaches the bottom or right.
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
					if (check_downleft(point[0], point[1], board)):
						stack.append([point[0]-1, point[1]+1])
					#don't add the bottom right point
					if (check_down(point[0], point[1], board) and (point[0] != higher_x and point[1]+1 != lower_y)):
						stack.append([point[0], point[1]+1])
					#don't add the bottom right point and stay within bounds
					if (check_downright(point[0], point[1], board) and (point[0]+1 != higher_x and point[1]+1 != lower_y) and point[0]+1 <= higher_x): 
						stack.append([point[0]+1, point[1]+1])
		#look for a cut-off path starting from the left. In this case, a cut-off path is made if it reaches the bottom or right.
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
					if (check_upright(point[0], point[1], board)):
						stack.append([point[0]+1, point[1]-1])
					#don't add the bottom right point
					if (check_right(point[0], point[1], board) and (point[0]+1 != higher_x and point[1] != lower_y)):
						stack.append([point[0]+1, point[1]])
					#don't add the bottom right point and stay within bounds
					if (check_downright(point[0], point[1], board) and (point[0]+1 != higher_x and point[1]+1 != lower_y) and point[1]+1 <= lower_y):
						stack.append([point[0]+1, point[1]+1])

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
