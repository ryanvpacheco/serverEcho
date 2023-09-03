import socket
import threading

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                break
            
            parts = data.strip().split(" ")  # Remova espaços em branco extras
            command = parts[0].lower()
            
            if command == "echo":
                message = " ".join(parts[1:])
                client_socket.send(message.encode("utf-8"))
                client_socket.send(b"\n")  # Adicione uma nova linha após a mensagem "echo"
            elif command == "exit" or command == "quit":  # Reconhece "exit" ou "quit"
                client_socket.send(b"Goodbye!")
                break  # Encerra o loop quando o comando "exit" ou "quit" é recebido
            else:
                client_socket.send(b"Unknown command")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 12345))
    server.listen(5)
    print("Server listening on port 12345")
    
    running = True
    
    try:
        while running:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr}")
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
    except KeyboardInterrupt:
        running = False
        server.close()
        print("Server stopped")

if __name__ == "__main__":
    main()
