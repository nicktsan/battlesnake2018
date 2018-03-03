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
	
	x2 = mysnake_head['x']
	y2 = mysnake_head['y']
	coordinate = []
	
	for food in food_list['data']:    # Find a food
		x1 = food['x']
		y1 = food['y']
		food_ok = 0
		# check all obstacles in between (call function)
		distance = calc_distance(x1,y1,x2,y2)   #calculate the distance from food to head
		# get the coordinate of all other snakes
		for other_snake in snake_list['data']:
			if (snake_list['id'] == mysnake['id']):
				continue
			else:
				othersnake_head = othersnake['body']['data'][0]
				x3 = othersnake_head['x']
				y3 = othersnake_head['y']
				other_distance = calc_distance(x1,y1,x3,y3)
				if (distance < other_distance):
					pass
				elif (distance > other_distance):
					food_ok + 1
				else:
					other_length = othersnake['length']
					our_length = mysnake['length']
					if (other_length > our_length):
						food_ok + 1
					elif (our_length > other_length):
						pass
					else:
						food_ok + 1
		if (food_ok == 0):
			coordinate.append([distance, x1, y1])       #store distancea and coordinatea in list
				
		# call obstacles in between function
		# call calc_distance function

		#compare our distance with their distance
		# if they are closer, abandon the food, find next food and go through the same process 

		# got the food that we are closer than others, store it in list
	   
	   
	coordinate = sorted(coordinate, key=lambda x:x[0])     #sort all the coordinate base on distance
	row = coordinate[0]             #choose row 0 as the closest food
	food_dist = row[0]
	x1 = row[1]
	y1 = row[2]
	#
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
	#is_left = check_left(mysnake_head['x'], mysnake_head['y'], board)
	#is_right = check_right(mysnake_head['x'], mysnake_head['y'], board)
	#is_up = check_up(mysnake_head['x'], mysnake_head['y'], board)
	#is_down = check_down(mysnake_head['x'], mysnake_head['y'], board)
	
	# TODO: Do things with data
	#if (is_up == True):
	#   directions.remove('up')
	#if (is_down == True):
	#   directions.remove('down')
	#if (is_left == True):
	#   directions.remove('left')
	#if (is_right == True):
	#   directions.remove('right')
	#direction = random.choice(directions)

	#We only need to do advanced decision making if there is more than 1 viable choice that will not kill the snake.
	#if (len(directions) > 1):
		#make a points list for the length of remaining viable directions.
	#   points = np.zeros(len(directions)) #np.zeros(x) creates an array of zeros of length x.
		
		#TODO assign points to corresponding choices



		#calculate which remaining option has the most points
	#   max_point_index = np.argwhere(points == np.amax(points))
	#   top_dirs = []
	#   #create a list of indeces of highest points.
	#   for index in max_point_index:
	#       top_dirs.append(directions[index[0]])
	#   direction = random.choice(top_dirs)
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