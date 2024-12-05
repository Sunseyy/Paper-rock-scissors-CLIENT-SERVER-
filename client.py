import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

def display_menu():
    print("1. Start Random Match")
    print("2. Send Game Invite")
    print("3. Accept Game Invite")
    print("4. View Player Rankings")
    print("5. Tournant")
    print("6. Quit")
    print("7.see result of invite (clear invitation)")
    choice = input("Enter your choice: ")
    return int(choice)

def handle_choice(choice):
    if choice == 1:
        client.send(b'random_match')
    elif choice == 2:
        #recipient = input("Enter the username to invite: ")
        client.send(f'send_invite'.encode('ascii'))
    elif choice == 3:
        
        client.send('accept_invite'.encode('ascii'))
    elif choice == 4:
        client.send(b'view_rankings')
    elif choice == 5:
        client.send(b'Tournoi')
    elif choice == 6:
        client.send(b'quit')
        client.close()
        exit()
    elif choice ==7:
        client.send(b'see')

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'L/S':
                
                while True:
                    L_S = input("Welcome! Type 'Login' to log in or 'Signup' to create a new account: ")
                    if L_S.lower() == 'login' or L_S.lower() == 'signup':
                        break

                client.send(L_S.encode('ascii'))
            elif message == 'Username: ':
                username = input("Enter your username: ")
                client.send(username.encode('ascii'))
            elif message == 'Password: ':
                password = input("Enter your password: ")
                client.send(password.encode('ascii'))
            elif message == 'menu':
                
                    choice = display_menu()
                    handle_choice(choice)
            elif message.startswith('Match'):
                print("Match received, waiting for input...")
                
                while True:
                    move = input("Choose Paper rock scissors: ")
                    if move == "rock" or move =="paper" or move =="scissors":
                        break
                print(f"Sending choice: {move}")
                client.send(move.encode('ascii'))
            elif message == 'join_tournament':
                choice_tournament=input("  you want to join ? (1/quit)")
                client.send(choice_tournament.encode('ascii'))
            elif message == 'bye':
                client.close()
                exit()
            elif message =='invite':
                invitee = input("Enter the username to invite:")
                client.send(invitee.encode('ascii'))
            else:
                print(message)
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
            break

thread = threading.Thread(target=receive)
thread.start()
