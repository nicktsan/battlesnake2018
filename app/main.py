from battlesnake_functions import *
import operator
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
	directions = ['up', 'down', 'left', 'right']
	mysnake_head = mysnake['body']['data'][0] #should get the head's point
	mysnake_neck = mysnake['body']['data'][1] #should get the neck's point
	mylength =  mysnake['length']
	myhealth = mysnake['health']

	board = init_board(food_list, snake_list, board_width, board_height, mysnake_head)
	
	is_left = check_left(mysnake_head['x'], mysnake_head['y'], board)
	is_right = check_right(mysnake_head['x'], mysnake_head['y'], board)
	is_up = check_up(mysnake_head['x'], mysnake_head['y'], board)
	is_down = check_down(mysnake_head['x'], mysnake_head['y'], board)
	
	# TODO: Do things with data
	if (is_up == True):
		directions.remove('up')
	if (is_down == True):
		directions.remove('down')
	if (is_left == True):
		directions.remove('left')
	if (is_right == True):
		directions.remove('right')
	direction = random.choice(directions)

	#We only need to do advanced decision making if there is more than 1 viable choice that will not kill the snake.
	if (len(directions) > 1):
		#make a dictionary for remaining viable directions.
		#For example: if directions = ['up', 'down', 'right'] then moves will be
		#							  {'up': 0, 'down': 0, 'right': 0}
		moves = {}
		for direction in directions:
			moves[direction] = 0
		"""
		TODO assign points to corresponding choices
		Let's say we want to give 'right' 3 points. Type:
			moves['right'] += 3 
		moves will then become 
			{'up': 0, 'down': 0, 'right': 3}
		"""
		goal_points = seek_food(mysnake_head, food_list, snake_list, mysnake)
		#goal_points is a list of [distance, x, y] objects
		for goal_point in goal_points:
			path = jps((mysnake_head['x'], mysnake_head['y']), (goal_point[1], goal_point[2]), board)
			if path != None:
				head, nextNode = path[0][0], path[0][1]
				vect = calc_vec(head[0], head[1], nextNode[0], nextNode[1])
				vX, vY = vect[0], vect[1]
				priority = 200
				score = (priority - myhealth)*0.01
				if (vX < 0):
					if ('left' in moves):
						moves['left'] += score
				if (vX > 0):
					if ('right' in moves):
						moves['right'] += score
				if (vY < 0):
					if ('up' in moves):
						moves['up'] += score
				if (vY > 0):
					if ('down' in moves):
						moves['down'] += score
				break
		
		for move in moves:
			x, y = mysnake_head['x'], mysnake_head['y']
			if move == 'left':
				x -= 1
			if move == 'right':
				x += 1
			if move == 'up':
				y -= 1
			if move == 'down':
				y += 1
			num_obstacles = checkOneTileAway(board, x, y, mylength, snake_list)
			penalty = -0.25
			if (num_obstacles > 1):
				moves[move] = moves[move] - penalty*num_obstacles
			if (num_obstacles >= 3):
				moves[move] -= 10000
		#get the direction with the most points, return that as the final direction
		direction = max(moves.iteritems(), key = operator.itemgetter(1))[0]
	
	
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