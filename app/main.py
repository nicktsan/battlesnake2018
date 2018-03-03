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
		'color': '#FF0000',
		'taunt': 'dat is not de wae',
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
	mysnake = data['you']
	snake_list = data['snakes']
	food_list = data['food'] #use food_list['data'][int]['x'] to get the 'x' point of food at index int in the food list
	directions = ['up', 'down', 'left', 'right']
	mysnake_head = mysnake['body']['data'][0] #should get the head's point
	mysnake_neck = mysnake['body']['data'][1] #should get the neck's point

	board = init_board(food_list, snake_list, board_width, board_height)
	
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
		#Find our head location
		"""
		x2 = mysnake_head['x']
		y2 = mysnake_head['y']

		coordinate = []

		for food in food_list['data']:    # Find a food
			x1 = food['x']
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
		"""
		coordinate,x2,y2 = seek_food(mysnake_head, food_list, snake_list, mysnake)

		
		counter = 0
		for line in coordinate:
			row = coordinate[counter]
			food_dist = row[0]
			x1 = row[1]
			y1 = row[2]
			path = jps((x2, y2), (x1, y1), board)
			if path == None:
				counter += 1
				continue
			else:
				head, nextNode = path[0][0], path[0][1]
				vect = calc_vec(head[0], head[1], nextNode[0], nextNode[1])
				vX, vY = vect[0], vect[1]
				if (vX < 0):
					if ('left' in moves):
						moves['left'] += 1
				if (vX > 0):
					if ('right' in moves):
						moves['right'] += 1
				if (vY < 0):
					if ('up' in moves):
						moves['up'] += 1
				if (vY > 0):
					if ('down' in moves):
						moves['down'] += 1
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