import math
import copy
from node import Node
from state import State


def main():
	str_input = "7 1 1 2"
	# node = Node(1, None, 0, None, math.inf, -math.inf, [], [])
	# parent_state = State([1], 3)
	# child = Node(5, node, 0, None, math.inf, -math.inf, [])
	# state = State([1,5],7)
	# children = generate_children(node, parent_state)

	num_tokens, num_taken_tokens, list_taken_tokens, depth = parse_input(
		str_input)
	start_state = State(list_taken_tokens, num_tokens)
	# parent_node = Node(list_taken_tokens[len(list_taken_tokens) - 1], None, 0, None,math.inf, -math.inf, [])
	start_node = Node(1, None, 0, None, math.inf, -math.inf, [], start_state)
	players_turn = get_players_turn(list_taken_tokens)
	run_ab_algo(start_node, start_state, depth, players_turn)

	# print(parse_input(str_input))
	# print(first_move(8))
	# print(possible_tokens(2, [1,3,5,6,7,8]))
	# print(get_remaining_tokens(9,[2,1,4,3]))


def run_ab_algo(start_node, state, depth, players_turn):
	open_stack = []
	closed_stack = []
	parent_stack = []
	bottom_reached = False
	bubbling_up = False
	move = 0

	if depth == 0:
		max_depth = math.inf
	else:
		max_depth = depth

	open_stack.append(start_node)

	while len(open_stack) > 0:
		if len(closed_stack) == 0:
			current_node = open_stack.pop()
			closed_stack.append(current_node)
		else:
			closed_stack.append(current_node)
			current_node = open_stack.pop()

		while current_node.depth < max_depth:

			children = generate_children(current_node, current_node.state)

			if(len(children) == 0):
				break

			for child in children:
				open_stack.append(child)
				
			closed_stack.append(current_node)
			parent_stack.append(current_node)
			current_node = open_stack.pop()
		
		if current_node.depth == max_depth or len(children) == 0:
			bottom_reached = True

		if bottom_reached:
			get_score(current_node, current_node.state)
			if get_players_turn(current_node.state.taken_tokens):
				if current_node.parent.score == None:
					current_node.parent.score = current_node.score
					move = current_node.value
				elif current_node.score < current_node.parent.score:
					current_node.parent.score = current_node.score
					move = current_node.value
			else:
				if current_node.parent.score == None:
					current_node.parent.score = current_node.score
					move = current_node.value
				elif current_node.score > current_node.parent.score:
					current_node.parent.score = current_node.score
					move = current_node.value

	if len(open_stack) == 0: 
		
		while len(parent_stack) != 1:	  
			parent_node = parent_stack.pop()

			if get_players_turn(parent_node.state.taken_tokens):
				if parent_node.parent.score == None:
					parent_node.parent.score = parent_node.score
					move = parent_node.value
				elif parent_node.score < parent_node.parent.score:
					parent_node.parent.score = parent_node.score
					move = parent_node.value
			else:
				if parent_node.parent.score == None:
					parent_node.parent.score = parent_node.score
					move = parent_node.value
				elif parent_node.score > parent_node.parent.score:
					parent_node.parent.score = parent_node.score
					move = parent_node.value
	
	parent_node = parent_stack.pop()
	print(parent_node.score)
	get_best_move(parent_node)
	

def get_best_move(node):
	smallest_num = 100
	for child in node.children:
		if child.score == node.score and child.value < smallest_num:
			smallest_num = child.value

	print(smallest_num)

# convert input string to a tuple
def parse_input(inputStr):
	# parses string input and returns array of integers
	parsed_input = list(map(int, inputStr.split(" ")))

	num_tokens = parsed_input[0]
	num_taken_tokens = parsed_input[1]

	# Handles wether there have been any tokens that were taken
	if num_taken_tokens != 0:
		list_taken_tokens = list(parsed_input[2:len(parsed_input) - 1])
	else:
		list_taken_tokens = []

	depth = parsed_input[len(parsed_input)-1]

	return num_tokens, num_taken_tokens, list_taken_tokens, depth

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

def getOutput():
	print("Move: ")
	print("Value: ")
	print("Number of Nodes Visited: ")
	print("Number of Nodes Evaluated: ")
	print("Max Depth Reached: ")
	print("Avg Effective Branching Factor: ")

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
		node = Node(move, parent_node, parent_node.depth+1, None, math.inf, -math.inf, [], new_state)
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
	 
