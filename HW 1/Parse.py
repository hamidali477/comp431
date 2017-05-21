#! ~/comp431/submissions/HW1
import fileinput

"""
-Function: Recursively parses mail-from command and returns error messages when errors
    in syntax are found
-Arguments: The string of the command taken from the file input at the command line
"""
def parseMailCommand(command):
    tokens = tokenizeCommand(command)
    print command.rstrip('\n')          # removes trailing newline character for correct output format
    if(tokens[0] != "MAIL"):
        print "ERROR -- mail-from-cmd"
        return 0
    if(tokens[1] != "FROM:"):
        print "ERROR -- mail-from-cmd"
        return 0
    if(parsePath(tokens[2]) == 0): return 0
    else: print "Sender ok"

# Parses path component of mail-from command
def parsePath(path):
    if (path[0] != "<" or path[len(path)-1]) != ">":
        print "ERROR -- path"
        return 0
    mailbox = path[1:]
    if parseMailbox(mailbox) == 0: return 0

# Parses mailbox component of mail-from command
def parseMailbox(mailbox):
    special = ["<", ">", "(" , ")" , "[" , "]" , "\\" , "." , "," , ";" , ":" , "\"", " "]
    position = 0
    hasLocalPart = False
    for char in mailbox:
        if char in special:
            print "ERROR -- mailbox"
            return 0
        else:
            hasLocalPart = True
        if char == "@" and hasLocalPart:
            break
        position+=1

    domain = mailbox[position:]
    if domain[0] != "@":
        print "ERROR -- mailbox"
        return 0
    if (parseDomain(domain[1:len(domain)-1]) == 0): return 0

# Parses domain component of mail-from command
def parseDomain(domain):
    for char in domain:
        if char.isalpha() != True and char.isdigit() != True:
            if char != ".":
                print "ERROR -- domain"
                return 0

"""
-Function: Tokenizes string of command that is input and returns as an array of
    tokens ready to be parsed
-Arguments: The string of the command taken from the file input at the command line - provided by argument passed to 'parseMailCommand()'
"""
def tokenizeCommand(command):
    index = 0
    tokens = [None]*3

    # Tokenize 'MAIL'
    for char in command:
        if char != " ":
            index+=1
        else: break
    tokens[0] = command[0:index]

    # Remove 'MAIL' from string
    command = command[index:]
    index = 0
    startFrom = 0

    # Tokenize 'FROM:'
    for char in command:
        if char == " ":
            index+=1
        elif char.isalpha() and command[index-1] == " ":
            startFrom = index
            index+=1
        elif char == ":":
            break
        else: index+=1
    tokens[1] = command[startFrom:index+1]

    # Remove "FROM:" from string
    command = command[index+1:]
    index = 0

    #Tokenize path/mailbox
    startPath = 0
    for char in command:
        if char == " ":
            index+=1
        elif char == "<" and command[index-1] == " ":
            startPath = index
            index+=1
        elif char == ">": break
        else: index+=1

    tokens[2] = command[startPath:index+1]

    return tokens

"""
Retrieving file input at command line and feeding it to the program line-by-line (e.g. command-by-command)
"""
# command = raw_input("Enter SMTP command: ")
# parseMailCommand(command);

for line in fileinput.input():
    parseMailCommand(line);
