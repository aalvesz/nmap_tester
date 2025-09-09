import socket
import threading
import time
from queue import Queue
import select
import platform
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# Documentação:
# Script de varredura de portas TCP/UDP com interface gráfica aprimorada.
# Usa ttk para widgets modernos, barra de progresso, e botões para salvar/limpar resultados.
# Compatível com Linux e Windows, com timeout dinâmico (2s Windows, 1s Linux).
# Executar com sudo (Linux) ou como administrador (Windows) para UDP mais preciso.

# Ajuste de timeout baseado no sistema operacional
TIMEOUT = 2 if platform.system() == "Windows" else 1

def tcp_scan(host, port, results):
    """
    Realiza varredura TCP em uma porta específica.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(TIMEOUT)
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
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)
    try:
        sock.sendto(b'', (host, port))
        readable, _, _ = select.select([sock], [], [], TIMEOUT)
        if readable:
            data, _ = sock.recvfrom(1024)
            if data:
                results[port] = "Aberta"
            else:
                results[port] = "Fechada"
        else:
            results[port] = "Aberta/Filtrada"
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

def scan_ports(hosts, ports, scan_type='both', threads=10):
    """
    Função principal para varredura.
    """
    results = {}
    for host in hosts:
        results[host] = {'tcp': {}, 'udp': {}}
        queue = Queue()
        for port in ports:
            queue.put(port)
        
        thread_list = []
        for _ in range(threads):
            t = threading.Thread(target=worker, args=(host, queue, results[host], scan_type))
            t.daemon = True
            t.start()
            thread_list.append(t)
        
        queue.join()
    
    return results

def parse_ports(ports_str):
    """
    Parseia string de portas: ex: '1-100,443,8080'
    """
    ports = []
    try:
        for part in ports_str.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                ports.extend(range(start, end + 1))
            else:
                ports.append(int(part))
        return ports
    except ValueError:
        raise ValueError("Formato de portas inválido. Use ex: 1-100,443,8080")

def run_scan():
    """
    Executa a varredura a partir da GUI.
    """
    try:
        host = entry_host.get().strip()
        ports = entry_ports.get().strip()
        scan_type = var_type.get()
        threads = int(entry_threads.get().strip())
        
        if not host or not ports:
            messagebox.showerror("Erro", "Preencha os campos de host e portas!")
            return
        
        text_results.delete(1.0, tk.END)
        text_results.insert(tk.END, "Iniciando varredura...\n")
        progress_bar.start()
        root.update()
        
        start_time = time.time()
        hosts = host.split(',')
        ports_list = parse_ports(ports)
        results = scan_ports(hosts, ports_list, scan_type, threads)
        
        text_results.delete(1.0, tk.END)
        for host, host_results in results.items():
            text_results.insert(tk.END, f"\nResultados para {host}:\n", "header")
            if scan_type in ['tcp', 'both']:
                text_results.insert(tk.END, "Resultados TCP:\n", "subheader")
                for port, status in sorted(host_results['tcp'].items()):
                    text_results.insert(tk.END, f"Porta {port}: {status}\n", "result")
            if scan_type in ['udp', 'both']:
                text_results.insert(tk.END, "Resultados UDP:\n", "subheader")
                for port, status in sorted(host_results['udp'].items()):
                    text_results.insert(tk.END, f"Porta {port}: {status}\n", "result")
        
        text_results.insert(tk.END, f"\nVarredura concluída em {time.time() - start_time:.2f} segundos.\n", "footer")
        progress_bar.stop()
    except ValueError as e:
        progress_bar.stop()
        messagebox.showerror("Erro", str(e))
    except Exception as e:
        progress_bar.stop()
        messagebox.showerror("Erro", f"Erro durante a varredura: {str(e)}")

def save_results():
    """
    Salva os resultados em um arquivo.
    """
    try:
        with open("scan_results.txt", "w") as f:
            f.write(text_results.get(1.0, tk.END))
        messagebox.showinfo("Sucesso", "Resultados salvos em scan_results.txt")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

def clear_results():
    """
    Limpa a área de resultados.
    """
    text_results.delete(1.0, tk.END)

# Interface gráfica com Tkinter e ttk
root = tk.Tk()
root.title("Port Scanner")
root.geometry("600x600")
root.minsize(500, 400)  # Tamanho mínimo para redimensionamento
root.configure(bg="#f0f0f0")  # Fundo claro

# Aplicar tema ttk
style = ttk.Style()
style.theme_use("clam")  # Tema moderno (clam, alt, ou default)
style.configure("T.Label", font=("Helvetica", 10), background="#f0f0f0")
style.configure("T.Button", font=("Helvetica", 10, "bold"))
style.configure("T.Radiobutton", font=("Helvetica", 10), background="#f0f0f0")

# Frame para entradas
frame_inputs = ttk.Frame(root)
frame_inputs.pack(pady=10, padx=10, fill="x")

# Campo Host
ttk.Label(frame_inputs, text="Host(s) (ex: 127.0.0.1,192.168.1.1):").grid(row=0, column=0, sticky="w", pady=5)
entry_host = ttk.Entry(frame_inputs, width=50)
entry_host.grid(row=0, column=1, pady=5, padx=5)

# Campo Portas
ttk.Label(frame_inputs, text="Portas (ex: 1-100,443,8080):").grid(row=1, column=0, sticky="w", pady=5)
entry_ports = ttk.Entry(frame_inputs, width=50)
entry_ports.grid(row=1, column=1, pady=5, padx=5)

# Tipo de varredura
ttk.Label(frame_inputs, text="Tipo de varredura:").grid(row=2, column=0, sticky="w", pady=5)
var_type = tk.StringVar(value="both")
ttk.Radiobutton(frame_inputs, text="TCP", variable=var_type, value="tcp").grid(row=2, column=1, sticky="w")
ttk.Radiobutton(frame_inputs, text="UDP", variable=var_type, value="udp").grid(row=3, column=1, sticky="w")
ttk.Radiobutton(frame_inputs, text="Ambos", variable=var_type, value="both").grid(row=4, column=1, sticky="w")

# Campo Threads
ttk.Label(frame_inputs, text="Threads (ex: 10):").grid(row=5, column=0, sticky="w", pady=5)
entry_threads = ttk.Entry(frame_inputs, width=10)
entry_threads.insert(0, "10")
entry_threads.grid(row=5, column=1, sticky="w", pady=5, padx=5)

# Frame para botões
frame_buttons = ttk.Frame(root)
frame_buttons.pack(pady=10)

# Botões
ttk.Button(frame_buttons, text="Iniciar Varredura", command=run_scan).pack(side="left", padx=5)
ttk.Button(frame_buttons, text="Limpar Resultados", command=clear_results).pack(side="left", padx=5)
ttk.Button(frame_buttons, text="Salvar Resultados", command=save_results).pack(side="left", padx=5)

# Barra de progresso
progress_bar = ttk.Progressbar(root, mode="indeterminate")
progress_bar.pack(pady=5, fill="x", padx=10)

# Área de resultados
text_results = scrolledtext.ScrolledText(root, width=60, height=20, font=("Courier", 10), bg="#ffffff", fg="#333333")
text_results.pack(pady=10, padx=10, fill="both", expand=True)

# Configurar tags para estilização de texto
text_results.tag_configure("header", font=("Helvetica", 12, "bold"), foreground="#2e7d32")
text_results.tag_configure("subheader", font=("Helvetica", 10, "bold"), foreground="#1565c0")
text_results.tag_configure("result", font=("Courier", 10))
text_results.tag_configure("footer", font=("Helvetica", 10, "italic"), foreground="#555555")

# Iniciar a aplicação
root.mainloop()