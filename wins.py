#helper fxns to detect wins
def flip_horizontal(result):
    # flip results horizontally to keep track them in a more readable list
    horizontal_values = []
    for value in result.values():
        horizontal_values.append(value)
    # rotate 90 degrees to get text representation of spin in order
    rows, cols = len(horizontal_values), len(horizontal_values[0])
    hvals2 = [[""] * rows for _ in range(cols)]
    for x in range(rows): 
        for y in range(cols):
            hvals2[y][rows - x - 1] = horizontal_values[x][y] #purpose of this is to reverse the order of elements within each row and also to change their positions from the original list to the new list hvals2.
    hvals3 = [item[::-1] for item in hvals2]
    return hvals3

def longest_seq(hit):
    subSeqLength, longest = 1, 1
    start, end = 0,0
    for i in range(len(hit) -1):
        if hit[i] == hit[i + 1] - 1:
            subSeqLength += 1
            if subSeqLength > longest:
                longest = subSeqLength
                start = i+2 - subSeqLength
                end = i + 2
        else:
            subSeqLength = 1
    return hit[start : end]