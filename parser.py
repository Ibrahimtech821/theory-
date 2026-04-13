def regex_to_tokens(regex):
    tokens = []
    i = 0
    while i < len(regex):
        c = regex[i]
        if c in {'(', ')', '|', '*', '+', '?'}:
            tokens.append(c)
            i += 1
        elif c == '[': ## as it will first check if [  if there it will take next i in j and then loop and then put a-z as one token 
             #class [a-z]
            j = i + 1
            while j < len(regex) and regex[j] != ']':
                j += 1
            if j >= len(regex):
                raise ValueError("Unclosed character class")
            tokens.append(regex[i:j+1])  
            i = j + 1
        else:
            tokens.append(c)
            i += 1
    return tokens

def add_concatenation(tokens):
    result = []
    for i in range(len(tokens)):
        result.append(tokens[i])
        if i < len(tokens) - 1:
            if (tokens[i] not in {'(', '|'} and 
                tokens[i+1] not in {'|', '*', '+', '?', ')'}):
                result.append('.')
    return result

def to_postfix(tokens):
    ##Shunting Yard algorithm to make put the operator precdence as when we will do nfa builder so it will help us in making 
    ## operands have there operators correctly in order
    precedence = {'*': 3, '+': 3, '?': 3, '.': 2, '|': 1}
    output = []
    stack = []
    
    for t in tokens:
        if t not in precedence and t not in {'(', ')'}:
            # Operand
            output.append(t)
        elif t == '(':
            stack.append(t)
        elif t == ')':
            while stack and stack[-1] != '(': ## check if the stack is true and also the last is not (
                output.append(stack.pop()) # if this ) is enter then keep pop the operators from the stack
                #and put it to output
            stack.pop()  # it will remove  '('
        else:
            # operator as here it will check percende as if percednce of new input is lower than what in stack 
            # then remove what in stack and put it in output and if more than or empty put it in tack 
            while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence[t]:
                output.append(stack.pop())
            stack.append(t)
    
    while stack:
        output.append(stack.pop()) ## as if anuthing in stack put it in last 
    
    return output

def parse_regex(regex):
    tokens = regex_to_tokens(regex)
    tokens = add_concatenation(tokens)
    postfix = to_postfix(tokens)
    return postfix


if __name__ == "__main__":
    regex = "a[b-z]*|(d|e)"    

    tokens = regex_to_tokens(regex)
    concat = add_concatenation(tokens)
    postfix = to_postfix(concat)
    print(f"Regex: {regex}")
    print(f"TOKENS: {tokens}")
    print(f"CONCAT: {concat}")
    print(f"POSTFIX: {postfix}")