class State:
    taken_tokens: []
    num_tokens: None

    def __init__(self, taken_tokens, num_tokens):
        self.taken_tokens = taken_tokens
        self.num_tokens = num_tokens
