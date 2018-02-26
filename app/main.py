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
	snek, grid = init(data)
	game_id = data.get('game_id')
	board_width = data.get('width')
	board_height = data.get('height')
	mysnake = data['you']['body']['data']
	snake_list = data['snakes']
	mysnake_head = mysnake[0] #should get the head's point
	# TODO: Do things with data
	
	above_headx, above_heady = get_up(mysnake_head)
	directions = ['up', 'down', 'left', 'right']
	#direction = random.choice(directions)
	if (mysnake_head['y'] == 0):
		direction = 'left'
	#if (mysnake_head['y'] == 0 and mysnake_head['x'] == 0):
	#	direction = 'down'
	#elif (mysnake_head['y'] == board_height and mysnake_head['x'] == board_width):
		#direction = 'up'
	#elif (mysnake_head['y'] == 0):
		#direction = 'left'
	#elif (mysnake_head['x'] == 0):
		#direction = 'right'
	return {
		'move': direction,
		'taunt': 'dat is not de wae'
	}


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
	bottle.run(
		application,
		host=os.getenv('IP', '0.0.0.0'),
		port=os.getenv('PORT', '8080'),
debug = True)