import socket

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 40000
    s.connect((host, port))
    
    

    while True:
        message = s.recv(4096)
        print(message.decode(), end="")

        if message.decode() == " > " or message.decode() == " (w) > ":
            command = input()
            if command != "":
                s.send(command.encode())
            else:
                s.send(("\x10").encode())
            if command == "quit":
                break
        else:
            print()

        # data = s.recv(4096)
        # print(data.decode(), end=" b\n")

    s.close()
