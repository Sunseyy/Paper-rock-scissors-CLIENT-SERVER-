import socket
import threading
import queue
import time
import random 
host = '127.0.0.1'
port = 55555
import sys
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
user_credentials = {}  # This will store username: password ,scores , last attempt , client

queue=[]
tournoi= []

def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    
    while True:
        try:
            client_socket.send('menu'.encode('ascii'))
            
            message = client_socket.recv(1024).decode()
            #print("i am right as usual")
            if not message:
                break

            
           
            
            if message == 'menu':
                handle_menu(client_socket)
            elif message == 'random_match':
                
                handle_random_match(client_socket,client_address)
                #print("coucou")
            elif message == 'send_invite':
                handle_invite(client_socket,client_address)
                pass
            elif message == 'accept_invite':
                accept_invite(client_socket,client_address)
                pass
            elif message == "view_rankings":
               
                view_rankings(client_socket);
                #print("Hey")
            elif message == 'Tournoi':
                start_tournoi(client_socket,client_address)
                #print("Im here ",{client_address})
                #print(user_credentials[client_address])
            
            elif message == 'see':
                see_result(client_socket,client_address)
                #print(user_credentials[client_address])
                
                
            elif message == 'quit':
                #print(user_credentials[client_address]["status"])
                user_credentials[client_address]["status"] = "Offline"
                #print(user_credentials[client_address]["status"])
                break

        except Exception as e:
            #print(f"An error occurred: {e}")
            pass

    client_socket.close()
    user_credentials[client_address]["status"]= "Offline"
    print(f"Connection closed from {client_address}")

def see_result(client, username):
    if user_credentials[username]["result"] is not None and user_credentials[username]["Invite_statuts"] == "Done":
        client.send(f"\033[34mResult of your last invited game against {user_credentials[username]['Invt_From']} : {user_credentials[username]['result']}\033[0m".encode('ascii'))

        client.send("\033[32mclearing the game...\033[0m".encode('ascii'))

        user_credentials[username]["Invt_From"] = None
        user_credentials[username]["Invite_statuts"] = None
        user_credentials[username]["last_attempt"] = None
   




def handle_invite(client,username):
    print(user_credentials[username]["last_attempt"])
    if user_credentials[username]["Invite_statuts"] == None and user_credentials[username]["Invt_From"] == None:
        client.send("invite".encode('ascii'))
        invitee=client.recv(1024).decode()
        if invitee in user_credentials and user_credentials[invitee]["client"] is not None:
            #print("here")
            user_credentials[username]["Invt_To"] = invitee
            user_credentials[username]["Invite_statuts"] ="Pending"
            client.send("Match".encode('ascii'))
            last=client.recv(1024).decode()
            user_credentials[username]["last_attempt"] =last
            user_credentials[invitee]["Invt_From"] =username
       
    else :
        client.send("\033[31mPlease let them accept your invitation then try again\033[0m".encode("ascii"))

    print(user_credentials[username]["last_attempt"])
        
def accept_invite(client, username):
    try:
        invite_from = user_credentials[username]['Invt_From']
        client.send(f"Your invitations are from {invite_from}".encode('ascii'))

        client.send("Match".encode('ascii'))
        chance1 = client.recv(1024).decode()
        user_credentials[username]['last_attempt'] = chance1
        #print('chance1', chance1)

        # Check if 'Invt_From' exists and has a valid user
        if invite_from not in user_credentials:
            print(f"Invite from user '{invite_from}' does not exist.")
            return

        chance2 = user_credentials[invite_from]['last_attempt']
        #print('chance2', chance2)

        result = compare_choices(chance1, chance2)
        if result == 0:
            user_credentials[invite_from]['result'] = "It's a tie"
            user_credentials[username]['result'] = "It's a tie"
            user_credentials[username]['score'] += 2
            user_credentials[invite_from]['score'] += 2
        elif result == 1:
            user_credentials[invite_from]['result'] = "You lost!"
            user_credentials[username]['result'] = "You won!"
            user_credentials[username]['score'] += 5
            user_credentials[invite_from]['score'] -= 2
        elif result == -1:
            user_credentials[invite_from]['result'] = "You won!"
            user_credentials[username]['result'] = "You lost!"
            user_credentials[username]['score'] -= 2
            user_credentials[invite_from]['score'] += 5

        #print("im here")

        user_credentials[username]["Invite_statuts"] = "Done"
        user_credentials[invite_from]["Invite_statuts"] = "Done"
        user_credentials[invite_from]["Invt_To"] = None
        print(user_credentials[username]["Invite_statuts"])

    except KeyError as e:
        #print(f"KeyError: {e}")
        pass
    except Exception as e:
        #print(f"An error occurred: {e}")
        pass

# You can also add specific prints before each critical operation to trace exactly where it fails.

    

def display_tournament(tournoi,client):
   for users in tournoi:
       print(f"Tournant : {users}")
    

def start_tournoi(client, username):
        display_tournament(tournoi,client)
        start_game=0
        #print(username)
   
        client.send("join_tournament".encode('ascii'))
        choice = client.recv(1024).decode()
        
        if choice in ["1"]:
            if len(tournoi)<3: #1
                tournoi.append(username)
                client.send(f"You have successfully joined {1}".encode('ascii'))
                while len(tournoi)<5: #2
                    continue
                #print("hey")
                tournoi.clear()
            elif len(tournoi)==3 : #1
                tournoi.append(username)
                client.send("we will start the game !".encode('ascii'))
                pair1,pair2=get_pairs(tournoi)
                #client 1 vs client 2
                
                # Using get() to avoid KeyError
               
                client1 = user_credentials.get(pair1[0], {}).get("client", "Client not found")
                client2 = user_credentials.get(pair1[1], {}).get("client", "Client not found")
                client3 = user_credentials.get(pair2[0], {}).get("client", "Client not found")
                client4 = user_credentials.get(pair2[1], {}).get("client", "Client not found")

                while True:
                    client1.send(f"You will be playing against {pair1[1]}".encode('ascii'))
                    
                    client1.send("Match".encode('ascii'))
                    
                    client2.send(f"You will be playing against {pair1[0]}".encode('ascii'))
                    client2.send("Match".encode('ascii'))
                    choice1 = client1.recv(1024).decode()
                

                
                    choice2 = client2.recv(1024).decode()
                    result1 = compare_choices(choice1, choice2)
                    if result1 == 1 :
                        win = pair1[0]
                        winner = client1
                        break
                    elif result1 == -1:
                        win = pair1[1]
                        winner = client2
                        break

                print("Winner of first round is ", winner)
                while True:
                    client3.send(f"You will be playing against {pair2[1]}".encode('ascii'))
                    
                    client4.send(f"You will be playing against {pair2[0]}".encode('ascii'))
                    client3.send("Match".encode('ascii'))
                    client4.send("Match".encode('ascii'))
                    choice3 = client3.recv(1024).decode()
                    choice4 = client4.recv(1024).decode()
                    result2 = compare_choices(choice3, choice4)
                    if result2 == 1 :
                        win2 = pair2[0]
                        winner2 = client3
                        break
                    elif result2 == -1:
                        win2 = pair2[1]
                        winner2 = client4
                        break

                print("winner of the second round is ", winner2)

                while True:
                    winner.send(f"You will be playing against {win2}".encode('ascii'))
                    
                    winner2.send(f"You will be playing against {win}".encode('ascii'))
                    winner.send("Match".encode('ascii'))
                    winner2.send("Match".encode('ascii'))
                    choice5 = winner.recv(1024).decode()
                    choice6 = winner2.recv(1024).decode()
                    result3 = compare_choices(choice5, choice6)
                    if result3 == 1 :
                        winner3 = win
                        break
                    elif result3 == -1:
                        winner3 = win2
                        break


                '''client1.send(f"Winner is {winner3} he won 10 points".encode('ascii'))
                client2.send(f"Winner is {winner3} he won 10 points".encode('ascii'))
                client3.send(f"Winner is {winner3} he won 10 points".encode('ascii'))
                client4.send(f"Winner is {winner3} he won 10 points".encode('ascii'))'''
                red_text = f"\033[31mWinner is {winner3} he won 10 points\033[0m"
                client1.send(red_text.encode('ascii'))
                client2.send(red_text.encode('ascii'))
                client3.send(red_text.encode('ascii'))
                client4.send(red_text.encode('ascii'))

                
                user_credentials[winner3]['score']+=10
                    
                
                tournoi.append("NEW")
                    
                    
                    
                    
                

                    
                 


                
                
                

                # Compare the choices for client1 vs client2 (pair1)
               
          
def get_pairs(tournoi):
    random.shuffle(tournoi)
    pair1 = tournoi[:2]
    pair2 = tournoi[2:]
    return pair1, pair2


def compare_choices(choice1, choice2):
    
    if choice1 == choice2:
        
        return 0
    elif (choice1 == 'rock' and choice2 == 'scissors') or \
         (choice1 == 'scissors' and choice2 == 'paper') or \
         (choice1 == 'paper' and choice2 == 'rock'):
        return 1
    else:
        return -1


def view_rankings(client_socket):
    print("amm")
    try:
        print("am ")
        # Sort users based on their scores in descending order
        rankings = sorted(user_credentials.items(), key=lambda x: x[1]['score'], reverse=True)
        
        # Create a message with the rankings
        rankings_message = "User Rankings:\n"
        print(rankings_message)
        for rank, (username, info) in enumerate(rankings, start=1):
            rankings_message += f"{rank}. {username}: {info['score']} points\n"
            print(rankings_message)
        
        # Send the rankings message to the client
        client_socket.send(rankings_message.encode('ascii'))
    except Exception as e:
        print(f"An error occurred while displaying rankings: {e}")
        client_socket.send("An error occurred while displaying rankings.".encode('ascii'))



def handle_menu(client_socket):
    menu = """
    1. Start Random Match
    2. Send Game Invite
    3. Accept Game Invite
    4. Quit
    """
    client_socket.send(menu.encode())

def handle_random_match(client_socket,username):
    
    print(f"USERNAME IS {username}")
    if len(queue) == 0:
        queue.append((client_socket, username))
        while len(queue)<2:
            continue
        queue.pop(0)
        queue.pop(0)

    else:
        
        client_socket1 ,username1  = client_socket ,username
        print("Sending Match to Client 1")
        client_socket1.send("Match".encode('ascii'))

        client_socket2,username2 = queue.pop(0)
        print("Sending Match to Client 2")
        client_socket2.send("Match".encode('ascii'))

        #print(client_socket1)
        #print(client_socket2)

        # Wait for choice from client_socket1
        print("Waiting for choice from Client 1...")
        choice1 = client_socket1.recv(1024).decode()
        #print(f"Choice 1: {choice1}")

        print(client_socket1)
        print(client_socket2)

        # Wait for choice from client_socket2
        print("Waiting for choice from Client 2...")
        choice2 = client_socket2.recv(1024).decode()
        #print(f"Choice 2: {choice2}")

        if choice1 == choice2:
            result = "It's a tie!"
        elif (choice1 == "rock" and choice2 == "scissors") or (choice1 == "scissors" and choice2 == "paper") or (choice1 == "paper" and choice2 == "rock"):
            result = "Client 1 wins!"
        else:
            result = "Client 2 wins!"
        #threading.Thread(target=handle_client, args=(client_socket1, "Client 1")).start()
        if result == "Client 1 wins!":
            client_socket1.send("\033[32mYou WON YEY\033[0m".encode('ascii'))
            client_socket2.send("\033[31mYou lost :(\033[0m".encode('ascii'))
            user_credentials[username1]['score'] += 5
            user_credentials[username2]['score'] -= 2
        elif result == "Client 2 wins!":
            client_socket1.send("\033[31mYou lost :(\033[0m".encode('ascii'))
            client_socket2.send("\033[32mYou WON YEY\033[0m".encode('ascii'))
            user_credentials[username1]['score'] += 5
            user_credentials[username2]['score'] -= 2
        else:
            client_socket1.send(result.encode('ascii'))
            client_socket2.send(result.encode('ascii'))
            user_credentials[username1]['score'] += 1
            user_credentials[username2]['score'] += 1

        queue.append("coucou")
        queue.append("hello")
            
        '''threading.Thread(target=handle_client, args=(client_socket1, "Client 1")).start()
        threading.Thread(target=handle_client, args=(client_socket2, "Client 2")).start()'''


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
                
                if username in user_credentials and user_credentials[username]['password'] == password and user_credentials[username]['status'] == "Offline" :
                    client_socket.send("Login successful!".encode('ascii'))
                    print(f"{username} logged in successfully.")
                    client_socket.send('menu'.encode('ascii'))
                    threading.Thread(target=handle_client, args=(client_socket, username)).start()
                else:
                    client_socket.send("Invalid credentials. Connection closed.".encode('ascii'))
                    print(f"Failed login attempt for username: {username}")
                    client_socket.send('bye'.encode('ascii'))
                    client_socket.close()

            elif L_S.lower() == 'signup':
                client_socket.send('Username: '.encode('ascii'))
                username = client_socket.recv(1024).decode('ascii').strip()
                
                if username in user_credentials:
                    client_socket.send("Username already taken. Connection closed.".encode('ascii'))
                    print(f"Username already taken: {username}")
                    client_socket.send('bye'.encode('ascii'))
                    client_socket.close()
                else:
                    client_socket.send('Password: '.encode('ascii'))
                    password = client_socket.recv(1024).decode('ascii').strip()
                    
                    user_credentials[username] = {'password': password, 'score': 0, 'last_attempt': None , 'client': client_socket ,"status" : "Online" , 'Invite_statuts':None , "result": None ,'Invt_From':None ,"Invt_To" : None}
                    client_socket.send("Signup successful!".encode('ascii'))
                    print(f"New user registered: {username}")
                    
                    threading.Thread(target=handle_client, args=(client_socket, username)).start()
        
        except Exception as e:
            
            client_socket.close()

def shutdown_server():
    print("Server is shutting down...")
    for client in clients:
        client.close()  
    server.close()
    sys.exit() 


def listen_for_shutdown():
    while True:
        
        command = input()
        if command == '/shutdown':
            print("Shutdown command received from server console.")
            shutdown_server()
            break  

command_thread = threading.Thread(target=listen_for_shutdown)
command_thread.start()
start()
