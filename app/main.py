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
	directions = ['up', 'down', 'left', 'right']
	mysnake_head = mysnake['body']['data'][0] #should get the head's point
	mysnake_neck = mysnake['body']['data'][1] #should get the neck's point

	board = init_board(food_list, snake_list, board_width, board_height)
	"""
	x2 = mysnake_head['x']
	y2 = mysnake_head['y']
	coordinate = []
	
	
	for food in food_list['data']:    # Find a food
		x1 = food['x']
		y1 = food['y']
		food_ok = True
		# check all obstacles in between (call function)
		distance = calc_distance(x1,y1,x2,y2)   #calculate the distance from food to head
		# get the coordinate of all other snakes
		
		for other_snake in snake_list['data']:
			if (other_snake['id'] != mysnake['id']):
				othersnake_head = other_snake['body']['data'][0]
				x3 = othersnake_head['x']
				y3 = othersnake_head['y']
				other_distance = calc_distance(x1,y1,x3,y3)
				if (distance < other_distance):
					continue
				elif (distance > other_distance):
					food_ok = False
				else:
					other_length = other_snake['length']
					our_length = mysnake['length']
					if (other_length > our_length):
						food_ok = False
					elif (our_length > other_length):
						continue
					else:
						food_ok = False
			
		if (food_ok == True):
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
	"""
	coordinate,x2,y2 = seek_food(mysnake_head, food_list, snake_list, mysnake)

	row = coordinate[0]             #choose row 0 as the closest food
	food_dist = row[0]
	x1 = row[1]
	y1 = row[2]

	path = jps((x2, y2), (x1, y1), board)
	if path != None:
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
	
	



	#figure out which way to turn
	"""
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
	"""
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