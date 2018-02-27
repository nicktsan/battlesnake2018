#create a board and fill it with food, snakes, and our snake
def init_board(food_list, snake_list, width, height):
	#initialize a 2d list of 0's with width rows and height columns
	board = [([0] * width) for row in xrange(height)]
	#fill in food locations
	for food in food_list['data']:
		x = food['x']
		y = food['y']
		board[y][x] = 'food'
	#fill in snake body locations with their id
	for snake in snake_list['data']: #snake contains all info within a snake's 'data'
		for point in snake['body']['data']:
			x = point['x']
			y = point['y']
			board[y][x] = snake['id']
	return board

#to refer an x,y point on the board, type it as board[y][x]
def is_obstacle(board, x, y):
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

#check if obstacles are to the left of our snake. Returns True
#if something is to the left, and False if something isn't to the left.
def check_left(head, board):
	#check for wall
	if (head['x'] == 0):
		return True
	#check for snakes
	return is_obstacle(board, head['x']-1, head['y'])

#check if obstacles are to the right of our snake
def check_right(head, board, board_width):
	#check for wall
	if (head['x'] == board_width-1):
		return True
	#check for snakes
	return is_obstacle(board, head['x']+1, head['y'])

#check if obstacles are above our snake
def check_up(head, board):
	#check for wall
	if (head['y'] == 0):
		return True
	#check for snakes
	return is_obstacle(board, head['x'], head['y']-1)

#check if obstacles are below our snake
def check_down(head, board, board_height):
	#check for wall
	if (head['y'] == board_height-1):
		return True
	#check for snakes
	return is_obstacle(board, head['x'], head['y']+1)

#check if obstacle is above and to the left of snake head
"""
def check_upleft(head, board):
	if (head['x'] == 0):
		return True
	return check_up()

#calculates distance between point 1 and point 2
def calc_distance(x1, y1, x2, y2):
	horizontal_distance = x1 - x2
	vertical_distance = y1 - y2
	total_distance = abs(horizontal_distance) + abs(vertical_distance)
	return total_distance

#returns False if nothing is in between the shortest path from point 1 to point 2.
#returns True if something is in between the shortest path from point 1 to point 2.
def is_between(board, x1, y1, x2, y2):
	#first, find the bounds of the shortest path from point 1 to point 2.
	lower_x = x1
	higher_x = x2
	lower_y = y1
	higher_y = y2
	if (x1 > x2):
		lower_x = x2
		higher_x = x1
	if (y1 > y2):
		lower_y = y2
		higher_y = y1
	#first case: if, shortest path from point 1 to point 2 is a horizontal line,
	#check if there is something in that line.
	if (y1 == y2):
		return all(
			is_obstacle(board, x, y1) == True
			for x in range(lower_x+1, higher_x)
		)
	#second case: if, shortest path from point 1 to point 2 is a vertical line,
	#check if there is something in that line.
	if (x1 == x2):
		return all(
			is_obstacle(board, x1, y) == True
			for y in range(lower_y+1, higher_y)
		)
	slope = find_slope(x1, y1, x2, y2)
	#third case: the points are connectable by a negative slope (top left to bottom right)


	#fourth case: the points are connectable by a positive slope (bottom left to top right)


	return False
"""