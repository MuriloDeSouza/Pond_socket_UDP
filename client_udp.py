import socket

def udp_client():
    # Cria um socket UDP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    server_address = ('localhost', 12345)
    
    try:
        while True:
            message = input("Digite uma mensagem (ou 'sair' para encerrar): ")
            if message.lower() == 'sair':
                break
                
            # Envia dados
            client_socket.sendto(message.encode(), server_address)
            
            # Recebe resposta
            data, server = client_socket.recvfrom(4096)
            print(f"Resposta do servidor: {data.decode()}")
            
    finally:
        client_socket.close()
        print("Cliente encerrado.")

if __name__ == "__main__":
    udp_client()