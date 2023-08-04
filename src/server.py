import socket as sock
import threading
import select
import sys
import os

os.system("cls")
server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
server.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)

if len(sys.argv) != 2:
    print("error\nCorrect usage: script, IP address")
    exit()

print(sys.argv)
IP_addr = str(sys.argv[1])
Port = 55555

server.bind((IP_addr, Port))
server.listen(100)

clients = []
c_names = []

def client_thread(conn, addr, c_name):
    conn.send("[38;5;40mYO men, wellcome to my chat program".encode())
    conn.send(f"you name is {c_name}".encode())
    conn.send("\nnow give me your money.[m\n\n".encode())

    while True:
        try:
            message = conn.recv(2048).decode()
            if message:
                index = clients.index(conn)
                name = c_names[index]
                if "/sys" in message:
                    if "--server" in message:
                        sysct = message.replace(f"{name}: /sys --server ", "")
                        os.system(f"{sysct}")
                    if f"--{name}" in message:
                        print("execute in client")
                    else:
                        pass

                print("<", addr[0] , ">", message)
                message_to_send = "<" + addr[0] + ">" + message
                broadcast(message_to_send.encode(), conn)
            else:
                remove(conn)
        except:
            index = clients.index(conn)
            c_name = c_names[index]
            print(f'{c_name} left the chat')
            broadcast(f'{c_name} left the chat'.encode(), conn)
            conn.close()
            clients.remove(conn)
            c_names.remove(c_name)
            break

def broadcast(message, conn):
    for client in clients:
        if client != conn:
            try:
                client.send(message)
            except:
                continue

def receive():
    while True:
        conn, addr = server.accept()
        print(addr[0], "connected")

        conn.send('NICK'.encode())
        c_name = conn.recv(2048).decode()
        c_names.append(c_name)
        clients.append(conn)
        print("the joined clients: ", len(clients))

        print(f'name is {c_name}')
        broadcast(f'{c_name} joined the chat!\n'.encode(),conn)
        conn.send(b'sucess to connected the server!')

        thread = threading.Thread(target=client_thread, args=(conn, addr, c_name))
        thread.start()

print("[*] server started")
receive()
