#Joel Anguiano
#CS4375: OS
#3 methods

from os import read #from os library import read method

next = 0
limit = 0

#This method calls read to fill a buffer, and gets one char at at time
def my_getChar(): #define = creating method : use method, loops, tryCatch
    global next, limit #initializing 2 variables

    if next == limit:
        next = 0
        limit = read(0,1000) #

        if limit == 0:
            return "EOF"

    if next < len(limit) -1: #Check to make sure limit[next] wont go out of bounds. 
        c = chr(limit[next])#converting from ascii to char
        next += 1
        return c

    else:
        return "EOF"
    
def my_getLine():
    global next
    global limit
    line = ""
    char = my_getChar()
    while (char != '' and char != "EOF"):
        line += char
        char = my_getChar()
    next = 0
    limit = 0
    return line

def my_readLines():
    numLines = 0
    inLine = my_getLine()
    while len(inLine):
        numLines += 1
        print(f"### Line {numLines}: <{str(inLine)}> ###\n")
        inLine = my_getLine()
    print(f"EOF after {numLines}\n")

    

 
