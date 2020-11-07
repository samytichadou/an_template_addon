# split string on spaces
def split_string_on_spaces(string, char_limit):

    lines = []

    words = string.split()

    print(words)

    line = ""
    for w in words:
        if len(line) < char_limit:
            line += w + " "
        else:
            line = line[:-1]
            lines.append(line)
            line = w + " "

    if line not in lines:    
        lines.append(line)
        
    return lines