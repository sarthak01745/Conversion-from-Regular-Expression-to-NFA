class State:
    def __init__(self):
        self.transitions = {}

class NFA:
    def __init__(self, start, end):
        self.start = start
        self.end = end

def symbol_nfa(symbol):
    start = State()
    end = State()
    start.transitions[symbol] = [end]
    return NFA(start, end)

def concat(nfa1, nfa2):
    nfa1.end.transitions['ε'] = [nfa2.start]
    return NFA(nfa1.start, nfa2.end)

def union(nfa1, nfa2):
    start = State()
    end = State()
    start.transitions['ε'] = [nfa1.start, nfa2.start]
    nfa1.end.transitions['ε'] = [end]
    nfa2.end.transitions['ε'] = [end]
    return NFA(start, end)

def kleene(nfa):
    start = State()
    end = State()
    start.transitions['ε'] = [nfa.start, end]
    nfa.end.transitions['ε'] = [nfa.start, end]
    return NFA(start, end)

def postfix(regex):
    precedence = {'+':1, '.':2, '*':3}
    output = ""
    stack = []

    for c in regex:
        if c.isalnum():
            output += c
        elif c == '(':
            stack.append(c)
        elif c == ')':
            while stack[-1] != '(':
                output += stack.pop()
            stack.pop()
        else:
            while stack and precedence.get(stack[-1],0) >= precedence[c]:
                output += stack.pop()
            stack.append(c)

    while stack:
        output += stack.pop()
    return output

regex = "a+b"
post = postfix(regex)

stack = []

for c in post:
    if c.isalnum():
        stack.append(symbol_nfa(c))
    elif c == '.':
        b = stack.pop()
        a = stack.pop()
        stack.append(concat(a, b))
    elif c == '+':
        b = stack.pop()
        a = stack.pop()
        stack.append(union(a, b))
    elif c == '*':
        a = stack.pop()
        stack.append(kleene(a))

final_nfa = stack.pop()

print("Regular Expression:", regex)
print("NFA constructed successfully")
