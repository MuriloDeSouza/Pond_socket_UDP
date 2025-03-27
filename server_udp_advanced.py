import socket
import struct
import os

def calculate_udp_checksum(src_addr, dest_addr, protocol, udp_length, udp_header, data):
    """
    Calcula o checksum UDP conforme RFC 768
    """
    # Cria o pseudo-header
    pseudo_header = struct.pack('!4s4sBBH',
                               socket.inet_aton(src_addr),
                               socket.inet_aton(dest_addr),
                               0, protocol, udp_length)
    
    # Combina pseudo-header, UDP header e dados
    checksum_data = pseudo_header + udp_header + data
    
    # Preenche com zero se o tamanho for ímpar
    if len(checksum_data) % 2 != 0:
        checksum_data += b'\x00'
    
    # Calcula o checksum
    checksum = 0
    for i in range(0, len(checksum_data), 2):
        word = (checksum_data[i] << 8) + checksum_data[i+1]
        checksum += word
        checksum = (checksum & 0xffff) + (checksum >> 16)
    
    checksum = ~checksum & 0xffff
    return checksum if checksum != 0 else 0xffff  # Conforme RFC, zero é enviado como todos 1s

def udp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('0.0.0.0', 12345)  # Escuta em todas as interfaces
    server_socket.bind(server_address)
    
    print(f"Servidor UDP avançado ouvindo em {server_address}")
    print(f"PID do servidor: {os.getpid()}")

    try:
        while True:
            # Recebe datagrama
            data, client_address = server_socket.recvfrom(65535)
            
            # Exibe informações do cabeçalho (disponíveis via getsockname e client_address)
            print(f"\nRecebido {len(data)} bytes de {client_address}")
            print(f"Porta local (servidor): {server_socket.getsockname()[1]}")
            print(f"Porta remota (cliente): {client_address[1]}")
            
            # Exibe os dados recebidos completos
            print(f"Dados recebidos: {data.decode()}")
            
            # Prepara resposta
            response_data = f"Resposta do servidor PID {os.getpid()}".encode()
            
            # Calcula checksum manualmente para fins educacionais
            src_port = server_socket.getsockname()[1]
            dest_port = client_address[1]
            length = 8 + len(response_data)
            checksum = 0
            
            # Monta cabeçalho UDP fictício para cálculo do checksum
            udp_header = struct.pack('!HHHH', 
                                src_port, 
                                dest_port, 
                                length, 
                                checksum)
            
            # Calcula checksum (para demonstração)
            checksum = calculate_udp_checksum(
                server_address[0], 
                client_address[0], 
                17,  # Protocolo UDP
                length, 
                udp_header, 
                response_data
            )
            
            print(f"\n[DEBUG] Cabeçalho UDP simulado:")
            print(f"- Porta origem: {src_port}")
            print(f"- Porta destino: {dest_port}")
            print(f"- Comprimento: {length}")
            print(f"- Checksum calculado: {checksum} (0x{checksum:04x})")
            
            # Envia resposta (deixando o kernel lidar com os cabeçalhos reais)
            server_socket.sendto(response_data, client_address)
            
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        server_socket.close() 
    

if __name__ == "__main__":
    udp_server()

########## funcionando também
# try:
#         while True:
#             # Recebe datagrama
#             data, client_address = server_socket.recvfrom(65535)
            
#             # Extrai porta de origem do cliente (assumindo que o cliente não usou porta zero)
#             src_port = struct.unpack('!H', data[:2])[0]
            
#             print(f"\nRecebido {len(data)} bytes de {client_address}")
#             # print(f"Porta de origem do cliente: {src_port}") -- comentando para plotar os 8 primeiros caracteres primeiros
#             print(f"Dados recebidos: {data[8:].decode()}")
            
#             # Verifica checksum (opcional)
#             # Na prática, o kernel já fez essa verificação
            
#             # Prepara resposta
#             response_data = f"Resposta do servidor PID {os.getpid()}".encode()
#             # print(f"Hex dump dos dados recebidos: {data.hex()}")
#             server_socket.sendto(response_data, client_address) # adicionando a resposta do servidor
            
#             # Monta cabeçalho UDP manualmente
#             src_port = 12345  # Nossa porta
#             dest_port = client_address[1]  # Porta do cliente
#             length = 8 + len(response_data)  # 8 bytes de cabeçalho + dados
#             checksum = 0  # Inicialmente zero para cálculo
            
#             udp_header = struct.pack('!HHHH', 
#                                    src_port, 
#                                    dest_port, 
#                                    length, 
#                                    checksum)
            
#             # Calcula checksum
#             checksum = calculate_udp_checksum(
#                 server_address[0], 
#                 client_address[0], 
#                 17,  # Protocolo UDP
#                 length, 
#                 udp_header, 
#                 response_data
#             )
            
#             # Recria header com checksum correto
#             udp_header = struct.pack('!HHHH', 
#                                    src_port, 
#                                    dest_port, 
#                                    length, 
#                                    checksum)
            
#             # Envia pacote completo
#             server_socket.sendto(udp_header + response_data, client_address)
            
#     except KeyboardInterrupt:
#         print("\nServidor encerrado.")
#     finally:
#         server_socket.close()


# try:
#         while True:
#             # Recebe datagrama - o kernel já processou os cabeçalhos
#             data, client_address = server_socket.recvfrom(65535)
            
#             print(f"\nRecebido {len(data)} bytes de {client_address}")
#             print(f"Dados recebidos completos: {data.decode()}")  # Mostra todos os dados
            
#             # Prepara resposta - o kernel vai adicionar os cabeçalhos automaticamente
#             response_data = f"Resposta do servidor PID {os.getpid()}".encode()
            
#             # Envia apenas os dados - cabeçalhos são tratados pelo kernel
#             server_socket.sendto(response_data, client_address)
        
#     except KeyboardInterrupt:
#         print("\nServidor encerrado.")
#     finally:
#         server_socket.close()