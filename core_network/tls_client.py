import socket
import ssl

def run_tls_client():
    host = '127.0.0.1'
    port = 8443
    
    # Configurar el contexto SSL del cliente cargando la CA raíz de confianza
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(cafile="pki/ca.crt")
    context.check_hostname = True # Valida que el hostname coincida con el certificado
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        print(f"[CLIENTE SEGURO TLS] Conectando de forma segura a {host}:{port}...")
        
        # 1. Conectar primero el socket TCP al servidor
        client_socket.connect((host, port))
        
        # 2. Envolver el socket conectado con TLS (aquí se realiza el Handshake y validación de la PKI)
        secure_socket = context.wrap_socket(client_socket, server_hostname="localhost")
        
        message = "Hola servidor, este mensaje viaja cifrado y protegido por TLS."
        print(f"Enviando: {message}")
        secure_socket.sendall(message.encode('utf-8'))
        
        response = secure_socket.recv(1024).decode('utf-8')
        print(f"[Respuesta del servidor seguro]: {response}")
        secure_socket.close()
        
    except ssl.SSLError as e:
        print(f"[-] ERROR DE VALIDACIÓN PKI/TLS: Certificado rechazado. Razón: {e}")
    except Exception as e:
        print(f"[-] Error de conexión: {e}")

if __name__ == "__main__":
    run_tls_client()