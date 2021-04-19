from state import State

class Node:
    value: None
    parent: None
    depth: None
    score: None
    a_score: None
    b_score: None
    children: []
    state: None

    def __init__(self, value, parent, depth, score, a_score, b_score, children, state):
        self.value = value
        self.parent = parent
        self.depth = depth
        self.score = score
        self.a_score = a_score
        self.b_score = b_score
        self.children = children
        self.state = state
