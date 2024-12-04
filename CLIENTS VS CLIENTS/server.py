import socket
import threading

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []
queue = []
choices = {}  # Dictionary to store client moves

def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            print(f"Received message: {message}")
            if message.startswith("MOVE"):
                _, move = message.split()
                choices[client] = move
                client2 = find_opponent(client)
                if client2:
                    evaluate_game(client, client2)
            else:
                print("Received non-move message")
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                print(f"{nickname} has left the chat.")
                nicknames.remove(nickname)
            break

def find_opponent(client):
    for client2 in choices:
        if client2 != client and client2 in clients:
            return client2
    return None

def evaluate_game(client1, client2):
    move1 = choices[client1]
    move2 = choices[client2]
    index1 = clients.index(client1)
    index2 = clients.index(client2)
    nickname1 = nicknames[index1]
    nickname2 = nicknames[index2]

    result = ""
    if move1 == move2:
        result = "It's a draw!"
    elif (move1 == "Rock" and move2 == "Scissors") or (move1 == "Scissors" and move2 == "Paper") or (move1 == "Paper" and move2 == "Rock"):
        result = f"{nickname1} wins!"
    else:
        result = f"{nickname2} wins!"

    client1.send(f"Your move: {move1}, Opponent's move: {move2}. {result}".encode('ascii'))
    client2.send(f"Your move: {move2}, Opponent's move: {move1}. {result}".encode('ascii'))

    # Reset choices
    del choices[client1]
    del choices[client2]

def match_clients(client1, client2):
    index1 = clients.index(client1)
    index2 = clients.index(client2)

    nickname1 = nicknames[index1]
    nickname2 = nicknames[index2]

    client1.send("You are matched with another player. Start playing!".encode('ascii'))
    client1.send("Choose Paper/Rock/Scissors".encode('ascii'))
    client1.send("PLAY".encode('ascii'))

    client2.send("You are matched with another player. Start playing!".encode('ascii'))
    client2.send("Choose Paper/Rock/Scissors".encode('ascii'))
    client2.send("PLAY".encode('ascii'))

def receive():
    while True:
        client, address = server.accept()
        print(f"Connection from {address} has been established.")

        client.send('username'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        client.send("You are now connected!".encode('ascii'))

        if len(queue) == 0:
            client.send("Room empty, wait for someone to join.".encode('ascii'))
            queue.append(client)
        else:
            matched_client = queue.pop(0)
            match_clients(matched_client, client)

        client_thread = threading.Thread(target=handle_client, args=(client,))
        client_thread.start()

receive()
