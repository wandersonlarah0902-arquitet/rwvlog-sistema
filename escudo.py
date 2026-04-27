import psutil
import socket

print("-" * 50)
print("SISTEMA DE MONITORAMENTO RWV-TECH")
print("-" * 50)

# Coletando conexões de rede
conexoes = psutil.net_connections(kind='inet')

print(f"{'PROCESSO':<20} | {'IP LOCAL':<20} | {'IP REMOTO':<20} | {'STATUS'}")
print("-" * 80)

for conn in conexoes:
    # Obtendo o nome do programa que está usando a conexão
    try:
        processo = psutil.Process(conn.pid).name()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        processo = "Desconhecido"

    laddr = f"{conn.laddr.ip}:{conn.laddr.port}"
    raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "Aguardando"
    
    # Filtra apenas conexões estabelecidas (ativas)
    if conn.status == 'ESTABLISHED':
        print(f"{processo[:20]:<20} | {laddr:<20} | {raddr:<20} | {conn.status}")

print("-" * 80)
print("Se houver IPs estranhos (como de outros países), devemos investigar o processo.")
