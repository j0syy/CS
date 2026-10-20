# Infraestructura de Comunicaciones Seguras

Este proyecto implementa y simula una arquitectura de seguridad de red para una pequeña organización, demostrando la aplicación de distintos mecanismos criptográficos y de control de acceso para proteger las comunicaciones en diferentes niveles.

## 1. Arquitectura Desarrollada

El sistema se diseñó bajo un modelo híbrido estructurado en módulos lógicos que separan las implementaciones reales a nivel de capa de aplicación de las simulaciones a nivel de red. La arquitectura opera sobre una red local (LAN) y se divide en cuatro componentes principales:

*   **Módulo PKI (`pki/`):** El ancla de confianza del sistema. Utiliza OpenSSL para establecer una Autoridad Certificadora (CA) propia que emite y firma criptográficamente los certificados digitales del servidor.
*   **Infraestructura Central (`core_network/`):** Implementa el modelo Cliente-Servidor real utilizando sockets TCP de Python y el módulo `ssl`. Se ejecuta en dos equipos físicos distintos, demostrando el establecimiento de un canal seguro extremo a extremo frente a un canal vulnerable en texto plano.
*   **Simulador de IPSec (`ipsec_sim/`):** Un motor basado en software que modela el comportamiento de la capa de red. Emula la encapsulación de paquetes (modos Transporte y Túnel) e implementa un mecanismo de defensa algorítmico (ventana deslizante) contra ataques de retransmisión (*Replay Attacks*).
*   **Sistema VPN y AAA (`vpn_system/`):** Modela el control perimetral. Incorpora un servidor de acceso remoto con Control de Acceso Basado en Roles (RBAC) y un enrutador lógico que encapsula tráfico para interconectar dos subredes distintas (VPN Sitio a Sitio), centralizando la auditoría en un archivo de registros (`logs/security.log`).

---

## 2. Instrucciones de Ejecución

Para desplegar y verificar el funcionamiento del sistema en un entorno de dos computadoras, sigue estos pasos:

### Fase A: Preparación y Generación de PKI (Computadora Servidor)
1. Abre una terminal (Git Bash o PowerShell) en la raíz del proyecto.
2. Ejecuta el script de OpenSSL para generar la Autoridad Certificadora y las llaves:
   ```bash
   ./generate_ca.sh
   ```
   *(Si usas PowerShell puro sin Git Bash, ejecuta los comandos de OpenSSL línea por línea indicados en la documentación).*

### Fase B: Configuración de Red para 2 Equipos
1. En la **Computadora Servidor**, averigua tu dirección IPv4 local (ej. `192.168.1.50`). 
2. Abre el archivo `core_network/tls_server.py` y asegúrate de que esté configurado para escuchar en la red local: `host = '0.0.0.0'`.
3. Copia el archivo de la autoridad certificadora (`pki/ca.crt`) y transfiérelo a la **Computadora Cliente**, guardándolo en la misma ruta relativa.
4. En la **Computadora Cliente**, abre `core_network/tls_client.py` y configura la variable `host` con la IP exacta de la computadora servidor.

### Fase C: Ejecución de las Pruebas de Seguridad
Abre distintas terminales para ejecutar cada módulo independiente:

*   **Prueba Cliente-Servidor y TLS (Requiere 2 PCs):**
    *   *Terminal Servidor:* `python core_network/tls_server.py`
    *   *Terminal Cliente:* `python core_network/tls_client.py`
*   **Prueba IPSec y Anti-Replay (Local):** 
    *   Ejecuta: `python ipsec_sim/ipsec_simulation.py`
*   **Prueba VPN y Control de Acceso (Local):** 
    *   Ejecuta: `python vpn_system/remote_vpn.py`
    *   Ejecuta: `python vpn_system/site_to_site.py`

---

## 3. Función de las Tecnologías Implementadas

*   **TLS (Transport Layer Security):** Se encarga de cifrar los datos en tránsito en la capa de aplicación/transporte. Garantiza la confidencialidad e integridad del mensaje para que no pueda ser leído ni modificado por intermediarios en la red local.
*   **PKI (Public Key Infrastructure):** Proporciona la validación de identidad. Evita ataques de intermediario (*Man-in-the-Middle*) asegurando que el cliente se conecte al servidor legítimo y no a un impostor, verificando la cadena de confianza.
*   **SSH (Secure Shell):** Permite a los administradores de sistemas acceder a la terminal del servidor de forma remota y segura. Reemplaza conexiones inseguras (como Telnet) mediante el uso de criptografía asimétrica.
*   **IPSec (Internet Protocol Security):** Asegura el tráfico IP en la capa de red. En **Modo Transporte**, cifra solo la carga útil de los datos. En **Modo Túnel**, encapsula el paquete IP original completo dentro de uno nuevo.
*   **VPN (Virtual Private Network):** Crea un túnel privado sobre una red pública. La **VPN de Acceso Remoto** permite a un empleado externo entrar a la red corporativa bajo una identidad verificada. La **VPN Sitio a Sitio** conecta de manera permanente dos sedes corporativas distintas.

---

## 4. Diferencias entre los Mecanismos

| Característica | TLS | IPSec / VPN | SSH |
| :--- | :--- | :--- | :--- |
| **Capa OSI** | Capa de Transporte / Aplicación (Capas 4-7). | Capa de Red (Capa 3). | Capa de Aplicación (Capa 7). |
| **Alcance de Protección** | Protege una conexión o sesión específica entre un cliente y un servidor (ej. navegador y servidor web). | Protege **todo** el tráfico de red que atraviesa el túnel, independientemente de la aplicación. | Protege una sesión de línea de comandos o transferencia administrativa de archivos. |
| **Transparencia** | Las aplicaciones deben estar programadas explícitamente para soportar TLS. | Es transparente para el usuario y las aplicaciones; el SO maneja el cifrado en segundo plano. | Requiere el uso explícito de un cliente SSH. |
| **Identidad** | Basada casi exclusivamente en Certificados Digitales (PKI). | Basada en claves precompartidas (PSK), certificados o protocolos IKE. | Basada en llaves públicas/privadas del usuario (RSA, Ed25519). |

---

## 5. Principales Limitaciones de Seguridad de la Solución

1.  **Naturaleza Simulada de la Capa de Red:** Los módulos de IPSec y VPN son abstracciones algorítmicas implementadas a nivel de aplicación en Python. No interactúan directamente con el kernel del sistema operativo ni modifican las interfaces de red físicas, por lo que no interceptan el tráfico real de la tarjeta de red.
2.  **Criptografía Falsa en Simuladores:** Mientras que el módulo TLS utiliza cifrado real mediante los algoritmos estándar de la industria, los módulos de IPSec y VPN del proyecto simplemente "etiquetan" las cadenas de texto simulando que están encapsuladas, pero no aplican un algoritmo de cifrado matemático (como AES) sobre las cargas útiles.
3.  **Gestión de Credenciales en Texto Plano:** En el script de la VPN de acceso remoto, las contraseñas de los usuarios están incrustadas directamente en el código fuente (`USERS_DB`). Una solución en producción requiere derivación de claves criptográficas (hashes como Argon2 o bcrypt) y almacenamiento seguro.
4.  **Confianza Local de la PKI:** La Autoridad Certificadora generada es autofirmada y de alcance local. Aunque es funcional para esta arquitectura de prueba, ningún sistema externo confiará en ella por defecto, ya que no pertenece a una entidad pública reconocida mundialmente (como Let's Encrypt o DigiCert).