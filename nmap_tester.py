import socket
import threading
import argparse
from queue import Queue
import time
import struct
import select

# Documentação mínima:
# Este script realiza varredura de portas TCP e UDP em um ou mais endereços IP.
# Para TCP: Usa scan de conexão completa (connect scan), que não requer privilégios root.
# Para UDP: Envia um pacote UDP vazio e verifica se há resposta ou timeout (pode não ser 100% preciso devido à natureza do UDP).
# Executar em Linux como usuário root para melhores resultados em UDP, mas TCP funciona sem root.
# Uso: python port_scanner.py --host <IP> --ports <1-1024> --type <tcp/udp/both> --threads <num_threads>

def tcp_scan(host, port, results):
    """
    Realiza varredura TCP em uma porta específica.
    - Tenta conectar à porta; se sucesso, aberta.
    - Se falha, fechada ou filtrada (não distingue perfeitamente).
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Timeout de 1 segundo
    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            results[port] = "Aberta"
        else:
            results[port] = "Fechada/Filtrada"
    except Exception:
        results[port] = "Fechada/Filtrada"
    finally:
        sock.close()

def udp_scan(host, port, results):
    """
    Realiza varredura UDP em uma porta específica.
    - Envia pacote UDP vazio.
    - Se recebe ICMP port unreachable, fechada.
    - Se timeout sem resposta, aberta/filtrada (UDP não envia ACK).
    - Requer raw sockets para ICMP, mas aqui usamos select para simplicidade.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    try:
        sock.sendto(b'', (host, port))
        readable, _, _ = select.select([sock], [], [], 1)
        if readable:
            data, _ = sock.recvfrom(1024)
            if data:
                results[port] = "Aberta"  # Resposta recebida
            else:
                results[port] = "Fechada"
        else:
            results[port] = "Aberta/Filtrada"  # Timeout, pode ser aberta
    except socket.timeout:
        results[port] = "Aberta/Filtrada"
    except Exception:
        results[port] = "Fechada/Filtrada"
    finally:
        sock.close()

def worker(host, queue, results, scan_type):
    """
    Thread worker para processar portas da fila.
    """
    while not queue.empty():
        port = queue.get()
        if scan_type == 'tcp' or scan_type == 'both':
            tcp_scan(host, port, results['tcp'])
        if scan_type == 'udp' or scan_type == 'both':
            udp_scan(host, port, results['udp'])
        queue.task_done()

def scan_ports(host, ports, scan_type='both', threads=10):
    """
    Função principal para varredura.
    - ports: lista de portas ou range (ex: range(1, 1025))
    - Suporta múltiplos hosts, mas aqui implementado para um; estender para lista.
    """
    results = {'tcp': {}, 'udp': {}}
    queue = Queue()
    for port in ports:
        queue.put(port)
    
    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker, args=(host, queue, results, scan_type))
        t.daemon = True
        t.start()
        thread_list.append(t)
    
    queue.join()
    
    return results

def print_results(results, scan_type):
    """
    Exibe os resultados da varredura.
    """
    if scan_type == 'tcp' or scan_type == 'both':
        print("\nResultados TCP:")
        for port, status in sorted(results['tcp'].items()):
            print(f"Porta {port}: {status}")
    if scan_type == 'udp' or scan_type == 'both':
        print("\nResultados UDP:")
        for port, status in sorted(results['udp'].items()):
            print(f"Porta {port}: {status}")

def parse_ports(ports_str):
    """
    Parseia string de portas: ex: '1-100,443,8080'
    """
    ports = []
    for part in ports_str.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))
    return ports

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ferramenta de varredura de portas TCP/UDP.")
    parser.add_argument('--host', required=True, help="Endereço IP ou hostname para varredura.")
    parser.add_argument('--ports', default='1-1024', help="Portas para varrer, ex: 1-1024,8080.")
    parser.add_argument('--type', default='both', choices=['tcp', 'udp', 'both'], help="Tipo de varredura: tcp, udp ou both.")
    parser.add_argument('--threads', type=int, default=10, help="Número de threads para paralelismo.")
    
    args = parser.parse_args()
    
    ports = parse_ports(args.ports)
    start_time = time.time()
    
    results = scan_ports(args.host, ports, args.type, args.threads)
    
    print_results(results, args.type)
    
    print(f"\nVarredura concluída em {time.time() - start_time:.2f} segundos.")