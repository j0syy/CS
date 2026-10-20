import socket

def run_client():
    host = '127.0.0.1'
    port = 8080
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    message = "Hola servidor, este mensaje viaja en texto plano y vulnerable."
    print(f"Cliente inseguro Enviando: {message}")
    client_socket.sendall(message.encode('utf-8'))
    
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Respuesta del servidor: {response}")
    client_socket.close()

if __name__ == "__main__":
    run_client()