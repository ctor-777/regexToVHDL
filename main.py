
precedence = {
    "*": 4,
    "+": 4,
    "?": 4,
    "|": 1
}

def get_range(first, last):
    ranges = "abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRSTUVWXY0123456789"

    return ranges[ranges.find(first):ranges.find(last)+1]


def parse_regex(regex):
    begin = regex.find("[")
    if begin != -1:

        end = regex.find("]", begin)

        if end == -1 or regex.find("[", begin+1, end) != -1:
            raise ValueError("square braquets opened but never closed")

        alternative = "|".join(parse_range(regex[begin+1:end]))

        regex = regex[:begin] + "(" + alternative + ")" + parse_regex(regex[end+1:])

    return regex

def parse_range(potential_range):
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

def parse_iteration(regex):
    begin = regex.find("{")
    end = regex.find("}")
    if begin != -1:
        if end == -1:
            raise ValueError("curly braquets opened but never closed")
        coma_pos = regex.find(",", begin, end)
        if coma_pos == -1:
            regex = regex[:begin] + (int(regex[begin+1:end])-1) * regex[begin-1] + parse_iteration(regex[end+1:])
        else:
            if regex[coma_pos+1] == "}":
                regex = regex[:begin] + (int(regex[begin+1:coma_pos])) *regex[begin-1] + "*" + parse_iteration(regex[end+1:])
    return regex
test = "abdc{5}xdxd{2,}"
print(test)
print(parse_iteration(test))
