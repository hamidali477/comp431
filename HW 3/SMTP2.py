#! ~/comp431/submissions/HW3
import sys, fileinput

def parse_forward_file(forward_file):
    """ Parses forward-file and retrieves sender and receiver email addresses and
    the email message to write corresponding commands to stdout.
    """

    msg = ''
    for line in forward_file:
        index = 0
        if line[0:5] == "From:" and msg == '':
            send_command("mail-from", parse_path(line))
            check_response(sys.stdin.readline().rstrip('\n'), 'mail-from')

        elif line[0:5] == "From:" and msg != '':
            """ Handles case of multiple messages in forward file. If next 'From:'
            of file is reached, send DATA cmd and reset for next message
            """
            send_command("data", msg)
            check_response(sys.stdin.readline().rstrip('\n'), 'msg')
            msg = ''
            send_command("mail-from", parse_path(line))
            check_response(sys.stdin.readline().rstrip('\n'), 'mail-from')

        elif line[0:3] == "To:":
            send_command("rcpt-to", parse_path(line))
            check_response(sys.stdin.readline().rstrip('\n'), 'rcpt-to')
        else:
            msg+=line

    send_command("data", msg)
    check_response(sys.stdin.readline().rstrip('\n'), 'data')
    sys.stdout.write("QUIT")
    sys.exit()

def parse_path(line):
    """ Returns email address from lines starting with 'From:' or 'To:' """

    index = 0
    for char in line:
        if char == '<':
            start_mailbox = index
        if char == '>':
            end_mailbox = index+1
        index+=1
    return line[start_mailbox:end_mailbox]

def send_command(command, token):
    """ Writes command to stdout """

    if command == "mail-from":
        sys.stdout.write("MAIL FROM: " + token + '\n')
    if command == "rcpt-to":
        sys.stdout.write("RCPT TO: " + token + '\n')
    if command == "data":
        sys.stdout.write("DATA\n")
        check_response(sys.stdin.readline().rstrip('\n'), 'data')
        sys.stdout.write(token + '\n.\n')

def check_response(response, command):
    """ check's response of "server" """

    sys.stderr.write(response + '\n')
    if response[0:3] == "250" and command != 'data':
        return True
    elif response[0:3] == "354" and command == 'data':
        return True
    else:
        sys.stdout.write("QUIT\n")
        sys.exit()

parse_forward_file(fileinput.input())
