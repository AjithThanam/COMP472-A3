
def main():
    str_input = "7 3 1 4 2 3"
    #print(parse_input(str_input))
    
    #print(first_move(8))

    #print(possible_tokens(2, [1,3,5,6,7,8]))
   
    #print(get_remaining_tokens(9,[2,1,4,3]))

# convert input string to a tuple
def parse_input(inputStr):
    #parses string input and returns array of integers
    parsed_input = list(map(int, inputStr.split(" ")))

    num_tokens = parsed_input[0]
    num_taken_tokens = parsed_input[1]

    #Handles wether there have been any tokens that were taken
    if num_taken_tokens != 0:
        list_taken_tokens = list(parsed_input[2:len(parsed_input) - 1])
    else:
        list_taken_tokens = []

    depth = parsed_input[len(parsed_input)-1]

    return num_tokens, num_taken_tokens, list_taken_tokens, depth

#provides a list of potential tokens to pick from on the first move
def first_move(num_tokens):
    odd_tokens = []
    if isinstance(num_tokens/2, float):
        upper_limit = int(num_tokens/2) + 1
    else:
        upper_limit = (num_tokens/2) - 1

    for num in range(1, upper_limit):
        if num % 2 != 0:
            odd_tokens.append(num)

    return odd_tokens

#provides a list of potential tokens to pick from, based on what has already been picked
def get_possible_tokens(last_token, remaining_tokens):
    possible_tokens = []

    for token in remaining_tokens:
        if last_token % token == 0 or  token % last_token == 0:
            possible_tokens.append(token)

    if len(possible_tokens) == 0:
        return False
    else:
        return possible_tokens

#determines whos turn it is based on how many tokens have been taken
def get_players_turn(taken_tokens):
    if len(taken_tokens) == 0 or len(taken_tokens) % 2 == 0 :
        return "max"
    else:
        return "min"

#return a list of remaining tokens based on what has been taken 
def get_remaining_tokens(num_tokens, taken_tokens):
    remaining_tokens = []

    for num in range (1, num_tokens + 1):
        if num not in taken_tokens:
            remaining_tokens.append(num)

    return remaining_tokens


if __name__ == '__main__':
    main()
     
