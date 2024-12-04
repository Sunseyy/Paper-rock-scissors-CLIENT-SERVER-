import socket
import threading
import queue

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
user_credentials = {}  # This will store username: password ,scores , last attempt

matchmaking_queue = queue.Queue()


def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            
           
            
            if message == 'menu':
                handle_menu(client_socket)
            elif message == 'random_match':
                
                handle_random_match(client_socket)
            elif message == 'send_invite':
                #handle_invite(client_socket, data)
                pass
            elif message == 'accept_invite':
                #handle_accept_invite(client_socket, data)
                pass
            elif message == 'quit':
                break

        except:
            break

    client_socket.close()
    print(f"Connection closed from {client_address}")

def handle_menu(client_socket):
    menu = """
    1. Start Random Match
    2. Send Game Invite
    3. Accept Game Invite
    4. Quit
    """
    client_socket.send(menu.encode())

def handle_random_match(client_socket):
    add_to_queue(client_socket)
    print(queue)
    print("this is the queue")
    
    match = find_match()
    print(match)
    if match:
        print("coucou3")
        player1_socket, player2_socket = match
        start_game_session(player1_socket, player2_socket)
    else:
        # Wait for another player to join
        wait_for_match(client_socket)


def add_to_queue(client_socket):
    matchmaking_queue.put(client_socket)

def find_match():
    if matchmaking_queue.qsize() >= 2:
        print("COUCOU")
        player1_socket = matchmaking_queue.get()
        print("Coucou1")
        player2_socket = matchmaking_queue.get()
        print(player1_socket, player2_socket)
        return player1_socket, player2_socket
    return None

def wait_for_match(client_socket):
    while matchmaking_queue.qsize() < 2:
        print("IM WAITING")
        continue
    handle_random_match(client_socket)
def start_game_session(player1_socket, player2_socket):
    # Notify both players that the game is starting
    
    player1_socket.send(b"Match found! Starting game...")
    
    player2_socket.send(b"Match found! Starting game...")
    
    # Game loop for handling moves and determining the winner
   
    move1 = receive_move(player1_socket)
    print(move1)
    move2 = receive_move(player2_socket)
       
    print(move2)
        
    winner = determine_winner(move1, move2)
        
    player1_socket.send(f"Opponent move: {move2}. Result: {winner}".encode())
    player1_socket.send("menu".encode())
    player2_socket.send(f"Opponent move: {move1}. Result: {winner}".encode())
        
        

    
   
def receive_move(client_socket):
    try:
       
        move = client_socket.recv(1024).decode()
        if move in ["rock", "paper", "scissors"]:
            return move
    except:
        return None 

def determine_winner(move1, move2):
    if move1 == move2:
        return "Draw"
    elif (move1 == "rock" and move2 == "scissors") or \
         (move1 == "scissors" and move2 == "paper") or \
         (move1 == "paper" and move2 == "rock"):
        return "Player 1 wins"
    else:
        return "Player 2 wins"
    

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
                    client_socket.send('menu'.encode('ascii'))
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
                    client_socket.send('menu'.encode('ascii'))
                    threading.Thread(target=handle_client, args=(client_socket, username)).start()
        
        except Exception as e:
            print(f"An error occurred: {e}")
            client_socket.close()

start()
