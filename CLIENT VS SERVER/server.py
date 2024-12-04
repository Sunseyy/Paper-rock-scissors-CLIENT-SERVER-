import socket
import threading
import random

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

def Server_choice():
    return random.choice(["rock", "paper", "scissors"])

def determine_winner(message, Choice):
    if message == Choice:
        return "It's a tie!"
    elif ((message == "rock" and Choice == "scissors") or 
          (message == "paper" and Choice == "rock") or 
          (message == "scissors" and Choice == "paper")):
        return "Client wins!"
    else:
        return "Server wins!"

def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if not message:
                break

            Choice = Server_choice()
            win = determine_winner(message, Choice)
            client.send(f'{win} (Server chose {Choice})'.encode('ascii'))
        except:
            break
    client.close()

def start_server():
    while True:
        client, address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client,))
        client_thread.start()
        print(f"Connection from {address} has been established.")

start_server()
