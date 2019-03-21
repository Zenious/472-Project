import numpy as np
def naive_heuristic(board_state, cell_lookup):
	score = 0
	for index,cell in enumerate(board_state):

		coordinates = cell_lookup[index]
		if cell['colour'] == 'R':
			if cell['dot'] == 'C':
				score -= 1.5*coordinates
			if cell['dot'] == 'F':
				score -= 2*coordinates
		elif cell['colour'] == 'W':
			if cell['dot'] == 'C':
				score += coordinates
			if cell['dot'] == 'F':
				score += 3*coordinates
		else:
			continue
	return score

def zw_heuristic(board_state, cell_lookup):
	score = 0
	# matrix = np.array(board_state).reshape(12, 8)
	# vert  = np.transpose(matrix)

	# r = 0
	# w = 0
	# c = 0
	# f = 0
	# for x in matrix:
	# 	for y in x:
	# 		if y['colour'] == "R":
	# 			r += 1
	# 		if y['colour'] == "W":
	# 			w += 1
	# 		if y['dot'] == "C":
	# 			c += 1
	# 		if y['dot'] == "F":
	# 			f += 1
	# 	score += r*10+w*5-c*10-f*10
	# for x in vert:
	# 	for y in x:
	# 		if y['colour'] == "R":
	# 			r += 1
	# 		if y['colour'] == "W":
	# 			w += 1
	# 		if y['dot'] == "C":
	# 			c += 1
	# 		if y['dot'] == "F":
	# 			f += 1
	# 	score += r*10+w*5-c*10-f*10
	for index,cell in enumerate(board_state):
		coordinates = cell_lookup[index]
		score = 10
		if cell['colour'] == 'R':
			score -= 10
		if cell['colour'] == 'W':
			score -= 10
		if cell['dot'] == 'C':
			score += 5
		if cell['dot'] == 'F':
			score += 5

		##  7 4 8
		##	1   2
		##  5 3 6
		##
		cell_lookup_1 = index - 1*3
		cell_lookup_2 = index + 1*3
		cell_lookup_3 = index - 8*3
		cell_lookup_4 = index + 8*3
		cell_lookup_5 = index - 9*3
		cell_lookup_6 = index - 7*3
		cell_lookup_7 = index + 7*3
		cell_lookup_8 = index + 9*3
		cell_lookup_list = [cell_lookup_1, cell_lookup_2, cell_lookup_3, cell_lookup_4, cell_lookup_5, cell_lookup_6, cell_lookup_7, cell_lookup_8]
		cell_lookup_list = filter(lambda x: (x < 8*12 and x >= 0), cell_lookup_list)
		for lookup in cell_lookup_list:
			lookup_cell = board_state[lookup]
			if lookup_cell['colour'] == cell['colour']:
				score += 100
			if lookup_cell['dot'] == cell['dot']:
				score += 500
			if lookup_cell['colour'] == cell['colour']	and lookup_cell['dot'] == cell['dot']:
				score *=-2
				
		cell_lookup_1 = index - 1*2
		cell_lookup_2 = index + 1*2
		cell_lookup_3 = index - 8*2
		cell_lookup_4 = index + 8*2
		cell_lookup_5 = index - 9*2
		cell_lookup_6 = index - 7*2
		cell_lookup_7 = index + 7*2
		cell_lookup_8 = index + 9*2
		cell_lookup_list = [cell_lookup_1, cell_lookup_2, cell_lookup_3, cell_lookup_4, cell_lookup_5, cell_lookup_6, cell_lookup_7, cell_lookup_8]
		cell_lookup_list = filter(lambda x: (x < 8*12 and x >= 0), cell_lookup_list)
		for lookup in cell_lookup_list:
			lookup_cell = board_state[lookup]
			if lookup_cell['colour'] == cell['colour']:
				score -= 50
			if lookup_cell['dot'] == cell['dot']:
				score += 25

		cell_lookup_1 = index - 1*1
		cell_lookup_2 = index + 1*1
		cell_lookup_3 = index - 8*1
		cell_lookup_4 = index + 8*1
		cell_lookup_5 = index - 9*1
		cell_lookup_6 = index - 7*1
		cell_lookup_7 = index + 7*1
		cell_lookup_8 = index + 9*1
		cell_lookup_list = [cell_lookup_1, cell_lookup_2, cell_lookup_3, cell_lookup_4, cell_lookup_5, cell_lookup_6, cell_lookup_7, cell_lookup_8]
		cell_lookup_list = filter(lambda x: (x < 8*12 and x >= 0), cell_lookup_list)
		for lookup in cell_lookup_list:
			lookup_cell = board_state[lookup]
			if lookup_cell['colour'] == cell['colour']:
				score -= 10
			if lookup_cell['dot'] == cell['dot']:
				score += 5

		return score