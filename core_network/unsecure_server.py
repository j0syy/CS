import socket

def run_server():
    host = '127.0.0.1'
    port = 8080
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    print(f"SERVIDOR INSEGURO Escuchando en {host}:{port} (Sin cifrado)...")
    
    while True:
        conn, addr = server_socket.accept()
        print(f"Conexión entrante desde {addr}")
        
        # Recibe datos en texto plano
        data = conn.recv(1024).decode('utf-8')
        print(f"Recibido en texto plano: {data}")
        
        response = "Mensaje recibido sin protección."
        conn.sendall(response.encode('utf-8'))
        conn.close()

if __name__ == "__main__":
    run_server()