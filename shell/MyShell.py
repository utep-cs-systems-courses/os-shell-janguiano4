#Joel Anguiano
#Lab1 p.1

import os
import sys
import re
from lab0 import my_getLine 

str1 = "$"

while 1:
    os.write(1, str1.encode())
    userInput = my_getLine()
    if len(userInput) == 0:
        break
    if userInput == "exit":
        sys.exit(1)

    tokens = userInput.split()
    rc = os.fork()
    
    if rc < 0:
       os.write(2,("Fork failed").encode())
       sys.exit(1)

    elif rc == 0:
       for dir in re.split(":",os.environ['PATH']):
           program = "%s/%s" % (dir, tokens[0])
           try:
               os.execve(program,tokens,os.environ)
           except FileNotFoundError:
               pass
       os.write(2,("Failed").encode())
       sys.exit(1)

    else:
        wait = os.wait()

           
           
