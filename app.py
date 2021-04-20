import math
import copy
from node import Node
from state import State


evaluated_counter = 0
depth_counter = 0
visited_counter = 1

def main():
	str_input = "3 1 1 1"

	num_tokens, num_taken_tokens, list_taken_tokens, depth, start_token = parse_input(str_input)
	start_state = State(list_taken_tokens, num_tokens)
	start_node = Node(start_token, None, 0, None, -math.inf, math.inf, [], start_state)
	players_turn = get_players_turn(list_taken_tokens)
	response = run_ab_algo(start_node, start_state, depth, players_turn, -math.inf, math.inf)
	count_visited(start_node)
	output_results(start_node, response)

def count_visited(node):
	global visited_counter

	if(len(node.children) == 0):
		return

	for child in node.children:
		if(child.score != None):
			visited_counter += 1
			count_visited(child)
		
def run_ab_algo(node, state, depth, players_turn, alpha, beta):
	if depth == 0:
		max_depth = math.inf
	else:
		max_depth = depth

	global evaluated_counter
	global depth_counter
	
	children = generate_children(node, node.state)
	
	if node.depth == max_depth or len(children) == 0:
		evaluated_counter += 1
		if node.depth > depth_counter:
			depth_counter = node.depth
		return get_score(node, node.state)

	if players_turn:
		max_val = -math.inf	
		for child in children:
			temp_val = run_ab_algo(child, child.state, depth, not players_turn, alpha, beta)
			max_val = max(max_val, temp_val)
			alpha = max(alpha, temp_val)
			child.score = temp_val
			if beta <= alpha:
				break
		return max_val
	else:
		min_val = +math.inf	
		for child in children:
			temp_val = run_ab_algo(child, child.state, depth, not players_turn, alpha, beta)
			min_val = min(min_val, temp_val)
			beta = min(beta, temp_val)
			child.score = temp_val
			if beta <= alpha:
				break
		return min_val
		
def output_results(node, score):
	global evaluated_counter
	global depth_counter
	global visited_counter
	smallest_num = 100

	branching_factor = round(((visited_counter-1)/(visited_counter-evaluated_counter)), 1)

	for child in node.children:
		if child.score == score and child.value < smallest_num:
			smallest_num = child.value

	print("Best Move: " + str(smallest_num))
	print("Score: " + str(score))
	print("Visited Counter: " + str(visited_counter))
	print("Evaluated Counter: " + str(evaluated_counter))
	print("Max Depth: " + str(depth_counter))
	print("Avg Effective Branching Factor: " + str(branching_factor))

# convert input string to a tuple
def parse_input(inputStr):
	# parses string input and returns array of integers
	parsed_input = list(map(int, inputStr.split(" ")))

	num_tokens = parsed_input[0]
	num_taken_tokens = parsed_input[1]

	# Handles wether there have been any tokens that were taken
	if num_taken_tokens != 0:
		list_taken_tokens = list(parsed_input[2:len(parsed_input) - 1])
		start_token = parsed_input[len(parsed_input)-2]
		print(start_token)
	else:
		list_taken_tokens = []
		start_token = None

	depth = parsed_input[len(parsed_input)-1]

	return num_tokens, num_taken_tokens, list_taken_tokens, depth, start_token

# provides a list of potential tokens to pick from on the first move
def first_move(num_tokens):
	odd_tokens = []
	if num_tokens % 2 != 0:
		upper_limit = int(num_tokens/2) + 1
	else:
		upper_limit = int(num_tokens/2) - 1

	for num in range(1, upper_limit):
		if num % 2 != 0:
			odd_tokens.append(num)

	return odd_tokens

# provides a list of potential tokens to pick from, based on what has already been picked
def get_possible_tokens(last_token, remaining_tokens):
	possible_tokens = []

	for token in remaining_tokens:
		if last_token % token == 0 or  token % last_token == 0:
			possible_tokens.append(token)

	if len(possible_tokens) == 0:
		return False
	else:
		return possible_tokens

# determines whos turn it based on how many tokens have been taken
def get_players_turn(taken_tokens):
	if len(taken_tokens) == 0 or len(taken_tokens) % 2 == 0 :
		return True
	else:
		return False

# return a list of remaining tokens based on what has been taken 
def get_remaining_tokens(num_tokens, taken_tokens):
	remaining_tokens = []

	for num in range (1, num_tokens + 1):
		if num not in taken_tokens:
			remaining_tokens.append(num)

	return remaining_tokens

# returns if a number is prime or not
def isPrime(number):
	result = True

	if number == 1:
		result = False
	elif number > 1:
		for i in range(2, number):
			if (number % i) == 0 & number != i:
				result = False
				break
	

	return result

def getMaxPrime(number):       
	maxPrime = -1
	
	while number % 2 == 0:
		maxPrime = 2
		number >>= 1
		  
	for i in range(3, int(math.sqrt(number)) + 1, 2):
		while number % i == 0:
			maxPrime = i
			number = number / i
	 
	if number > 2:
		maxPrime = number
	  
	return int(maxPrime)

def generate_children(parent_node, state):
	if(parent_node.value == None):
		possible_moves = first_move(state.num_tokens)
		nodes = create_nodes(parent_node, possible_moves, state)
	else:
		tokens_remaining = get_remaining_tokens(state.num_tokens, state.taken_tokens)
		possible_moves = get_possible_tokens(state.taken_tokens[len(state.taken_tokens)-1], tokens_remaining)
		if possible_moves != False:
			nodes = create_nodes(parent_node, possible_moves, state)
		else:
			return []
	
	parent_node.children = nodes

	return nodes

def create_nodes(parent_node, moves_list, state):
	nodes = []
	for move in moves_list:
		new_state = copy.deepcopy(state)
		new_state.taken_tokens.append(move)
		node = Node(move, parent_node, parent_node.depth+1, None, -math.inf, math.inf, [], new_state)
		nodes.append(node)
	
	return nodes

def get_score(node, state):

	if len(state.taken_tokens) % 2 == 0:
		turn = 'min'
	else:
		turn = 'max'
		
	children = generate_children(node, state)

	if len(children) == 0:
		if turn == 'max':
			node.score = 1.0
		else:
			node.score = -1.0

	elif 1 not in state.taken_tokens:
		node.score = 0

	elif node.parent.value == 1:
		num_successor = len(node.parent.children)

		if (num_successor % 2) == 0:
			node.score = -0.5
		else:
			node.score = 0.5
		
		if(turn == "min"):
			node.score = -1 * node.score
			
	elif isPrime(node.parent.value):
		multiples = num_multiples(node.parent, node.parent.value)
		
		if multiples % 2 == 0:
			node.score = -0.7
		else:
			node.score = 0.7
		
		if(turn == "min"):
			node.score = -1 * node.score
	
	else:
		max_divider = getMaxPrime(node.parent.value)
		
		multiples = num_multiples(node.parent, max_divider)

		if multiples % 2 == 0:
			node.score = -0.6
		else:
			node.score = 0.6
		
		if(turn == "min"):
			node.score = -1 * node.score
	
	return node.score
						
def num_multiples(node, prime):
	num_multiples = 0

	if len(node.children) != 0:
		for child in node.children:
			if prime % child.value == 0 or child.value % prime == 0:
				num_multiples += 1
	
	return num_multiples
		
if __name__ == '__main__':
	main()
	 
