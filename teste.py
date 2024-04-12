class State:
    def __init__(self, is_final=False):
        self.is_final = is_final
        self.transitions = {}

class AFN:
    def __init__(self):
        self.states = []
        self.start_state = None
        self.final_states = []

    def add_state(self, state):
        self.states.append(state)
        if state.is_final:
            self.final_states.append(state)

    def add_transition(self, from_state, to_state, symbol):
        from_state.transitions[symbol] = to_state

def thompson_algorithm(expression):
    stack = []
    for symbol in expression:
        if symbol == 'ε':
            start = State()
            end = State(is_final=True)
            start.transitions[symbol] = end
            stack.append(start)
            stack.append(end)
        elif symbol == '|':
            right = stack.pop()
            left = stack.pop()
            start = State()
            end = State(is_final=True)
            start.transitions['ε'] = left
            start.transitions['ε'] = right
            stack.append(start)
            stack.append(end)
        elif symbol == '*':
            state = stack.pop()
            start = State()
            end = State(is_final=True)
            start.transitions['ε'] = state
            state.transitions['ε'] = end
            stack.append(start)
            stack.append(end)
        elif symbol == '.':
            right = stack.pop()
            left = stack.pop()
            start = State()
            end = State(is_final=True)
            start.transitions['ε'] = left
            left.transitions['ε'] = right
            stack.append(start)
            stack.append(end)
        else:
            state = State(is_final=True)
            start = State()
            start.transitions[symbol] = state
            stack.append(start)
            stack.append(state)
    return stack[0]

# Exemplo de uso
expression = '0|(1(01*(00)*0)*1)*'
afn = AFN()
afn.start_state = thompson_algorithm(expression)
afn.final_states = [afn.start_state]

# Imprimindo o AFN
for state in afn.states:
    print(f"Estado: {'Final' if state.is_final else 'Inicial'}")
    for symbol, next_state in state.transitions.items():
        print(f"Transição: {symbol} -> Estado: {'Final' if next_state.is_final else 'Inicial'}")
