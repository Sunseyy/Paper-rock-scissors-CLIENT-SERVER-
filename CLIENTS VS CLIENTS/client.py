import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

username = input("Please enter your username: ")

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            print(f"Received message: {message}")
            if message == 'username':
                client.send(username.encode('ascii'))
            elif message == 'PLAY':
                print("Entering PLAY state")
                valid_moves = ["PAPER", "ROCK", "SCISSORS"]
                while True:
                    game = input("Choose Paper/Rock/Scissors: ").upper()
                    print(f"{game} is blah blah")
                    if game in valid_moves:
                        print("Sending move to server")
                        client.send(f'MOVE {game.capitalize()}'.encode('ascii'))
                        break
                    else:
                        print("Invalid input. Please choose Paper, Rock, or Scissors.")
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        message = f'{username}: {input("")}'
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
