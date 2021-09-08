import select
import socket

HEADER = 10
IP = "localhost"
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))

server_socket.listen(10)

sockets_list = [server_socket]
clients = {}

joined = "{joined}"
left = "{left}"


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER)

        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}

    except:
        print("ok")
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for notified_sockets in read_sockets:
        if notified_sockets == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)
            if user is False:
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = user

            client_socket.send(f"{len(sockets_list):<{HEADER}}".encode('utf-8'))

            print(f"Accepted new connection from{client_address[0]} : {client_address[1]} username:"
                  f"{user['data'].decode('utf-8')}")

            for client_socket in clients:
                client_socket.send(user['header'] + user['data'] + f"{len(joined):<{HEADER}}".encode("utf-8") +
                                   joined.encode("utf-8") + f"{len(sockets_list):<{HEADER}}".encode('utf-8'))


        else:
            message = receive_message(notified_sockets)

            if message is False:
                print(f"Closed connection from {clients[notified_sockets]['data'].decode('utf-8')}")
                header_user_left = clients[notified_sockets]['header']
                name_user_left = clients[notified_sockets]['data']
                sockets_list.remove(notified_sockets)
                for client_socket in clients:
                    client_socket.send(header_user_left + name_user_left +
                                       f"{len(left):<{HEADER}}".encode("utf-8") +
                                       left.encode("utf-8") +
                                       f"{len(sockets_list):<{HEADER}}".encode('utf-8'))
                del clients[notified_sockets]
                continue
            user = clients[notified_sockets]
            print(f"Received message from {user['data'].decode('utf-8')}:{message['data'].decode('utf-8')}")

            for client_socket in clients:
                if client_socket != notified_sockets:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'] +
                                       f"{len(sockets_list):<{HEADER}}".encode('utf-8'))

    for notified_sockets in exception_sockets:
        sockets_list.remove(notified_sockets)
        del clients[notified_sockets]
