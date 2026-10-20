import logging
import os

LOG_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(LOG_DIR, "security.log")


CATEGORIAS = ("CONN", "AUTHN", "AUTHZ", "ADMIN", "TLS", "SSH", "VPN", "IPSEC")


ESTADOS_ALERTA = ("FAILED", "DENIED", "REJECTED", "ATTACK_DETECTED")

logger = logging.getLogger("SecurityAuditLogger")
logger.setLevel(logging.INFO)
logger.propagate = False  

formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

if not logger.handlers:
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def limpiar(x):
    return str(x).replace("\n", " ").replace("\r", " ").replace("|", "/")


def log_event(categoria, evento, usuario="-", ip="-", estado="INFO", detalle=""):

    categoria = categoria.upper()
    if categoria not in CATEGORIAS:
        raise ValueError(f"Categoria invalida: {categoria}. Usa una de {CATEGORIAS}")

    msg = (f"[{categoria}] | Event: {limpiar(evento)} | "
           f"User: {limpiar(usuario)} | IP: {limpiar(ip)} | "
           f"Status: {limpiar(estado)} | Details: {limpiar(detalle)}")


    if str(estado).upper() in ESTADOS_ALERTA:
        logger.warning(msg)
    else:
        logger.info(msg)


if __name__ == "__main__":
    # Prueba rapida
    log_event("AUTHN", "LOGIN", usuario="ana", ip="10.0.0.5", estado="OK", detalle="VPN acceso remoto")
    log_event("AUTHZ", "ACCESO_RECURSO", usuario="ana", ip="10.0.0.5", estado="DENIED", detalle="recurso=db-finanzas")
    log_event("ADMIN", "NOTA", detalle="intento | de inyectar\nuna linea falsa")
