import socket
import struct
import os

def udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Permite que o sistema escolha uma porta disponível (porta zero)
    client_socket.bind(('0.0.0.0', 0))
    
    server_address = ('localhost', 12345)
    
    print(f"Cliente UDP avançado iniciado na porta {client_socket.getsockname()[1]}")
    print(f"PID do cliente: {os.getpid()}")
    print("Digite mensagens para enviar ao servidor (ou 'sair' para encerrar)")
    
    try:
        while True:
            message = input("> ")
            if message.lower() == 'sair':
                break
                
            # Monta datagrama UDP manualmente
            src_port = client_socket.getsockname()[1]  # Nossa porta
            dest_port = server_address[1]  # Porta do servidor
            length = 8 + len(message.encode())  # 8 bytes de cabeçalho + dados
            checksum = 0  # Inicialmente zero para cálculo
            
            udp_header = struct.pack('!HHHH', 
                                   src_port, 
                                   dest_port, 
                                   length, 
                                   checksum)
            
            data = message.encode()
            
            # Calcula checksum (opcional - o kernel geralmente faz isso)
            # checksum = calculate_udp_checksum(...)
            # Na prática, vamos deixar o kernel lidar com isso
            
            # Envia mensagem (o kernel calculará o checksum)
            client_socket.sendto(data, server_address)
            
            # Recebe resposta
            response, server = client_socket.recvfrom(4096)
            print(f"Resposta do servidor: {response[8:].decode()}")
            
    finally:
        client_socket.close()
        print("Cliente encerrado.")

if __name__ == "__main__":
    udp_client()