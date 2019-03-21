import math, random, copy, pickle
from operator import itemgetter
from heuristics import zw_heuristic, naive_heuristic

ROTATION = {
	1: {
		'C1' : {'colour':'R','dot':'F'},
		'C2' : {'colour':'W','dot':'C'},
		'link': 'right'
	},
	2: {
		'C1' : {'colour':'W','dot':'C'},
		'C2' : {'colour':'R','dot':'F'},
		'link': 'up'
	},
	3:{
		'C1' : {'colour':'W','dot':'C'},
		'C2' : {'colour':'R','dot':'F'},
		'link': 'right'
	},
	4:{
		'C1' : {'colour':'R','dot':'F'},
		'C2' : {'colour':'W','dot':'C'},
		'link': 'up'
	},
	5:{
		'C1' : {'colour':'R','dot':'C'},
		'C2' : {'colour':'W','dot':'F'},
		'link': 'right'
	},
	6:{
		'C1' : {'colour':'W','dot':'F'},
		'C2' : {'colour':'R','dot':'C'},
		'link': 'up'
	},
	7:{
		'C1' : {'colour':'W','dot':'F'},
		'C2' : {'colour':'R','dot':'C'},
		'link': 'right'
	},
	8:{
		'C1' : {'colour':'R','dot':'C'},
		'C2' : {'colour':'W','dot':'F'},
		'link': 'up'
	}
}
COLUMNS = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

WIDTH = 8
HEIGHT = 12
GRID = []																					# 1D board representation - each element is a cell object
MAX_PLAYER = 'colour'
MIN_PLAYER = 'dot'
TREE_HEIGHT = 3																		# depth/height, doesn't include root node
NUM_CHILDREN = len(ROTATION) * WIDTH														# 8 rotations * maximum number of legal cells
MAX_LEAVES = int(math.pow(NUM_CHILDREN, TREE_HEIGHT))										# number of nodes with a value
MAX_NODES = int((math.pow(NUM_CHILDREN, TREE_HEIGHT + 1) - 1 ) / ( NUM_CHILDREN - 1 ))		# total calculated nodes of tree
TREE_ARRAY = [math.nan] * MAX_NODES															# k-ary array
TREE_ARRAY_MOVES = [{}] * MAX_NODES	
HCOUNT = 0

# Pre-generate lookup table for cell reference and dereference
cell_lookup = {}

def clear_tree():
	global TREE_ARRAY
	global TREE_ARRAY_MOVES
	TREE_ARRAY = [math.nan] * MAX_NODES															# k-ary array
	TREE_ARRAY_MOVES = [{}] * MAX_NODES	

def cell_transform():
	for index in range(HEIGHT*WIDTH):
		column = index % (WIDTH) +1
		row = ((int) (index /(WIDTH)))
		coordinates = int(str(row) + str(column))
		cell_lookup[index] = coordinates
cell_transform()

# # #							# # #
# # #  Board manipulation code 	# # #
# # #							# # #	
def getLegalCells(board_state):
	legal_cells = set()
	for cell in range(len(board_state)):						
		# cell has been played, check above
		if isOccupiedCell(board_state, cell):
			if cell + WIDTH <= len(board_state) - 1:
				if not isOccupiedCell(board_state, cell + WIDTH):
					legal_cells.add(cell+WIDTH)
		# if board_state[cell]['colour'] == 'R' or board_state[cell]['colour'] == 'W':
		# 	if cell + WIDTH <= len(board_state) - 1:
		# 		if board_state[cell + WIDTH]['colour'] != 'R' and board_state[cell + WIDTH]['colour'] != 'W':				
		# 			legal_cells.append(cell+WIDTH)
			
		# cell is in first row
		elif cell < WIDTH:			
			if not isOccupiedCell(board_state, cell+WIDTH):
			# if board_state[cell + WIDTH]['colour'] != 'R' or board_state[cell + WIDTH]['colour'] != 'W':
				legal_cells.add(cell)				

	# # double check to remove unnecessary values
	# for c in legal_cells:
	# 	if (c + WIDTH) in legal_cells:
	# 		legal_cells.remove(c + WIDTH)

	return list(legal_cells)

def setWidth(width):
	WIDTH = width

def setHeight(height):
	HEIGHT = height

# missing recycled move code
def addMoveToBoard(parent_board, move, legal_cells):
		# board = copy.deepcopy(parent_board)
		board = pickle.loads(parent_board)
		column = move['column']
		row = move['row']
		rotation = move['rotation']

		# check last move played for RECYCLED moves
		"""
		if IS_RECYCLED_GAME:
			last_move = list(MOVE_HISTORY.items())[-1][1]
			if last_move['column'] == column and last_move['row'] == row and last_move['rotation']:
				return False
		"""

		# check bounds
		if(column > WIDTH or column < 0 or row > HEIGHT or row < 0):
			#print('[Illegal] Move out of bounds')
			return False

		# determine placement in array
		index = column + (row * WIDTH)

		# check empty cell
		if(board[index]['colour'] == 'R' or board[index]['colour'] == 'W'):
			#print('[Illegal] Cell Occupied')
			return False

		# if in legal cells
		if( index not in legal_cells):
			#print('[Illegal] not in legal cells')
			return False


		# Get cell attributes of rotation type
		C1 = ROTATION[rotation]['C1']
		C2 = ROTATION[rotation]['C2']
		link = ROTATION[rotation]['link']

		# determine index of link cell
		if (link is	'up'):
			link = index + WIDTH
			if(link >= (WIDTH * HEIGHT)):				
				#print('[Illegal] Link above can\'t play')
				return False
		else:
			link = index + 1
			if(link >= (WIDTH * (row+1))):
				#print('[Illegal] LINK out of row bounds')
				return False

			elif( ( link )not in legal_cells):		# prev link + 1?
				#print('[Illegal] link right not legal')
				return False

		# check if cell is occupied
		if isOccupiedCell(board, index) or isOccupiedCell(board, link):
			return False

		# updateLegalCells(legal_cells, index, link)
		if ROTATION[rotation]['link'] == 'right':			
			updateCell( board ,index, C1['colour'], C1['dot'], link, '>' )  
			updateCell( board, link, C2['colour'], C2['dot'], index, '<' )
		elif ROTATION[rotation]['link'] == 'up':
			updateCell( board, index, C1['colour'], C1['dot'], link, '^' )
			updateCell( board, link, C2['colour'], C2['dot'], index, 'v' )
		return board

def isOccupiedCell(board, cell):
	return board[cell]['colour'] != "" or board[cell]['dot'] != ""

def updateCell(board, cell, colour, dot, link, link_direction):
	board[cell]['colour'] = colour
	board[cell]['dot'] = dot
	board[cell]['link'] = link
	board[cell]['link_direction'] = link_direction

def displayBoard(board):
	display_height = 1
	for i in range(WIDTH):
		print(' _ _ _', end='')
	print()

	output = []
	string = ''
	# board
	for i in range(len(board)): 
		link_direction = '.' if str(board[i]['link_direction']) == '' else str(board[i]['link_direction'])
		colour = '.' if str(board[i]['colour']) == '' else str(board[i]['colour'])
		dot = '.' if str(board[i]['dot']) == '' else str(board[i]['dot'])
		string += "|"+ link_direction + colour + dot + link_direction +"|" 			
		
		# newline at width length
		if(math.ceil(i % WIDTH) is WIDTH-1):
			string += str(display_height)
			output.append(string)
			string = ''
			
			display_height += 1
	
	# display right-side-up				
	for line in range(len(output),0,-1):
		print(output[line-1])

	# column names 
	for i in range(WIDTH):
		print('  '+ COLUMNS[i] +'   ',end='')
	print('')


# # #			# # #
# # #  MiniMax	# # #
# # #			# # #
def setTreeHeght(height):
	TREE_HEIGHT = height
	
def setMaxPlayer(player_type):
	if player_type == 'colour':
		MAX_PLAYER = 'colour'
		MIN_PLAYER = 'dot'
	else:
		MAX_PLAYER = 'dot'
		MIN_PLAYER = 'colour'

def calculateHeuristic(board_state, player_type):

	# score = zw_heuristic(board_state, cell_lookup)
	score = naive_heuristic(board_state, cell_lookup)
	if player_type == 0: 
		return score
	else:
		return score * -1

# Creates a 1D k-ary tree based on TREE_HEIGHT and NUM_CHILDREN per node
# Tree is build DEPTH FIRST
def buildTree(depth, parent_index, board_state = False, legal_cells = False, recycling=False, last_move=None, player_type=0):
	# not at leaf node	
	if depth is not TREE_HEIGHT:						

		# contents of parent node - 0 is not appropriate placeholder	 
		TREE_ARRAY[parent_index] = 0		
		
		# testing algorithm
		# Uncomment this and comment out production section
		"""
		for c in range(NUM_CHILDREN):
			child_index = NUM_CHILDREN * parent_index + c + 1

			# go to child node
			buildTree(depth + 1, child_index)
		
		"""

		### production algorithm 
		child_index_count = 0
		pickle_board = pickle.dumps(board_state)
		for index in legal_cells:														
			for r in ROTATION:
				child_index = NUM_CHILDREN * parent_index + child_index_count + 1

				new_move = {
					'column' : index % WIDTH,
					'row' : math.floor( index / WIDTH),
					'rotation' : r
				}
				if recycling:
					if last_move == new_move:
						new_board = False
				# returns new board if legal, False bool if illegal
				new_board = addMoveToBoard(pickle_board, new_move, legal_cells)

				if recycling:
					if last_move['column'] == new_move['column']:
						if last_move['row'] == last_move['row']:
							print("FALSE depth{}".format(depth))
							print(new_move)
							print(last_move)
							# print(board_state)
							new_board = False

				if new_board != False:	
					
					child_index_count += 1

					# add move to array
					TREE_ARRAY_MOVES[child_index] = new_move

					new_legal_cells = getLegalCells(new_board)
					# immediately follow child subtree						
					buildTree( depth + 1, child_index, new_board, new_legal_cells )
				
				# make subtree unavailable
				else:										
					child_index_count += 1			

					# buildTree(depth + 1, child_index, copy.deepcopy(board_state), copy.deepcopy(legal_cells))					
					TREE_ARRAY[child_index] = math.nan															
	
	# at leaf node 
	else:
		heuristic = calculateHeuristic(board_state, player_type)
		TREE_ARRAY[parent_index] = heuristic
		

# Pretty prints tree
def printTree(depth, parent_index):
	total_children = 0
	if depth is not TREE_HEIGHT:
		for k in range(depth):
			print('\t',end='')
		print('Parent['+str(parent_index)+']: '+str(TREE_ARRAY[parent_index]))
		for c in range(NUM_CHILDREN):
			for i in range(depth):
				print('\t',end='')
			child_index = NUM_CHILDREN * parent_index + c + 1
			print('\tChild['+str(child_index)+']: '+str(TREE_ARRAY[child_index]))
			
			if not math.isnan(TREE_ARRAY[child_index]):
				total_children += 1
			
			printTree(depth + 1, child_index)
	if total_children != 0:
		for k in range(depth):
			print('\t',end='')
		print('Parent['+str(parent_index)+'] has # children: ' +str(total_children))


def traceHeuristic(stats, children_values, evaluated_children, parent_node_value):
	print(stats)	
	with open('trace.txt', 'a') as file:
		file.write(str(evaluated_children)+'\n')
		file.write(str(parent_node_value)+'\n\n')
		for node in children_values:
			file.write(str(node)+'\n')
		file.write('\n')

def minMax(depth, parent_index, show_stats=False, recycling=False):
	stats = ""
	evaluated_children = 0
	children_values = []
	move_to_play = {}
	if depth is not TREE_HEIGHT:
		
		# odd depth have to max
		if (depth % 2) != 0:
			node_value = -math.inf
			
			# check value of each child
			for c in range(NUM_CHILDREN):
				
				child_index = NUM_CHILDREN * parent_index + c + 1
				child_value, move_dump, child_eval = minMax(depth + 1, child_index, show_stats)
				evaluated_children += child_eval

				# ignore inf and nan
				# if math.isinf(node_value) and not math.isnan(child_value):
				# 	node_value = child_value
				
				# if math.isinf(child_value):
				# 	child_value = -math.inf

				#node_value = max(node_value, child_value)
				if child_value > node_value:
					node_value = child_value
					move_to_play = TREE_ARRAY_MOVES[child_index]
				if not math.isinf(child_value):
					children_values.append(child_value)
					evaluated_children += 1
			if math.isinf(node_value):
				node_value = math.inf
			for n in range(depth):
				stats += '\t'
			stats += '(-) for node ['+str(parent_index)+'] = ['+str(node_value)+'] \t--> ' + str(move_to_play)			

			if show_stats and depth == 1:
				# if evaluated_children != 0 and not math.isinf(node_value):
				if not recycling:
					traceHeuristic(stats, children_values, evaluated_children, node_value)
				return node_value, move_to_play, evaluated_children, children_values

			return node_value, move_to_play, evaluated_children

		# even == MAX_PLAYER
		else:
			node_value = math.inf
			
			# check value of each child
			nodes =[]
			for c in range(NUM_CHILDREN):			
				
				child_index = NUM_CHILDREN * parent_index + c + 1
				child_value, move_dump, child_eval = minMax(depth + 1, child_index, show_stats)
				
				evaluated_children += child_eval
				nodes.append(node_value)
				# ignore inf and nan
				# if math.isinf(node_value) and not math.isnan(child_value):
				# 	node_value = child_value
				
				# if math.isinf(child_value):
				# 	child_value = math.inf

				#node_value = min(node_value, child_value)			
				if child_value < node_value:
					node_value = child_value
					move_to_play = TREE_ARRAY_MOVES[child_index]
				if not math.isinf(child_value):
					children_values.append(child_value)
					evaluated_children += 1
			if math.isinf(node_value):
				node_value = -math.inf
			for n in range(depth):
				stats += '\t'
			stats += '(+) for node ['+str(parent_index)+'] = ['+str(node_value)+'] \t--> ' + str(move_to_play)
			
			if show_stats and depth == 1:
				# if evaluated_children != 0 and not math.isinf(node_value):
				if not recycling:
					traceHeuristic(stats, children_values, evaluated_children, node_value)
				return node_value, move_to_play, evaluated_children, children_values
			return node_value, move_to_play, evaluated_children

	# terminal node, return value
	else:		
		node_value = TREE_ARRAY[parent_index]
		move_to_play = TREE_ARRAY_MOVES[parent_index]
		return node_value, move_to_play, 0

def interfaceBoard(board_state):
	formatted_board = []
	# return board_state # for use to test with local code
	for n in board_state.board:
		# Symbol
		board_symbol = n.get_symbol()
		dot = ""
		if board_symbol == '\u25E6' :
			dot = 'C'
		elif board_symbol == '\u2022' :
			dot =  'F'

		# Colour
		board_color = n.get_color()
		color = ""
		if board_color == "Red":
			color = "R"
		elif board_color == "White":
			color = "W"

		# Direction
		direction = "."
		cell_direction = n.link_direction()
		if cell_direction == "up":
			direction = "^"
		elif cell_direction == 'down':
			direction = 'v'
		elif cell_direction == 'left':
			direction = '<'
		elif cell_direction == 'right':
			direction = '>'

		# link cell index
		cell_index = n.get_id()
		cell_variant = n.get_variant()
		if cell_variant == None:
			cell_link = ""
		elif cell_variant % 2 == 1:
			if cell_direction == 'left':
				cell_link = cell_index-1
			else:
				cell_link = cell_index+1 
		else:
			if cell_direction == 'down':
				cell_link = cell_index-8
			else:
				cell_link = cell_index+8


		cell = {
			"colour": color,
			"dot": dot,
			"link": cell_link,
			"link_direction": direction
		}
		formatted_board.append(cell)

	# formatted_board = board_state.copy()
	return formatted_board

def formatMove(move, recycling=False, r1=None, r2=None):
	print(move)
	if recycling:
		r1_row = math.floor(r1 / WIDTH),
		r2_row = math.floor(r2 / WIDTH),
		r1_col = r1 % WIDTH
		r2_col = r2 % WIDTH
		output = "{} {} {} {} {} {} {}".format(
			COLUMNS[r1_col], r1_row[0]+1, COLUMNS[r2_col], r2_row[0]+1,
			move['rotation'],COLUMNS[move['column']], move['row'] + 1)
	else:
		output = '0 '
		output += str(move['rotation']) + ' '
		output += COLUMNS[move['column']] + ' '
		output += str(move['row'] + 1) 
	return output

def parseMove(move):
	output = {
		'column' : 0,
		'row' : 0,
		'rotation' : 0
	}
	move_arr = move.split(" ")
	if len(move_arr) == 4:
		output['rotation'] = int(move_arr[1]) #Rotation
		for index,letter in enumerate(COLUMNS,0):
			if letter == move_arr[2]:
				output['column'] = index
				break
		output['row'] = int(move_arr[3]) - 1 
	else: # len == 7 A 1 A 2 2 H 1
		output['rotation'] = int(move_arr[4]) #Rotation
		for index,letter in enumerate(COLUMNS,0):
			if letter == move_arr[5]:

				output['column'] = index
				break
		output['row'] = int(move_arr[6]) - 1
	return output

def removable(board_state, last_move):
	removable_cells = set()
	for cell in range(len(board_state)):						
		if isOccupiedCell(board_state, cell):
			if ((cell + WIDTH) >= len(board_state)):
				removable_cells.add(cell)
				removable_cells.add(board_state[cell]['link'])
			elif not isOccupiedCell(board_state, cell + WIDTH):
				removable_cells.add(cell)
				removable_cells.add(board_state[cell]['link'])
	# Make last move tile unremovable
	index = last_move['row']*WIDTH + last_move['column']
	removable_cells = removable_cells - {index}
	removable_cells = removable_cells - {board_state[index]['link']}
	return removable_cells			

def removeCell(board_state, cell):
	board = pickle.loads(board_state)
	cell_link = board[cell]['link']
	board[cell_link] =  {
		"colour": '',
		"dot": '',
		"link": '',
		"link_direction": ''
	}
	board[cell] =  {
		"colour": '',
		"dot": '',
		"link": '',
		"link_direction": ''
	}
	return board

def getNextMove(board_state, player_type=1, show_stats=False,recycling=False,prev_move=None):
	clear_tree()
	root_board = interfaceBoard(board_state)

	minmax_output = 0
	if recycling:
		last_move = parseMove(prev_move)
		# get removable list of cells
		removable_cells = removable(root_board, last_move)
		removed = set()
		replaced_outputs = []
		for r in removable_cells:
			if r in removed:
				continue
			dumped_board = pickle.dumps(root_board)
			modified_board = removeCell(dumped_board, r)
			legal_cells = getLegalCells(modified_board)
			# add prev move as illegal
			buildTree(1,0, modified_board, legal_cells, recycling=True, last_move=last_move, player_type=player_type)
			removed.add(r)
			removed.add(root_board[r]['link'])
			if player_type == 'colour' or player_type == 'color' or player_type == 1:
				local_minmax_output = minMax(1, 0, show_stats, True)
			else:
				local_minmax_output = minMax(1, 0, show_stats, True)
			replaced_outputs.append(local_minmax_output+(r, root_board[r]['link']))
			clear_tree()
		# check if this is correct.
		if player_type == 'colour' or player_type == 'color' or player_type == 1:
			minmax_output = min(replaced_outputs,key=itemgetter(0))
		else:
			minmax_output = max(replaced_outputs,key=itemgetter(0))
		evaluated_children = 0
		children_values = []
		for output in replaced_outputs:
			evaluated_children += output[2]
			children_values.extend(output[3])
		traceHeuristic("", children_values, evaluated_children, minmax_output[0])
		# max(output)
	else:
		legal_cells = getLegalCells(root_board)
		buildTree(1, 0, root_board, legal_cells)
		# printTree(1,0)
		# if show_trace == True:
		# 	printTree(1,0)

		if player_type == 'colour' or player_type == 'color' or player_type == 1:
			minmax_output = minMax(1, 0, show_stats)
		else:
			minmax_output = minMax(1, 0, show_stats)

		if show_stats == True:
			# meta stats
			print('',end="\n**************\n")
			print('Dimensions', end=': ')
			print(str(WIDTH)+' '+str(HEIGHT))
			print('Board Cells', end=': ')
			print(str(WIDTH * HEIGHT))
			print('Depth', end=': ')
			print(str(TREE_HEIGHT))
			print('Children per node', end=': ')
			print(NUM_CHILDREN)
			print('Max nodes', end=': ')
			print(MAX_NODES)
			print('Max leaves', end=': ')
			print(MAX_LEAVES)
			print('Parent Nodes', end=': ')
			print(MAX_NODES - MAX_LEAVES)
			print('Length of tree', end=': ')
			print(len(TREE_ARRAY))
			print('HCOUNT:{}'.format(HCOUNT))

	print(minmax_output)
	if recycling:
		formatted_move = formatMove(minmax_output[1],recycling=True, r1=minmax_output[4], r2=minmax_output[5])
	else:
		formatted_move = formatMove(minmax_output[1])
	# print(root_board)
	return formatted_move

if __name__ == "__main__":
	print('\n*****MIN MAX TESTS****')
	test_board = []
	for n in range(WIDTH * HEIGHT):
		cell = {
			"colour": '',
			"dot": '',
			"link": '',
			"link_direction": ''
		}
		test_board.append(cell)

	# populate tree
	# print(getNextMove(test_board, 'dot', show_stats=True, show_trace=True))

	# test Recycling
	# test_board = [{'colour': 'W', 'dot': 'C', 'link': 8, 'link_direction': '^'}, {'colour': 'W', 'dot': 'C', 'link': 9, 'link_direction': '^'}, {'colour': 'W', 'dot': 'C', 'link': 10, 'link_direction': '^'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'W', 'dot': 'C', 'link': 12, 'link_direction': '^'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'W', 'dot': 'C', 'link': 14, 'link_direction': '^'}, {'colour': 'R', 'dot': 'C', 'link': 15, 'link_direction': '^'}, {'colour': 'R', 'dot': 'F', 'link': 0, 'link_direction': 'v'}, {'colour': 'R', 'dot': 'F', 'link': 1, 'link_direction': 'v'}, {'colour': 'R', 'dot': 'F', 'link': 2, 'link_direction': 'v'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'R', 'dot': 'F', 'link': 4, 'link_direction': 'v'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'R', 'dot': 'F', 'link': 6, 'link_direction': 'v'}, {'colour': 'W', 'dot': 'F', 'link': 7, 'link_direction': 'v'}, {'colour': 'W', 'dot': 'C', 'link': 24, 'link_direction': '^'}, {'colour': 'W', 'dot': 'C', 'link': 25, 'link_direction': '^'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'R', 'dot': 'C', 'link': 30, 'link_direction': '^'}, {'colour': 'R', 'dot': 'C', 'link': 31, 'link_direction': '^'}, {'colour': 'R', 'dot': 'F', 'link': 16, 'link_direction': 'v'}, {'colour': 'R', 'dot': 'F', 'link': 17, 'link_direction': 'v'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'W', 'dot': 'F', 'link': 22, 'link_direction': 'v'}, {'colour': 'W', 'dot': 'F', 'link': 23, 'link_direction': 'v'}, {'colour': 'W', 'dot': 'C', 'link': 40, 'link_direction': '^'}, {'colour': 'W', 'dot': 'C', 'link': 41, 'link_direction': '^'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'W', 'dot': 'C', 'link': 46, 'link_direction': '^'}, {'colour': 'R', 'dot': 'C', 'link': 47, 'link_direction': '^'}, {'colour': 'R', 'dot': 'F', 'link': 32, 'link_direction': 'v'}, {'colour': 'R', 'dot': 'F', 'link': 33, 'link_direction': 'v'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'R', 'dot': 'F', 'link': 38, 'link_direction': 'v'}, {'colour': 'W', 'dot': 'F', 'link': 39, 'link_direction': 'v'}, {'colour': 'W', 'dot': 'C', 'link': 56, 'link_direction': '^'}, {'colour': 'R', 'dot': 'C', 'link': 57, 'link_direction': '^'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'R', 'dot': 'C', 'link': 62, 'link_direction': '^'}, {'colour': 'R', 'dot': 'C', 'link': 63, 'link_direction': '^'}, {'colour': 'R', 'dot': 'F', 'link': 48, 'link_direction': 'v'}, {'colour': 'W', 'dot': 'F', 'link': 49, 'link_direction': 'v'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'W', 'dot': 'F', 'link': 54, 'link_direction': 'v'}, {'colour': 'W', 'dot': 'F', 'link': 55, 'link_direction': 'v'}, {'colour': 'W', 'dot': 'C', 'link': 72, 'link_direction': '^'}, {'colour': 'R', 'dot': 'C', 'link': 73, 'link_direction': '^'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'R', 'dot': 'C', 'link': 79, 'link_direction': '^'}, {'colour': 'R', 'dot': 'F', 'link': 64, 'link_direction': 'v'}, {'colour': 'W', 'dot': 'F', 'link': 65, 'link_direction': 'v'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'W', 'dot': 'F', 'link': 71, 'link_direction': 'v'}, {'colour': 'R', 'dot': 'C', 'link': 88, 'link_direction': '^'}, {'colour': 'R', 'dot': 'C', 'link': 89, 'link_direction': '^'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'R', 'dot': 'C', 'link': 95, 'link_direction': '^'}, {'colour': 'W', 'dot': 'F', 'link': 80, 'link_direction': 'v'}, {'colour': 'W', 'dot': 'F', 'link': 81, 'link_direction': 'v'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'W', 'dot': 'F', 'link': 87, 'link_direction': 'v'}]
	# test_board = [{'colour': 'W', 'dot': 'C', 'link': 8, 'link_direction': '^'}, {'colour': 'W', 'dot': 'C', 'link': 9, 'link_direction': '^'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'R', 'dot': 'C', 'link': 14, 'link_direction': '^'}, {'colour': 'R', 'dot': 'C', 'link': 15, 'link_direction': '^'}, {'colour': 'R', 'dot': 'F', 'link': 0, 'link_direction': 'v'}, {'colour': 'R', 'dot': 'F', 'link': 1, 'link_direction': 'v'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'W', 'dot': 'F', 'link': 6, 'link_direction': 'v'}, {'colour': 'W', 'dot': 'F', 'link': 7, 'link_direction': 'v'}, {'colour': 'W', 'dot': 'C', 'link': 24, 'link_direction': '^'}, {'colour': 'W', 'dot': 'C', 'link': 25, 'link_direction': '^'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'R', 'dot': 'C', 'link': 30, 'link_direction': '^'}, {'colour': 'R', 'dot': 'C', 'link': 31, 'link_direction': '^'}, {'colour': 'R', 'dot': 'F', 'link': 16, 'link_direction': 'v'}, {'colour': 'R', 'dot': 'F', 'link': 17, 'link_direction': 'v'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'W', 'dot': 'F', 'link': 22, 'link_direction': 'v'}, {'colour': 'W', 'dot': 'F', 'link': 23, 'link_direction': 'v'}, {'colour': 'W', 'dot': 'C', 'link': 40, 'link_direction': '^'}, {'colour': 'W', 'dot': 'C', 'link': 41, 'link_direction': '^'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'R', 'dot': 'C', 'link': 46, 'link_direction': '^'}, {'colour': 'R', 'dot': 'C', 'link': 47, 'link_direction': '^'}, {'colour': 'R', 'dot': 'F', 'link': 32, 'link_direction': 'v'}, {'colour': 'R', 'dot': 'F', 'link': 33, 'link_direction': 'v'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'W', 'dot': 'F', 'link': 38, 'link_direction': 'v'}, {'colour': 'W', 'dot': 'F', 'link': 39, 'link_direction': 'v'}, {'colour': 'W', 'dot': 'C', 'link': 56, 'link_direction': '^'}, {'colour': 'W', 'dot': 'C', 'link': 57, 'link_direction': '^'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'R', 'dot': 'C', 'link': 62, 'link_direction': '^'}, {'colour': 'R', 'dot': 'C', 'link': 63, 'link_direction': '^'}, {'colour': 'R', 'dot': 'F', 'link': 48, 'link_direction': 'v'}, {'colour': 'R', 'dot': 'F', 'link': 49, 'link_direction': 'v'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'W', 'dot': 'F', 'link': 54, 'link_direction': 'v'}, {'colour': 'W', 'dot': 'F', 'link': 55, 'link_direction': 'v'}, {'colour': 'W', 'dot': 'C', 'link': 72, 'link_direction': '^'}, {'colour': 'W', 'dot': 'C', 'link': 73, 'link_direction': '^'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'R', 'dot': 'C', 'link': 78, 'link_direction': '^'}, {'colour': 'R', 'dot': 'C', 'link': 79, 'link_direction': '^'}, {'colour': 'R', 'dot': 'F', 'link': 64, 'link_direction': 'v'}, {'colour': 'R', 'dot': 'F', 'link': 65, 'link_direction': 'v'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'W', 'dot': 'F', 'link': 70, 'link_direction': 'v'}, {'colour': 'W', 'dot': 'F', 'link': 71, 'link_direction': 'v'}, {'colour': 'R', 'dot': 'C', 'link': 88, 'link_direction': '^'}, {'colour': 'W', 'dot': 'C', 'link': 89, 'link_direction': '^'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'R', 'dot': 'C', 'link': 94, 'link_direction': '^'}, {'colour': 'R', 'dot': 'C', 'link': 95, 'link_direction': '^'}, {'colour': 'W', 'dot': 'F', 'link': 80, 'link_direction': 'v'}, {'colour': 'R', 'dot': 'F', 'link': 81, 'link_direction': 'v'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': '', 'dot': '', 'link': '', 'link_direction': '.'}, {'colour': 'W', 'dot': 'F', 'link': 86, 'link_direction': 'v'}, {'colour': 'W', 'dot': 'F', 'link': 87, 'link_direction': 'v'}]
	# print(getNextMove(test_board,'dot',show_stats=True,recycling=True,prev_move="H 11 H 12 8 H 11")) 

