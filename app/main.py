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
		'color': '#FF9000',
		'taunt': 'dat is not de wae',
		'head_url': head_url,
		'name': 'nicksnek',
		'head_type': 'tongue',
		'tail_type': 'round-bum'
	}


@bottle.post('/move')
def move():
	data = bottle.request.json
	game_id = data.get('game_id')
	board_width = data.get('width')
	board_height = data.get('height')
	mysnake = data['you']
	snake_list = data['snakes']
	food_list = data['food'] #use food_list['data'][int]['x'] to get the 'x' point of food at index int in the food list
	#directions = ['up', 'down', 'left', 'right']
	mysnake_head = mysnake['body']['data'][0] #should get the head's point
	mysnake_neck = mysnake['body']['data'][1] #should get the neck's point
	mysnake_tail = mysnake['body']['data'][-2] #should get the tail's point for next turn


	board = init_board(food_list, snake_list, board_width, board_height)
	
	coordinate = seek_food(mysnake_head, food_list, snake_list, mysnake)

	x2 = mysnake_head['x']
	y2 = mysnake_head['y']
	x4 = mysnake_tail['x']
	y4 = mysnake_tail['y']

	for result in coordinate:
		food_dist = row[0]
		x1 = row[1]
		y1 = row[2]

		
		#get the direction of next move HELP!

		"""
		if (next_move = 'left'):
			next_move_x,next_move_y = x2-1, y2
		if (next_move = 'up'):
			next_move_x,next_move_y = x2, y2-1
		if (next_move = 'right'):
			next_move_x,next_move_y = x2+1, y2
		if (next_move = 'down'):
			next_move_x,next_move_y = x2, y2+1
		"""
		path = jps((x1, y1), (x4, y4), board)   #(food -> our tail)  
		if path == None:                        #there is no path to the food or destination
			continue
		else:									#if there is a path
			#get the next move HELP!
				#figure out which way to turn

			is_left = check_left(mysnake_head['x'], mysnake_head['y'], board)
			is_right = check_right(mysnake_head['x'], mysnake_head['y'], board)
			is_up = check_up(mysnake_head['x'], mysnake_head['y'], board)
			is_down = check_down(mysnake_head['x'], mysnake_head['y'], board)

			if (x1 > x2):       # if food is on right hand side
				if (y1 > y2):    # if food is down-right
					directions = ['down', 'right', 'up', 'left']
					if (is_down == True):
						directions.remove('down')
					if (is_right == True):
						directions.remove('right')
					if (is_up == True):
						directions.remove('up')
				elif(y1 < y2):   # if food is up-right
					directions = ['up', 'right', 'down', 'left']
					if (is_up == True):
						directions.remove('up')
					if (is_right == True):
						directions.remove('right')
					if (is_down == True):
						directions.remove('down')
				else:
					directions = ['right', 'up', 'down', 'left']
					if (is_right == True):
						directions.remove('right')
					if (is_up == True):
						directions.remove('up')
					if (is_down == True):
						directions.remove('down')
			elif (x1 < x2):      # food is on the left hand side
				if (y1 > y2):    #food is down-left
					directions = ['down', 'left', 'up', 'right']
					if (is_down == True):
						directions.remove('down')
					if (is_left == True):
						directions.remove('left')
					if (is_up == True):
						directions.remove('up')
				elif(y1 < y2):   #food is up-left
					directions = ['up', 'left', 'down', 'right']
					if (is_up == True):
						directions.remove('up')
					if (is_left == True):
						directions.remove('left')
					if (is_down == True):
						directions.remove('down')
				else:
					directions = ['left', 'up', 'down', 'right']
					if (is_left == True):
						directions.remove('left')
					if (is_up == True):
						directions.remove('up')
					if (is_down == True):
						directions.remove('down')
			else:
				if (y1 > y2):    #food is directly below
					directions = ['down', 'up', 'left', 'right']
					if (is_down == True):
						directions.remove('down')
					if (is_up == True):
						directions.remove('up')
					if (is_left == True):
						directions.remove('left')
				else:            #food is directly above
					directions = ['up', 'left', 'right', 'up']
					if (is_up == True):
						directions.remove('up')
					if (is_left == True):
						directions.remove('left')
					if (is_down == True):
						directions.remove('down')
	direction = directions[0]

	#if no move availble from the above for loop, do a survival step that won't kill us HELP!

	#ignore every below!

	
	
	# TODO: Do things with data
	
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