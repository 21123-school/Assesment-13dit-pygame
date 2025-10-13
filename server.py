import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 49152))
server_socket.listen(5)

print("Server listening on port 49152...")

numid = 0
running = False

client_list = {}


def handle(client_socket, address, cid, client_list, running):
    """ """

    def findclients(location, client_list):
        """ """
        found = []
        for client in client_list:
            if client_list[client]['l'] == location:
                found.append(client)
        return found

    client_socket.sendall(cid)

    while running:
        client_data = client_socket.recv(1024)
        if client_data == b'\xef':
            print('Client ID:', int.from_bytes(cid), 'has left the game')
            del client_list[cid]
            break
        elif client_data:
            client_data = list(client_data)
            client_list[client_data[0].to_bytes(1, 'little')] = {'x': client_data[1].to_bytes(1, 'little') + client_data[2].to_bytes(1, 'little')}
            client_list[client_data[0].to_bytes(1, 'little')] = client_list[client_data[0].to_bytes(1, 'little')] + {'y': client_data[3].to_bytes(1, 'little') + client_data[4].to_bytes(1, 'little')}
            client_list[client_data[0].to_bytes(1, 'little')] = client_list[client_data[0].to_bytes(1, 'little')] + {'d':client_data[5].to_bytes(1, 'little'),'m':client_data[6].to_bytes(1, 'little'),'l':client_data[7].to_bytes(1, 'little')}
            client_list[client_data[0].to_bytes(1, 'little')]['n'] = chr(client_data[8]) + chr(client_data[9]) + chr(client_data[10])
            data = b''
            for client in findclients(client_list[cid]['l'], client_list):
                data = data + client + client_list[client]['x'] + client_list[client]['y'] + client_list[client]['d'] + client_list[client]['m'] + client_list[client]['l'] + client_list[client]['n'].encode() + b'\xff'
            client_socket.sendall(data)
    client_socket.close()


while True:
    client_socket, address = server_socket.accept()
    print('Client joined at IP:', address[0], ', ID assigned: ', numid)
    client_thread = threading.Thread(target=handle, args=(client_socket, address, numid.to_bytes(1, 'little'), client_list, running))
    client_thread.start()
    numid += 1
    running = True