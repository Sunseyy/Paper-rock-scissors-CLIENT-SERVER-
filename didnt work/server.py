import socket
import threading

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
user_credentials = {}  # This will store username: password ,scores , last attempt
queue = []

def handle_client(client_socket, username):
    try:
        while True:
            handle_MENU(client_socket, username)
    except Exception as e:
        print(f"An error occurred in handle_client: {e}")
        client_socket.close()

def play_random(client, username):
    if len(queue) == 0:
        client.send("Room empty, waiting for someone to join...".encode('ascii'))
        queue.append((client, username))
        while True:
            if len(queue) == 0:
                print("Room is no longer empty, breaking wait loop.")
                break
    else:
        matched_client, matched_username = queue.pop(0)
        match_clients(matched_client, client, matched_username, username)

def match_clients(client1, client2, user1, user2):
    try:
        # Notify both clients that they have been matched
        client1.send("You have been matched! Type Rock, Paper, or Scissors: ".encode('ascii'))
        client2.send("You have been matched! Type Rock, Paper, or Scissors: ".encode('ascii'))
        
        # Receive choices from both players
        choice1 = client1.recv(1024).decode('ascii').strip().lower()
        choice2 = client2.recv(1024).decode('ascii').strip().lower()
        
        # Determine the winner
        result = determine_winner(choice1, choice2)
        
        # Send results back to both clients
        client1.send(f"You chose {choice1}, opponent chose {choice2}. {result}".encode('ascii'))
        client2.send(f"You chose {choice2}, opponent chose {choice1}. {result}".encode('ascii'))
        
    except Exception as e:
        print(f"An error occurred during the match: {e}")
        client1.close()
        client2.close()

def determine_winner(choice1, choice2):
    if choice1 == choice2:
        return "It's a tie!"
    elif (choice1 == 'rock' and choice2 == 'scissors') or \
         (choice1 == 'scissors' and choice2 == 'paper') or \
         (choice1 == 'paper' and choice2 == 'rock'):
        return "You won!"
    else:
        return "You lost!"

def handle_MENU(client, username):
    # Loop to keep showing the menu after each game
    while True:
        client.send("Welcome to the Paper Rock Scissors Game!\nPlease choose an option from the menu below:\n1 - Play against someone on the server\n2 - Tournament against multiple people\n3 - View game statistics\nEnter your choice (1, 2, or 3): ".encode('ascii'))
        menu_choice = client.recv(1024).decode('ascii').strip()

        if menu_choice == '1':
            print(f'{username} is playing against a random person.')
            play_random(client, username)
        elif menu_choice == '2':
            client.send('Tournament feature not yet implemented.\n'.encode('ascii'))
            print('Tournament feature not yet implemented.')  # Placeholder for future implementation
        elif menu_choice == '3':
            client.send('Viewing game statistics not yet implemented.\n'.encode('ascii'))
            print('Viewing game statistics not yet implemented.')  # Placeholder for future implementation
        else:
            client.send("Invalid choice, try again.\n".encode('ascii'))

def start():
    print(f"Server started on {host}:{port}")
    while True:
        client_socket, addr = server.accept()
        print(f"New connection from {addr}")
        
        try:
            client_socket.send("L/S".encode('ascii'))
            L_S = client_socket.recv(1024).decode('ascii').strip()

            if L_S.lower() == 'login':
                client_socket.send('Username: '.encode('ascii'))
                username = client_socket.recv(1024).decode('ascii').strip()
                
                client_socket.send('Password: '.encode('ascii'))
                password = client_socket.recv(1024).decode('ascii').strip()
                
                if username in user_credentials and user_credentials[username]['password'] == password:
                    client_socket.send("Login successful!".encode('ascii'))
                    print(f"{username} logged in successfully.")
                    threading.Thread(target=handle_client, args=(client_socket, username)).start()
                else:
                    client_socket.send("Invalid credentials. Connection closed.".encode('ascii'))
                    print(f"Failed login attempt for username: {username}")
                    client_socket.close()

            elif L_S.lower() == 'signup':
                client_socket.send('Username: '.encode('ascii'))
                username = client_socket.recv(1024).decode('ascii').strip()
                
                if username in user_credentials:
                    client_socket.send("Username already taken. Connection closed.".encode('ascii'))
                    print(f"Username already taken: {username}")
                    client_socket.close()
                else:
                    client_socket.send('Password: '.encode('ascii'))
                    password = client_socket.recv(1024).decode('ascii').strip()
                    
                    user_credentials[username] = {'password': password, 'score': 0, 'last_attempt': None}
                    client_socket.send("Signup successful!".encode('ascii'))
                    print(f"New user registered: {username}")
                    
                    threading.Thread(target=handle_client, args=(client_socket, username)).start()
        
        except Exception as e:
            print(f"An error occurred: {e}")
            client_socket.close()

start()
