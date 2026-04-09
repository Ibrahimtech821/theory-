class NFA:
    def __init__(self):
        self.transitions = []  
        self.state_count = 0

    def new_state(self):
        # create states q0, q1, etc
        state_label = f"q{self.state_count}"
        self.state_count += 1
        return state_label

    def add_transition(self, s1, char, s2):
        # perform transition from s1 to s2 with char as input
        self.transitions.append((s1, char, s2))

class Fragment:
    def __init__(self, start, accept):
        # creating starting and acceptoing states
        self.start = start
        self.accept = accept

def build_nfa(postfix_tokens):
    nfa = NFA()
    stack = []
    epsilon = 'ε'

    for token in postfix_tokens:
        # single symbols as input
        if token not in {'*', '.', '|', '+', '?'}:
            s_start = nfa.new_state()
            s_end = nfa.new_state()
            nfa.add_transition(s_start, token, s_end)
            stack.append(Fragment(s_start, s_end))

        # concatenation (and)
        elif token == '.':
            if len(stack) < 2: 
                raise ValueError("Invalid regex: not enough operands for '.'") # Safety check for stack depth
            frag_b = stack.pop() 
            frag_a = stack.pop() 
            nfa.add_transition(frag_a.accept, epsilon, frag_b.start)
            stack.append(Fragment(frag_a.start, frag_b.accept))

        # union (or)
        elif token == '|':
            if len(stack) < 2: 
                raise ValueError("Invalid regex: not enough operands for '.'")
            frag_b = stack.pop()
            frag_a = stack.pop()
            s_start = nfa.new_state()
            s_end = nfa.new_state()
            
            nfa.add_transition(s_start, epsilon, frag_a.start)
            nfa.add_transition(s_start, epsilon, frag_b.start)
            nfa.add_transition(frag_a.accept, epsilon, s_end)
            nfa.add_transition(frag_b.accept, epsilon, s_end)
            stack.append(Fragment(s_start, s_end))
            
        # kleene Star
        elif token == '*':
            if len(stack) < 1:
                raise ValueError("Invalid regex: not enough operands for '.'")

            frag = stack.pop()
            s_start = nfa.new_state()
            s_end = nfa.new_state()

            nfa.add_transition(s_start, epsilon, frag.start)
            nfa.add_transition(s_start, epsilon, s_end)
            nfa.add_transition(frag.accept, epsilon, frag.start)
            nfa.add_transition(frag.accept, epsilon, s_end)

            stack.append(Fragment(s_start, s_end))


        # plus operator
        
        elif token == '+':
            if len(stack) < 1:
                raise ValueError("Invalid regex: not enough operands for '.'")

            frag = stack.pop()
            s_start = nfa.new_state()
            s_end = nfa.new_state()

            nfa.add_transition(s_start, epsilon, frag.start)
            nfa.add_transition(frag.accept, epsilon, frag.start)
            nfa.add_transition(frag.accept, epsilon, s_end)

            stack.append(Fragment(s_start, s_end))

        elif token == '?':
            if len(stack) < 1:
                raise ValueError("Invalid regex: not enough operands for '.'")

            frag = stack.pop()
            s_start = nfa.new_state()
            s_end = nfa.new_state()

            nfa.add_transition(s_start, epsilon, frag.start)
            nfa.add_transition(frag.accept, epsilon, s_end)
            nfa.add_transition(s_start, epsilon, s_end)

            stack.append(Fragment(s_start, s_end))

    if stack:
        return nfa, stack.pop()
    else:
        return nfa, None

