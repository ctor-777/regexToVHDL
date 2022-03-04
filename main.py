

def get_range(first, last):
    """
    return a range of letters of the alphabet given the first and last one.

    parameters:
        first (Char): first character in range
        last  (Char): last character in range

    returns:
        Str: the characters in between the first and last characters
    """
    ranges = "abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRSTUVWXY0123456789"

    return ranges[ranges.find(first):ranges.find(last)+1]


def parse_regex(regex):
    """
    return a regex string with the expressions '[]' substituted by the union of
    the elements inside of it in the form '(element1 | element2 | ... )'

    parameters:
        regex (str): regular expression to adjust

    returns:
        Str: adjusted regular expression

    raise:
        ValueError: if the expression given has unclosed squared braquets,
                    ex: "[a-b"
    """
    begin = regex.find("[")
    if begin != -1:

        end = regex.find("]", begin)

        if end == -1 or regex.find("[", begin+1, end) != -1:
            raise ValueError("square braquets opened but never closed")

        alternative = "|".join(parse_range(regex[begin+1:end]))

        regex = regex[:begin] + "(" + alternative + ")" + parse_regex(regex[end+1:])

    return regex

def parse_range(potential_range):
    """
    parse the ranges of a regular expression of the form [first-last] into the form
    [first...last] where the triple dot represent all the character in between first and
    last.

    prameters:
        potential_range (str): string of posible ranges, withour square braquets

    returns:
        Str: adjusted range
    """
    parsed_range = ""
    for index, token in enumerate(potential_range):
        if potential_range[index-1] != "-" and potential_range[index+1] != "-" and token != "-":
            parsed_range += token
        if token == "-":
            first = potential_range[index-1]
            last = potential_range[index+1]
            range = get_range(first, last) #TODO change name of that variable
            parsed_range += range
    return parsed_range

def get_parenthesis(regex):
    stack = -1
    for index, token in enumerate(reversed(regex)):
        if token == ")":
            stack += 1
        elif token == "(":
            if stack:
                stack -= 1
            else:
                return regex[-(index+1):]

def parse_iteration(regex):
    """
    adjust all iteration expressions of a regex expression into alternative, concatenation and
    klenee star expressions.

    parameters:
        regex (Str): regular expression to be adjusted

    returns:
        Str: adjusted regular expression

    raises:
        ValueError: if the expression has unclosed curly braquets
                    ex: "aba{5"
                    if the expression doesn't provide any value inside of
                    the curly braquets.
                    ex: "aba{}" or "aba{,}"
                    if the values provided inside the curly braquets are
                    not valid.
                    ex: "aba{five}"
    """
    begin = regex.find("{")
    end = regex.find("}")

    #if it find a opening curly braquet means there is a quntifier expression
    if begin != -1:
        if regex[begin-1] == ")":
            expression = get_parenthesis(regex[:begin])
        else:
            expression = regex[begin-1]


        #if it doesn't find a closing curly braquet means the firs opening braquet is unclosed, raise an error
        if end == -1:
            raise ValueError("curly braquets opened but never closed")

        #tries to find a come between the braquets
        coma_pos = regex.find(",", begin, end)

        #if it desn't find a coma means the expression is of the form {n}
        if coma_pos == -1:
            #try to find the value n in {n}, raise an error if it fails
            try:
                quant = int(regex[begin+1:end])
            except:
                raise ValueError("quantity provided is not correct")

            #if it finds the value n takes the expression until the first bracket, add
            #a n-1 (there's already one before the braquet) times multiplied value and
            #process the rest of the expression recursively
            regex = regex[:begin] + (quant-1) * expression + parse_iteration(regex[end+1:])

        #if it found a coma means the expression is of the form {min,max}
        else:
            #if theres no value after or before the coma until the braquet raise an error
            if regex[coma_pos+1] == "}" and regex[coma_pos-1] == "{":
                raise ValueError("no min or max value provided")

            #if there's no value after the coma means the expression is of the form {min,}
            if regex[coma_pos+1] == "}":
                #tries to find the value, if it is not valid raises an exception
                try:
                    min_value = int(regex[begin+1:coma_pos])
                except:
                    raise ValueError("minimun value provided is not correct")

                #if it finds the value, takes the expression until the opening braquet, adds a min-1
                #(same reason as before) times multipied value plus a klenee star and process
                #the rest of the expression recursively
                regex = regex[:begin] + min_value * expression + "*" + parse_iteration(regex[end+1:])

            #if there's no value before the coma, but there is after it (is an else statement), the expression
            #is of the form {,max}
            elif regex[coma_pos-1] == "{":
                #tries to find the value after the coma, if it is not valid raises and exception
                try:
                    max_value = int(regex[coma_pos+1: end])
                except:
                    raise ValueError("max value provided is not correct")

                #if it find the value, takes the expression until the opening of the braquet, and adjust the value
                #in a alternative form (from a{,3} to (|a|aa|aaa)) and process the rest of the expression recursively
                regex = regex[:begin-1] + max_to_alternative(expression, max_value) + parse_iteration(regex[end+1:])

            #if there's value after and before the coma the expression is of the form {min,max}
            else:
                #tries to find the max and min values, if any of both is invalid raises an exception
                try:
                    min_value = int(regex[begin+1:coma_pos])
                    max_value = int(regex[coma_pos+1:end])
                except:
                    raise ValueError("min or max value provided is not correct")

                #if it finds the values takes the expression until the opening braquet, add a min-1 multipied
                #value, adds a modified to alternative max times value (from a{2,4} to aa(|a|aa)) and process the rest
                #of the expression recursively
                regex = regex[:begin-1] + min_value * expression + max_to_alternative(expression, max_value-min_value) + parse_iteration(regex[end+1:])
    return regex

def max_to_alternative(expression, max_value):
    converted_expression = "("
    for i in range(max_value+1):
        converted_expression += expression * (i)
        if i != max_value and i != 0:
            converted_expression += "|"
        print(str(i) + "   " + str(converted_expression))
    return converted_expression + ")?"


def shunting_yard_regex(regex):
    precedence = {
        "(": 0,
        "|": 1,
        "_": 2,
        "*": 3,
        "?": 3
    }
    operators = []
    final = []
    for token in regex:
        if token in precedence or token == ")":
            if operators:
                if token == ")":
                    for index in range(len(operators)):
                        if operators[-1] != "(":
                            final.append(operators.pop())
                        else:
                            operators.pop()
                            break
                elif token == "(":
                    operators.append(token)
                elif precedence[token] > precedence[operators[-1]]:
                    operators.append(token)
                else:
                    for index in range(len(operators)):
                        if precedence[operators[-1]] >= precedence[token]:
                            final.append(operators.pop())
                        else:
                            break
                    operators.append(token)
            else:
                operators.append(token)
        else:
            final.append(token)

    if operators:
        for operator in reversed(operators):
            final.append(operator)
    return "".join(final)

def explicit_concat(regex):
    operators = ["?", "|", "*"]
    final = []
    for index, token in enumerate(regex):
        final.append(token)
        if not token in operators and index < len(regex)-1 and token != "(":
             if regex[index+1] not in operators and regex[index+1] != ")":
                final.append("_")
    return "".join(final)
test = "a{5,7}then(abc){5}"
print(test)
print(parse_iteration(test))
