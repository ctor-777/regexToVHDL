
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

    for index, token in enumerate(regex):
        if token == "[":
            begin = index
            end = regex.find("]", begin)
            if end == -1:
                raise ValueError("square braquets opened but never closed")

            alternative = "|".join(parse_concat(regex[begin+1:end]))
            print("alternative: " + alternative)

            regex = regex[:begin] + "(" + alternative + ")" + regex[end+1:]


    return regex

def parse_concat(concat):
    parsed_concat = ""
    for index, token in enumerate(concat):
        if token == "-":
            first = concat[index-1]
            last = concat[index+1]
            range = get_range(first, last)
            parsed_concat += range
    return parsed_concat


test = "abcd[a-dA-D]fghz[a-e1-3]"
print(test)
print(parse_regex(test))
