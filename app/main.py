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
		#make a points list for the length of remaining viable directions.
		points = np.zeros(len(directions)) #np.zeros(x) creates an array of zeros of length x.
		jumpPoints = 0 #insertjumpPoint algorithm here
		nextJumpPoint = jumpPoints[0][0]
		#stores the recommendations
		recommendations = []
		relativeY = nextJumpPoint[1] - mysnake_head['y']
		relativeX= nextJumpPoint[0] - mysnake_head['x']
		#if our point is above or below
		if(nextJumpPoint[0] == 0):
			#down
			if(relativeY >= 1):
				recommendations.append(checkOneTileAway(board, mysnake_head['x'], mysnake_head['y'] + 1, "down"))
			#up
			else if(relativeY <= -1):
				recommendations.append(checkOneTileAway(board, mysnake_head['x'], mysnake_head['y'] - 1, "up"))
		#if our point is left or right
		else if(nextJumpPoint[1] == 0):
			#right
			if(relativeX >= 1):
				recommendations.append(checkOneTileAway(board, mysnake_head['x'] + 1, mysnake_head['y'], "right"))
			#left
			else if(relativeX <= -1):
				recommendations.append(checkOneTileAway(board, mysnake_head['x'] - 1, mysnake_head['y'], "left"))
		#else we have 2 directions
		else
			#check Quadrant 1
			if(relativeX >= 1 and relativeY >= 1):
				recommendations.append(checkOneTileAway(board, mysnake_head['x'] + 1, mysnake_head['y'], "right"))
				recommendations.append(checkOneTileAway(board, mysnake_head['x'], mysnake_head['y'] + 1, "up"))
			#check Quadrant 4
			else if(relativeX >= 1 and relativeY <= -1)
				recommendations.append(checkOneTileAway(board, mysnake_head['x'] + 1, mysnake_head['y'], "right"))
				recommendations.append(checkOneTileAway(board, mysnake_head['x'], mysnake_head['y'] - 1, "down"))
			#check Quadrant 2
			else if(relativeX <= -1 and relativeY >= 1)
				recommendations.append(checkOneTileAway(board, mysnake_head['x'] - 1, mysnake_head['y'], "left"))
				recommendations.append(checkOneTileAway(board, mysnake_head['x'], mysnake_head['y'] + 1, "up"))
			else if(relativeX <= -1 and relativeY >= 1)
				recommendations.append(checkOneTileAway(board, mysnake_head['x'] - 1, mysnake_head['y'], "left"))
				recommendations.append(checkOneTileAway(board, mysnake_head['x'], mysnake_head['y'] - 1, "down"))
		#goes through each item in recommendations
		recommendationsIndex = 0
		goodDirections = []
		while(i < len(recommendations)):
			if(recommendations[i][1] == True):
				goodDirections.append(recommendations[i][0])
			recommendationsIndex = recommendationsIndex + 1
		#decides on direction
		if(len(goodDirections) > 1):
			direction = random.choice(goodDirections)
		else
			direction = goodDirections

		#calculate which remaining option has the most points
		#max_point_index = np.argwhere(points == np.amax(points))
		#top_dirs = []
		#create a list of indeces of highest points.
		#for index in max_point_index:
		#	top_dirs.append(directions[index[0]])
		#direction = random.choice(top_dirs)
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