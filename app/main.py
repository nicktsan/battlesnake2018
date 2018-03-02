from battlesnake_functions import *
import bottle
import os
import random
import numpy as np
import tflearn
import math
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean
from collections import Counter

class SnakeNN:
	def __init__(self, initial_games = 10000, test_games = 1000, goal_steps = 2000, lr = 1e-2, filename = 'battlesnake_nn.tflearn'):
		self.initial_games = initial_games
		self.test_games = test_games
		self.goal_steps = goal_steps
		self.lr = lr
		self.filename = filename
		self.vectors_and_keys = [
				[[-1, 0], 0],
				[[0, 1], 1],
				[[1, 0], 2],
				[[0, -1], 3]
		]

@bottle.route('/')
def static():
	return "the server is running hello world"

@bottle.route('/static/<path:path>')
def static(path):
	return bottle.static_file(path, root='static/')

@bottle.post('/start')
def start():
	data = bottle.request.json
	game_id = data.get('game_id')
	board_width = data.get('width')
	board_height = data.get('height')

	head_url = '%s://%s/static/head.png' % (
		bottle.request.urlparts.scheme,
		bottle.request.urlparts.netloc
	)

	# TODO: Do things with data

	return {
		'color': '#ffaa00',
		'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
		'head_url': head_url,
		'name': 'nicksnek',
		'head_type': 'fang',
		'tail_type': 'block-bum'
	}
    # Board Layout of a 6x6 board
    # --------------------------------
    # |(0,0)                    (5,0)|
    # |(0,1)                    (5,1)|
    # |                              |
    # |                              |
    # |                              |
    # |(0,5)                    (5,5)|
    # --------------------------------

	# Strategy:
    # Run in circles in the center of the board until HP runs to the threshold minimum. (Chase own tail)
    # *Calculate the distance from the snake to the food by using the formula (dy2-dy1)/(dx2-dx1)   Dy2,Dx2 is the food and Dy1,Dx1 is the snake head
    # Calculate other snake's distance to the food using the same above formula
    # Find out if a block is in the way in the next tile
    # Go for the food
    # Repeat * again until get the food
    # Return to center of the board


@bottle.post('/move')
def move():
	data = bottle.request.json

	for f in data['food']:
        grid[f[0]][f[1]] = FOOD
        
	game_id = data.get('game_id')
	board_width = data.get('width')
	board_height = data.get('height')
	mysnake = data['you']['body']['data']
	snake_list = data['snakes']
	mysnake_head = mysnake[0] #should get the head's point
	# TODO: Do things with data
	
	above_headx, above_heady = get_up(mysnake_head)
	directions = ['up', 'down', 'left', 'right']
	direction = 'up'
	#direction = random.choice(directions)

	#Find our head location
	x2 = mysnake_head['x'],
	y2 = mysnake_head['y']
	coordinate = []
	for food in food_list['data']:    # Find a food
		x1 = food['x'],
		y1 = food['y']
		# check all obstacles in between (call function)
		distance = calc_distance(x1,y1,x2,y2)   #calculate the distance from food to head
		# get the coordinate of all other snakes
		# call obstacles in between function
		# call calc_distance function

		#compare our distance with their distance
		# if they are closer, abandon the food, find next food and go through the same process 

		# got the food that we are closer than others, store it in list
		coordinate.append([distance, x1, y1])	    #store distancea and coordinatea in list
	coordinate = sorted(coordinate, key=lambda x: x[0])   	#sort all the coordinate base on distance
	for row in coordinate:					#choose row 0 as the closest food
		food_dist = row[0]
		x1 = row[1]
		y1 = row[2]
	
	#figure out which way to turn
	if (x1 > x2):       # if food is on right hand side
		if (y1 > y2):    # if food is down-right
			direction = 'down'
		elif(y1 < y2):   # if food is up-right
			direction = 'up'
		else:
			direction = 'right'
	elif (x1 < x2):      # food is on the left hand side
		if (y1 > y2):    #food is down-left
			direction = 'down'
		elif(y1 < y2):   #food is up-left
			direction = 'up'
		else:
			direction = 'left'
	else:
		if (y1 > y2):    #food is directly below
			direction = 'down'
		else:            #food is directly above
			direction = 'up'		
	return {
		'move': direction,
		'taunt': 'dat is not de wae'
	}		
#sfwefw

	# Find the distance from us to food
	# Find the distance from opponent to food
	# If the opponent is closer then we pass
	# If we are closer then find the next food and compare

	#if (mysnake_head['y'] == 0 and mysnake_head['x'] == 0):   #top left
	#	direction = 'down'
	#elif (mysnake_head['y'] == board_height-1 and mysnake_head['x'] == board_width-1):   #bottom right
	#	direction = 'up'
	#elif (mysnake_head['y'] == 0 and mysnake_head['x'] == board_width-1 ):    #top right
	#	direction = 'left'
	#elif (mysnake_head['y'] == board_height-1 and mysnake_head['x'] == 0):   #bottom left
	#	direction = 'right'
	#elif (mysnake_head['y'] == 0):   #top
	#	direction = 'left'
	#elif (mysnake_head['x'] == 0):   #left
	#	direction = 'down'
	#elif (mysnake_headp['y'] == board_height-1):    #bottom
	#	direction = 'right'
	#elif (mysnake_head['x'] == board_width-1):     #right
	#	direction = 'up'
	#return {
	#	'move': direction,
	#	'taunt': 'dat is not de wae'
	#}




# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
	bottle.run(
		application,
		host=os.getenv('IP', '0.0.0.0'),
		port=os.getenv('PORT', '8080'),
debug = True)

 food = board[y][x] 