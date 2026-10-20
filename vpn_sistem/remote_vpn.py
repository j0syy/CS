import logging
import os

# Configuración del registro de auditoría (AAA)
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/security.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Base de datos simulada de usuarios, credenciales y roles
USERS_DB = {
    "admin_user": {"password": "AdminPassword123", "role": "admin", "virtual_ip": "10.8.0.2"},
    "operator_user": {"password": "OpPassword123", "role": "operator", "virtual_ip": "10.8.0.3"},
    "guest_user": {"password": "GuestPassword123", "role": "guest", "virtual_ip": "10.8.0.4"}
}

# Matriz de Control de Acceso (RBAC)
RESOURCES = {
    "/api/server-config": ["admin"],
    "/api/restart-service": ["admin"],
    "/api/view-logs": ["admin", "operator"],
    "/api/public-dashboard": ["admin", "operator", "guest"]
}

class RemoteVPNServer:
    def authenticate(self, username, password):
        print(f"[AAA - AUTENTICACIÓN] Validando credenciales para: {username}")
        if username in USERS_DB and USERS_DB[username]["password"] == password:
            logging.info(f"AUTENTICACIÓN EXITOSA: Usuario '{username}' conectado desde IP externa.")
            print(f"[+] Autenticación exitosa. IP virtual asignada: {USERS_DB[username]['virtual_ip']}")
            return USERS_DB[username]
        else:
            logging.warning(f"AUTENTICACIÓN FALLIDA: Intento de acceso inválido para usuario '{username}'.")
            print(f"[-] Error de autenticación: Credenciales incorrectas.")
            return None

    def authorize_and_access(self, username, role, resource):
        print(f"[AAA - AUTORIZACIÓN] Evaluando permisos de '{username}' (Rol: {role}) sobre el recurso '{resource}'")
        
        if resource in RESOURCES:
            allowed_roles = RESOURCES[resource]
            if role in allowed_roles:
                logging.info(f"ACCESO PERMITIDO: Usuario '{username}' ({role}) accedió a {resource}")
                print(f"[+] Acceso CONCEDIDO al recurso {resource}\n")
                return True
            else:
                logging.warning(f"ACCESO DENEGADO: Usuario '{username}' ({role}) intentó acceder a recurso restringido {resource}")
                print(f"[-] Acceso DENEGADO: Tu rol ({role}) no cuenta con privilegios suficientes.\n")
                return False
        else:
            print(f"[-] Recurso no encontrado.\n")
            return False

if __name__ == "__main__":
    print("--- SIMULADOR DE VPN DE ACCESO REMOTO Y SISTEMA AAA ---")
    vpn = RemoteVPNServer()

    # Prueba 1: Usuario Operador intenta ver logs (Permitido) y luego configurar servidor (Denegado)
    session = vpn.authenticate("operator_user", "OpPassword123")
    if session:
        vpn.authorize_and_access("operator_user", session["role"], "/api/view-logs")
        vpn.authorize_and_access("operator_user", session["role"], "/api/server-config")

    # Prueba 2: Intento de autenticación fallida
    vpn.authenticate("admin_user", "ClaveFalsa")