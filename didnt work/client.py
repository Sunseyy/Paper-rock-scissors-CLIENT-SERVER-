import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'L/S':
                L_S = input("Welcome! Type 'Login' to log in or 'Signup' to create a new account: ")
                client.send(L_S.encode('ascii'))
            elif message == 'Username: ':
                username = input("Enter your username: ")
                client.send(username.encode('ascii'))
            elif message == 'Password: ':
                password = input("Enter your password: ")
                client.send(password.encode('ascii'))
            elif message.startswith('Welcome'):
                usermenu_choice = input(
                    "Welcome to the Paper Rock Scissors Game!\n"
                    "Please choose an option from the menu below:\n"
                    "1 - Play against someone on the server\n"
                    "2 - Tournament against multiple people\n"
                    "3 - View game statistics\n"
                    "Enter your choice (1, 2, or 3): "
                )
                client.send(usermenu_choice.encode('ascii'))
            elif "waiting for someone to join" in message:
                print(message)
                
            elif "You have been matched" in message:
                print(message)
                choice = input("Type Rock, Paper, or Scissors: ")
                client.send(choice.encode('ascii'))
            else:
                print(message)
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
            break

thread = threading.Thread(target=receive)
thread.start()
