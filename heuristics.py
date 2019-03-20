
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
