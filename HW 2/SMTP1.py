#! ~/comp431/submissions/HW2
import sys
"""
-parseMailCommand(): Recursively parses mail-from command and returns error messages when errors
    in syntax are found
-Parameters: An array of the tokenized command taken from the file input at the command line
"""
def parseMailCommand(tokens):
    sys.stdout.write(command + '\n')
    if(tokens[0] != "MAIL"):
        # print "error in MAIL"
        sys.stdout.write("500 Syntax error: command unrecognized\n")
        return 0
    if(tokens[1] != "FROM:"):
        sys.stdout.write(tokens[1] + "\n")
        # print "error in FROM"
        sys.stdout.write("500 Syntax error: command unrecognized\n")
        return 0
    if(parsePath(tokens[2]) == 0): return 0
    else:
        sys.stdout.write("250 OK\n")
        return parsePath(tokens[2])     # Return mailbox of sender
"""
-parseRcptCommand(): Recursively parses rcpt-to command and returns error messages when errors
    in syntax are found
-Parameters: An array of the tokenized command taken from the file input at the command line
"""
def parseRcptCommand(tokens):
    sys.stdout.write(command + '\n')
    if tokens[0] != "RCPT":
        # print "error in RCPT"
        sys.stdout.write("500 Syntax error: command unrecognized\n")
        return 0
    if(tokens[1] != "TO:"):
        # print "error in TO"
        sys.stdout.write("500 Syntax error: command unrecognized\n")
        return 0
    if(parsePath(tokens[2]) == 0): return 0
    else:
        hasRcpt = True
        sys.stdout.write("250 OK\n")
        return parsePath(tokens[2])     # Return mailbox of recipient
"""
-parseDataCommand(): Parses data command and returns error messages when errors
    in syntax are found. Receives message body from stdin and stores to message array
-Parameters: The string of the command taken from the file input at the command line
"""
def parseDataCommand(command):
    sys.stdout.write(command +'\n')
    if command != "DATA":
        sys.stdout.write("500 Syntax error: command unrecognized\n")
        return 0
    else:
        sys.stdout.write("354 Start mail input; end with <CRLF>.<CRLF>\n")
        message = []    # Initializing list of message lines
        while True:
            line = sys.stdin.readline()
            if line == ".\n":
                sys.stdout.write(line + '\n')
                sys.stdout.write("250 OK\n")
                return message
            else:
                message.append(line)
                sys.stdout.write(line)

# Parses path component of SMTP command
def parsePath(path):
    if (path[0] != "<" or path[len(path)-1]) != ">":
        sys.stdout.write("501 Syntax error in parameters or arguments\n")
        return 0
    mailbox = path[1:len(path)-1]
    if parseMailbox(mailbox) == 0: return 0
    else: return mailbox

# Parses mailbox component of SMTP command
def parseMailbox(mailbox):
    special = ["<", ">", "(" , ")" , "[" , "]" , "\\" , "." , "," , ";" , ":" , "\"", " "]
    position = 0
    hasLocalPart = False
    # print mailbox
    for char in mailbox:
        # print "here"
        if char in special:
            sys.stdout.write("501 Syntax error in parameters or arguments\n")
            return 0
        elif char not in special and char != "@":
            hasLocalPart = True
        elif char == "@" and hasLocalPart:
            break
        elif char == "@" and not hasLocalPart:
            sys.stdout.write("501 Syntax error in parameters or arguments\n")
            return 0
        position+=1
    if position >= len(mailbox):
        sys.stdout.write("501 Syntax error in parameters or arguments\n")
        return 0
    domain = mailbox[position:]
    if domain[0] != "@":
        sys.stdout.write("501 Syntax error in parameters or arguments\n")
        return 0
    if (parseDomain(domain[1:len(domain)]) == 0):
        # print domain[1:len(domain)]
        return 0

# Parses domain component of mail-from command
def parseDomain(domain):
    index = 0
    hasElement = False
    for char in domain:
        if not char.isalpha() and not char.isdigit():
            if char != ".":         # If char in domain is neither <a>,<d>, nor '.' throw error
                sys.stdout.write("501 Syntax error in parameters or arguments\n")
                return 0
            elif char == "." and not hasElement:        # If there is no element before '.', throw error
                sys.stdout.write("501 Syntax error in parameters or arguments\n")
                return 0
        else:
            if char.isdigit() and domain[index-1] == ".":       # If the first char in domain element is a digit throw error
                sys.stdout.write("501 Syntax error in parameters or arguments\n")
                return 0
            if hasElement and char != domain[len(domain)-1]:      # if char is not the first nor last character in the domain
                if char.isalpha() and (domain[index-1] == "." and domain[index+1] == "."): # If only one <a> in domain element throw error
                    sys.stdout.write("501 Syntax error in parameters or arguments\n")
                    return 0
            hasElement = True
        index+=1

"""
-tokenizeSMTPCommand(): Tokenizes string of MAIL FROM or RCPT command that is input and returns as an array of
    tokens ready to be parsed
-Parameters: The string of the command taken from the file input at the command line - provided by
    argument passed to 'parseMailCommand()' or 'parseRcptCommand()'
"""
def tokenizeSMTPCommand(command):
    index = 0
    tokens = [None]*3

    # Tokenize first part of command
    for char in command:
        if char == " ": break
        else:
            index+=1
    tokens[0] = command[0:index]

    # Remove first token from string
    command = command[index:]
    index = 0
    # Tokenize second part of command
    startNextToken = 0
    for char in command:
        if char == ":":
            break
        elif char.isalpha() and command[index-1] == " ":
            startNextToken = index
            index+=1
        else: index+=1
    tokens[1] = command[startNextToken:index+1]

    # Remove second token from string
    command = command[index+1:]
    index = 0
    #Tokenize path
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
-createMessage(): creates file in ./forward directory and writes email message to it
-parameters: sender (mailbox of sender), recipients (list of recipients), message (list of each line of message)
"""
def createMessage(sender, recipients, message):
    for recipient in recipients:
        mail = open('./forward/' + recipient, 'a+')
        mail.write('From: <' + sender + '>' + '\n')
        mail.write('To: <' + recipient + '>' + '\n')
        for line in message:
            mail.write(line)
    mail.close

"""
Retrieving command that is input from stdin and feeding it to the correct parser.
"""
hasMailFrom = False
hasRcpt = False
recipients = []
while True:
    command = sys.stdin.readline().rstrip('\n')
    tokens = tokenizeSMTPCommand(command)
    if tokens[0] == "MAIL":
        if hasMailFrom:
            sys.stdout.write("503 Bad sequence of commands\n")
        else:
            sender = parseMailCommand(tokens)
            if sender != 0:
                hasMailFrom = True
    elif tokens[0] == "RCPT":
        if not hasMailFrom:
            sys.stdout.write("503 Bad sequence of commands\n")
        else:
            recipients.append(parseRcptCommand(tokens))
            hasRcpt = True
    elif command == "DATA":
        if not hasRcpt:
            sys.stdout.write("503 Bad sequence of commands\n")
        else:
            message = parseDataCommand(command)
            createMessage(sender, recipients, message)
            hasMailFrom = False
            hasRcpt = False
    else:
        sys.stdout.write("500 Syntax error: command unrecognized\n")
