
def split(word):
    return [char for char in word]


toSquare = 'a6'

chars = split(toSquare)

removeSquare = str(chars[0]) + str(int(chars[1]) - 1) 

print (removeSquare)