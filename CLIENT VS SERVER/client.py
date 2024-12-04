import socket

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

while True:
    choice = input("Enter paper, rock, or scissors (or type 'quit' to exit): ").strip().lower()

    if choice == "quit":
        break

    if choice not in ["paper", "rock", "scissors"]:
        print("Invalid choice. Please try again.")
        continue

    client.sendall(choice.encode())
    response = client.recv(1024).decode()
    print(response)

client.close()
