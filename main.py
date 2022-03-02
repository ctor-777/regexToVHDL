
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

        if end == -1:
            raise ValueError("square braquets opened but never closed")

        alternative = "|".join(parse_range(regex[begin+1:end]))

        regex = regex[:begin] + "(" + alternative + ")" + parse_regex(regex[end+1:])

    return regex

def parse_range(potential_range):
    parsed_range = ""
    for index, token in enumerate(potential_range):
        if token == "-":
            first = potential_range[index-1]
            last = potential_range[index+1]
            range = get_range(first, last) #TODO change name of that variable
            parsed_range += range
    return parsed_range


test = "abcd[a-dA-D]fghz[a-e1-3]"
print(test)
print(parse_regex(test))
