import socket

def udp_server():
    # Cria um socket UDP (SOCK_DGRAM)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Associa o socket a um endereço e porta
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)
    
    print(f"Servidor UDP ouvindo em {server_address}")
    
    try:
        while True:
            # Recebe dados e endereço do cliente
            data, client_address = server_socket.recvfrom(4096)
            print(f"Recebido {len(data)} bytes de {client_address}: {data.decode()}")
            
            # Envia resposta
            response = f"Eco: {data.decode()}"
            server_socket.sendto(response.encode(), client_address)
            
    except KeyboardInterrupt:
        print("Servidor encerrado.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    udp_server()