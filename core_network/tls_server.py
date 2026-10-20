import socket
import ssl

def run_tls_server():
    host = '0.0.0.0'
    port = 8443
    
    # Configurar el contexto SSL para el servidor
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="pki/server.crt", keyfile="pki/server.key")
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    print(f"Escuchando en {host}:{port}...")
    
    while True:
        conn, addr = server_socket.accept()
        try:
            # Envolver el socket TCP estándar con la capa TLS
            secure_conn = context.wrap_socket(conn, server_side=True)
            print(f"Conexión segura TLS establecida con {addr}")
            print(f"Algoritmo de cifrado activo: {secure_conn.cipher()}")
            
            data = secure_conn.recv(1024).decode('utf-8')
            print(f"Recibido cifrado: {data}")
            
            response = "Mensaje recibido y protegido mediante TLS correctamente."
            secure_conn.sendall(response.encode('utf-8'))
            secure_conn.close()
        except ssl.SSLError as e:
            print(f"Error de negociación TLS con {addr}: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    run_tls_server()