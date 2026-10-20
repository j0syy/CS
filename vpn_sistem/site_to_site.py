import logging

class SiteToSiteVPNGateway:
    def __init__(self, site_name, local_subnet, remote_gateway_ip):
        self.site_name = site_name
        self.local_subnet = local_subnet
        self.remote_gateway_ip = remote_gateway_ip

    def send_packet(self, src_ip, dest_ip, data, peer_gateway):
        print(f"\n[{self.site_name}] Tráfico originado en {src_ip} con destino a {dest_ip}")
        
        # Verificar si el destino pertenece a la red remota de la sucursal (ej. red 10.200.x.x)
        if dest_ip.startswith("10.200."):
            print(f"[{self.site_name}] Destino remoto detectado. Redirigiendo al túnel VPN corporativo...")
            
            # Encapsulamiento del paquete en el túnel VPN sitio a sitio
            tunnel_packet = {
                "outer_src": self.local_subnet,
                "outer_dest": self.remote_gateway_ip,
                "inner_payload": data,
                "tunnel_active": True
            }
            print(f"[{self.site_name}] Paquete cifrado y enviado al Gateway remoto ({self.remote_gateway_ip})")
            peer_gateway.receive_tunnel_packet(tunnel_packet, dest_ip)
        else:
            print(f"[{self.site_name}] El tráfico pertenece a la red local.")

    def receive_tunnel_packet(self, tunnel_packet, final_dest):
        print(f"\n[{self.site_name}] Gateway receptor autenticó el paquete del túnel.")
        if tunnel_packet["tunnel_active"]:
            print(f"[{self.site_name}] Descifrando paquete IPsec Sitio a Sitio...")
            print(f"[{self.site_name}] Entregando al equipo destino interno: {final_dest} -> Contenido: '{tunnel_packet['inner_payload']}'")
        else:
            print(f"[{self.site_name}] Paquete descartado por falta de cifrado en el túnel.")

if __name__ == "__main__":
    print("--- SIMULACIÓN DE VPN SITIO A SITIO (Red Central <---> Red Sucursal) ---")
    
    # Inicializar pasarelas de ambas redes
    gateway_hq = SiteToSiteVPNGateway("Sede Central (HQ)", "192.168.10.1", "200.50.50.2")
    gateway_branch = SiteToSiteVPNGateway("Sucursal Remota", "10.200.50.1", "200.50.50.1")

    # Simular envío de datos desde la red central hacia la sucursal
    gateway_hq.send_packet(
        src_ip="192.168.10.15", 
        dest_ip="10.200.50.50", 
        data="Sincronización de registros contables de sucursal",
        peer_gateway=gateway_branch
    )