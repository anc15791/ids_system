'''
Define Common functions to use in other places
'''

# return contents of a file as a list with new line as separator.
def readFile(fname):
    with open(fname) as f:
        content = f.readlines()
    return content
