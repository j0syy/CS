import time
import logging

# Configurar registro de eventos
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class IPSecPacket:
    def __init__(self, src_ip, dest_ip, payload, seq_num):
        self.src_ip = src_ip
        self.dest_ip = dest_ip
        self.payload = payload
        self.seq_num = seq_num
        self.mode = None
        self.encapsulated_header = None

class IPSecSimulator:
    def __init__(self):
        self.received_seqs = set() # Registro de números de secuencia recibidos
        self.max_window_size = 64
        self.last_valid_seq = 0

    def transport_mode_encrypt(self, packet):
        packet.mode = "Transporte"
        logging.info(f"[IPSec TRANSPORTE] Protegiendo payload de {packet.src_ip} a {packet.dest_ip} (Seq: {packet.seq_num})")
        return packet

    def tunnel_mode_encrypt(self, packet):
        packet.mode = "Túnel"
        packet.encapsulated_header = {"gateway_src": "200.100.50.1", "gateway_dest": "200.100.50.2"}
        logging.info(f"[IPSec TÚNEL] Paquete encapsulado. Gateway Origen: {packet.encapsulated_header['gateway_src']} -> Destino: {packet.encapsulated_header['gateway_dest']} (Seq: {packet.seq_num})")
        return packet

    def receive_packet(self, packet):
        # Mecanismo de defensa Anti-Replay
        if packet.seq_num in self.received_seqs:
            logging.warning(f"[¡ALERTA REPLAY!] Paquete duplicado con secuencia {packet.seq_num}. ¡DESCARTADO!")
            return False
        
        if packet.seq_num <= self.last_valid_seq - self.max_window_size:
            logging.warning(f"[¡ALERTA REPLAY!] Paquete fuera de ventana (muy antiguo). Seq: {packet.seq_num}. ¡DESCARTADO!")
            return False

        # Aceptar paquete legítimo
        self.received_seqs.add(packet.seq_num)
        if packet.seq_num > self.last_valid_seq:
            self.last_valid_seq = packet.seq_num
        
        logging.info(f"[ÉXITO] Paquete aceptado en modo {packet.mode}. Carga útil: '{packet.payload}'")
        return True

if __name__ == "__main__":
    print("--- SIMULACIÓN DE IPSEC Y PROTECCIÓN ANTI-REPLAY ---")
    sim = IPSecSimulator()

    # Paquetes legítimos iniciales
    p1 = IPSecPacket("192.168.1.10", "10.0.0.5", "Datos confidenciales A", 100)
    p2 = IPSecPacket("192.168.1.10", "10.0.0.5", "Datos confidenciales B", 101)

    # Probar Modo Transporte
    t_packet = sim.transport_mode_encrypt(p1)
    sim.receive_packet(t_packet)

    # Probar Modo Túnel
    tunnel_packet = sim.tunnel_mode_encrypt(p2)
    sim.receive_packet(tunnel_packet)

    # Simular ataque de Replay (reinyectar el paquete 100 previamente capturado)
    print("\n--- SIMULANDO ATAQUE DE REPLAY ---")
    replay_packet = IPSecPacket("192.168.1.10", "10.0.0.5", "Paquete malicioso reenviado", 100)
    replay_packet.mode = "Transporte"
    sim.receive_packet(replay_packet)