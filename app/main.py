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
		'color': '#00FF00',
		'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
		'head_url': head_url,
		'name': 'nicksnek',
		'head_type': 'fang',
		'tail_type': 'block-bum'
	}


@bottle.post('/move')
def move():
	data = bottle.request.json
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
	direction = 'up'
	if (mysnake_head['y'] == 0):
		direction = 'left'
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