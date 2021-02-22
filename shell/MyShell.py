#Joel Anguiano
#CS 4375: Theory of Operating Systems
#Lab1 Shell

import os
import sys
import re
from lab0 import my_getLine 

#Redirection
def redirection(tokens):
    if ">" in tokens:
        os.close(1)
        os.open(tokens[tokens.index('>')+1], os.O_CREAT | os.O_WRONLY) #Open Output
        os.set_inheritable(1,True)
        tokens.remove(tokens[tokens.index('>') + 1])
        tokens.remove('>')

    if "<" in tokens:
        os.close(0)
        os.open(tokens[tokens.index('<')+1], os.O_RDONLY)
        os.set_remove(tokens[tokens.index('<')+1])
        tokens.remove('<')

    for dir in re.split(":", os.environ['PATH']):
        prog = "%s/%s" % (dir,tokens[0])
        try:
            os.execve(prog, tokens, os.environ)
        except FileNotFoundError:
            pass
    os.write(2,("%s: command not found\n" % tokens[0]).encode())
    sys.exit(0)

#Piping
def pipe(tokens):
    left = tokens[0:tokens.index("|")]
    right = tokens[tokens.index("|")+1:]
    
    pr,pw = os.pipe()
    
    rc = os.fork() #Fork off children

    if rc < 0:
        os.write(2,("Fork Failed, returning %d\n" %rc).encode())
        sys.exit(1)
        
    elif rc == 0: #Child 1

        os.close(1) #Disconnect from display
        os.dup(pw) #Connect to input of the pipe
        os.set_inheritable(1,True)
        
        for fd in (pr,pw): #Disconnect extra connections from the pipe
            os.close(fd)

        for dir in re.split(":",os.environ['PATH']): #child1
            program = "%s/%s" % (dir, left[0])
            try:
                os.execve(program,left,os.environ)
            except FileNotFoundError:
                pass
        os.write(2,(left[0]+":command not found\n").encode())
        sys.exit(1)

    

    else: #Child 2
        os.close(0) 
        os.dup(pr) #Connect to output of pipe
        os.set_inheritable(0, True)
        
        for fd in (pw,pr):
            os.close(fd)

        if '|' in right:
            pipe(right)

            
            
        for dir in re.split(":",os.environ['PATH']):
            program = "%s/%s" % (dir, right[0])
            try:
                os.execve(program, right,os.environ) #Replace memory with contents of command
            except FileNotFoundError:
                pass
        os.write(2,(right[0]+":command not found\n").encode()) 
        sys.exit(1)
        
        
        
########################     
while 1:

    if 'PS1' in os.environ:
        os.write(1,(os.environ['PS1']).encode())
    else:
        os.write(1,"$".encode())
        
    userInput = my_getLine()
    tokens = userInput.split()
    
    if len(tokens) == 0: #If input is empty
        break
    if tokens[0] == "exit": #If "exit" is typed, it will exit.
        sys.exit(1)

    if tokens[0] == "cd": #cd command
        if len(tokens) == 1:
            os.chdir("..")
        else:
            os.chdir(tokens[1])
        continue
    
    rc = os.fork()

    background = True

    if '&' in tokens:
        backgroundTask = False
        tokens.remove('&')
    
    if rc < 0:
       os.write(2,("Fork failed").encode())
       sys.exit(1)
        
    elif rc == 0:
        if ">" in tokens or "<" in tokens:
            redirection(tokens)

        elif '|' in tokens:
            pipe(tokens)
            
        else:
            for dir in re.split(":",os.environ['PATH']):
                program = "%s/%s" % (dir, tokens[0])
                try:
                    os.execve(program,tokens,os.environ)
                except FileNotFoundError:
                    pass
            os.write(2,("Failed\n").encode())
            sys.exit(1)
    else:
        if background == True:
            wait = os.wait()

           
           
