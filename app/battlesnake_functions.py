#create a board and fill it with food, snakes, and our snake
def init_board(food_list, snake_list, width, height):
	#initialize a 2d list of 0's with height rows and width columns
	board = [([0] * height) for row in xrange(width)]
	#fill in food locations
	for food in food_list['data']:
		x = food['x']
		y = food['y']
		board[x][y] = 'food'
	#fill in snake body locations with their id
	for snake in snake_list['data']: #snake contains all info within a snake's 'data'
		for point in snake['body']['data']:
			x = point['x']
			y = point['y']
			board[x][y] = snake['id']
	return board

def is_obstacle(board, x, y):
	if (board[x][y] != 'food' and board[x][y] != 0):
		return True
	return False

#chick if obstacles are to the left of our snake
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

#calculates distance between point 1 and point 2
def calc_distance(x1, y1, x2, y2):
	horizontal_distance = x1 - x2
	vertical_distance = y1 - y2
	total_distance = abs(horizontal_distance) + abs(vertical_distance)
	return total_distance

#returns False if nothing is in between the shortest path from point 1 to point 2.
#returns True if something is in between the shortest path from point 1 to point 2.
"""
def check_between(board, x1, y1, x2, y2):
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

		)
	#second case: if, shortest path from point 1 to point 2 is a vertical line,
	#check if there is something in that line.
	return False
"""