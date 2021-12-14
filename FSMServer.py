import socket, subprocess, os



def connectionHandler(info, newsock):
    print(f"New connection: {src}")
    data = newsock.recv(4096)
    print(data.decode())

def write_function(filename):
    try:
        if filename != '':
            file = open(filename, 'w+')
            newconn.send((f"Writing to file: \"{filename}\"").encode())
        else:
            newconn.send((f"Cant open {filename}").encode())
            return
    except OSError:
        return

    while True:
        newconn.send((" (w) > ").encode())
        words = newconn.recv(4096).decode()
        if words == "\x10":
            break
        file.write(words + "\n")
    file.close()
        

def cd_function(dirname):
    try:
        os.chdir(os.curdir + "/" + dirname)
    except OSError:
        newconn.send((f"Directory: {dirname} does not exist").encode())

def cat_function(filename):
    try:
        file = open(filename)
        lines = ""
        for line in file:
            lines += line
        newconn.send(lines.encode())
    except FileNotFoundError:
        newconn.send((f"File: {filename} does not exist").encode())

def mkdir_function(dirname):
    try:
        os.mkdir(dirname)
    except FileExistsError:
        newconn.send((f"Directory: {dirname} already exists").encode())


if __name__ == '__main__':
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 40000
    serversock.bind((host, port))
    serversock.listen(5)

    commands = ["pwd", "ls", "write", "cd", "quit", "cat", "mkdir"]

    while True:
        newconn, src = serversock.accept()

        while True:
            newconn.send((" > ").encode())
            command = newconn.recv(4096).decode()
            tokens = command.split(" ")
            
            if (tokens[0] not in commands):
                newconn.send(("Invalid command \n > ").encode())
                continue

            if tokens[0] == "pwd":
                output = os.path.realpath(os.getcwd())
                newconn.send(output.encode())

            if tokens[0] == "ls":
                output = "\n".join(os.listdir(os.getcwd()))
                newconn.send(output.encode())

            if tokens[0] == "cd":
                cd_function(tokens[1])

            if tokens[0] == "write":
                if len(tokens) < 2:
                    newconn.send((f"Missing required argument").encode())
                if len(tokens) == 2:
                    write_function(tokens[1])

            if tokens[0] == "cat":
                cat_function(tokens[1])

            if tokens[0] == "mkdir":
                mkdir_function(tokens[1])

            if tokens[0] == "quit":
                newconn.close()
                break
