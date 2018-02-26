def init_board(food_list, snake_list, width, height):
	board = [ ([0] * height) for row in xrange(width)]
	for food in food_list['data']:
		x = food['x']
		y = food['y']
		board[y][x] = 'food'
	for snake_body in snake_list['data']:
		for point in snake_body['body']['data']:
			x = point['x']
			y = point['y']
			board[y][x] = 'snake'
	return board

def check_left(head, board):
	#check for wall
	if (head['x'] == 0):
		return True
	#check for snakes
	if (board[head['y']][head['x']-1] == 'snake'):
		return True
	return False

def check_right(head, board, board_width):
	#check for wall
	if (head['x'] == board_width-1):
		return True
	#check for snakes
	if (board[head['y']][head['x']+1] == 'snake'):
		return True
	return False

def check_up(head, board):
	#check for wall
	if (head['y'] == 0):
		return True
	#check for snakes
	if (board[head['y']-1][head['x']] == 'snake'):
		return True
	return False

def check_down(head, board, board_height):
	#check for wall
	if (head['y'] == board_height-1):
		return True
	#check for snakes
	if (board[head['y']+1][head['x']] == 'snake'):
		return True
	return False