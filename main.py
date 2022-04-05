from string import Template
import sys

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
    one_operand_operators = ["?", "*"]
    final = []
    for index, token in enumerate(regex):
        final.append(token)
        if not token in operators and index < len(regex)-1 and token != "(":
             if regex[index+1] not in operators and regex[index+1] != ")":
                final.append("_")
        elif token in one_operand_operators and index < len(regex)-1:
            if regex[index+1] not in operators:
                final.append("_")
            final.append("_")
    return "".join(final)
test = "a{5,7}[a-b]*"

def full_parse(regex):
    return explicit_concat(parse_iteration(parse_regex(regex)))

main_template = Template("""
library IEEE;
use IEEE.std_logic_1164.all;

entity $name is
  port(
    n: in Character;
    clck, reset, enable: in std_logic;
    m: out std_logic
);
end entity;

architecture behavioral of $name is
    $arch_signals
begin
    signal_0 <= enable;

    $arch_body

    m <= signal_$signal;
end architecture;
""")

concatenation_template = Template("""
$reference: entity work.genseqnfa
    generic map(
        req => \'$character\'
    )
    port map(
        clck => clck,
        reset => reset,
        enable => $input,
        n => n,
        m => $output
    );

""")

end_alternative = Template("""
$output <= $input1 or $input2;
""")

signal_template = Template("""
signal $name: std_logic;
""")

def prefix_to_body(regex, signals = 0, instances = 0, inp = 0):
    print("in postfix_to_body  " + str(regex))
    operators = ["_", "|", "*", "?"]
    two_operand_operators = ["_", "|"]
    one_operand_operators = ["*", "?"]
    if regex[0] in two_operand_operators:
        print("first if")
        first_operand = regex[1]
        second_operand = regex[2]
        if not first_operand in operators:
            if second_operand in operators:
                if regex[0] == "_":
                    evaluation = prefix_to_body(regex[2:], signals+1, instances+1, signals+1)
                    concat = concatenation_template.substitute({"character": first_operand, "input": "signal_" + str(inp), "output": "signal_" + str(signals+1), "reference": "instance_" + str(instances+1)}) + evaluation[0]
                    signals = evaluation[1]
                    instances = evaluation[2]
                    return (concat, signals, instances)
                elif regex[0] == "|":
                    evaluation = prefix_to_body(regex[2:], signals+2, instances+1, inp)
                    alter = conctenation_template.substitute({"character": first_operand, "input": "signal_" + str(inp), "output": "signal_" + str(signals+1)}) + evaluation[0] + end_alternative.substitute({"output": "signal_" + str(signals+2), "input1": "signal_" + str(signals+1), "input2": "signal_" + str(evaluation[1]), "reference": "instance_" + str(instances+1)})
                    signals = evaluation[1]
                    instances = evaluation[2]
                    return (alter, signals, instances)
            elif not second_operand in operators:
                if regex[0] == "_":
                    concat = concatenation_template.substitute({"character": first_operand, "input": "signal_" + str(inp), "output": "signal_" + str(signals+1), "reference": "instance_" + str(instances+1)}) + concatenation_template.substitute({"character": second_operand, "input": "signal_" + str(signals+1), "output": "signal_" + str(signals+2), "reference":  "instance_" + str(instances+2)})
                    instances += 2
                    signals += 2
                    return (concat, signals, instances)
                elif regex[0] == "|":
                    alter = concatenation_template.substitute({"character": first_operand, "input": "signal_" + str(inp), "output": "signal_" + str(signals+1), "reference": "instance_" + str(instances+1)}) + concatenation_template.substitute({"character": second_operand, "input": "signal_" + str(inp), "output": "signal_" + str(signals+2), "reference": "instance_" + str(instances+2)}) + end_alternative.substitute({"output": "signal_" + str(signals+3), "input1": "signal_" + str(signals+1), "input2": "signal_" + str(signals+2)})
                    instances += 2
                    signals += 3
                    return (alter, signals, instances)
        else:
            end_first_operator = evaluate_operators_position(regex[1:])
            second_operand = regex[end_first_operator+1]
            if second_operand in operators:
                if regex[0] == "_":
                    evaluation = prefix_to_body(regex[1:end_first_operator+1], signals, instances, inp)
                    second_evaluation = prefix_to_body(regex[end_first_operator+1:], evaluation[1], evaluation[2], evalutaion[1])
                    concat = evaluation[0] + second_evaluation[0]
                    signals += second_evaluation[1]
                    instances += second_evaluation[2]
                    return (concat, signals, instances)
                elif regex[0] == "|":
                    evaluation = prefix_to_body(regex[1:end_first_operator+1], signals, instances, inp)
                    second_evaluation = prefix_to_body(regex[end_first_operator+1:], evaluation[1], evaluation[2], inp)
                    alter = evaluation[0] + second_evaluation[0] + end_alternative.substitute({"output": "signal_" + str(second_evaluation[1]+1), "input1": "signal_" + str(second_evaluation[1]), "input2": "signal_" + str(evaluation[1]) })
                    return (alter, second_evaluation[1]+1, second_evaluation[2])
            else:
                if regex[0] == "_":
                    evaluation = prefix_to_body(regex[1:end_first_operator+1], signals, instances, inp)
                    concat = evaluation[0] + concatenation_template.substitute({"character": second_operand, "input": "signal_" + str(evaluation[1]), "output": "signal_" + str(evaluation[1]+1), "reference": "instance_" + str(evaluation[2]+1)})
                    signals = evalutaion[1]+1
                    instances = evaluation[2]+1
                    return (concat, signals, instances)
                elif regex[0] == "|":
                    evaluation = prefix_to_body(regex[1:end_first_operator+1], signals, instances, inp)
                    alter = evaluation[0] + concatenation_template.subsitute({"character": second_operand, "input": "signal_" + str(inp), "output": "signal_" + str(evaluation[1]+1), "reference": "instance_" + str(evaluation[2]+1)}) + end_alternative.substitute({"output": "signal_" + str(evaluation[1]+2), "input1": "signal_" + str(evaluation[1]), "input2": "signal_" + str(evauation[1]+1)})
                    return (alter, evaluation[1]+2, evaluation[2]+1)
    elif regex[0] in one_operand_operators:
        operand = regex[1]
        if operand in operators:
            if regex[0] == "*":
                evaluation = postfix_to_body(regex[1:], signals+1, instances, signals+1)
                quant = evaluation[0] + end_alternative.substitute({"output": "signal_" + str(signals+1), "input1": "signal_" + str(inp), "input2": "signal_" + str(evaluation[1])})
                return (quant, evaluation[1], evaluation[2])
            elif regex[0] == "?":
                evaluation = postfix_to_body(regex[1:], signals, instances, inp)
                quant = evaluation[0] + end_alternative.substitute({"output": "signal_" + str(evaluation[1]+1), "input1": "signal_" + str(inp), "input2": "signal_" + str(evaluation[1])})
                return (quant, evaluation[1]+1, evaluation[2])
def evaluate_operators_position(regex, position = 0):
    two_operand_operators = ["_", "|"]
    one_operand_operators = ["*", "?"]
    operators = ["_", "|", "*", "?"]
    if regex[0] in two_operand_operators:
        if regex[1] in operators:
            tmp_pos = evaluate_operators_position(regex[1:])+1
            if regex[tmp_pos] in operators:
                tmp_pos2 = evaluate_operators_position(regex[tmp_pos:])
                return tmp_pos2 + tmp_pos
            else:
                return tmp_pos+position+1
        elif regex[2] in operators:
            tmp_pos = evaluate_operators_position(regex[2:], position+2)
            return tmp_pos
        else:
            return position+3
    elif regex[0] in one_operand_operators:
        if regex[1] in operators:
            temp = evaluate_operators_position(regex[1:])+1
            return temp + position
        else:
            return position+2
    else:
        return position+1

def generate_signals(signals):
    signals_template = Template("""
        signal $signals: std_logic;
    """)

    sign = ""
    for i in range(signals+1):
        if i != signals:
            sign += "signal_" + str(i) + ","
        else:
            sign += "signal_" + str(i)

    return signals_template.substitute({"signals": sign})

def generator(regex, name="generator"):
    print(regex)
    body = prefix_to_body(regex[::-1])
    print(body)
    signals = generate_signals(body[1])
    document = main_template.substitute({"name": name, "arch_signals": signals, "arch_body": body[0], "signal": body[1]})

    with open(name + ".vhdl", "w") as file:
        file.write(document)


parsed = shunting_yard_regex(explicit_concat(parse_regex(parse_iteration(sys.argv[1])))[::-1])
generator(parsed)
#tes(test|tost)t
