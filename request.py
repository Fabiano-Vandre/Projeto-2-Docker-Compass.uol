import requests
import threading
import time

# URL do seu Load Balancer
LOAD_BALANCER_URL = "http://LB-TESTE2-333342165.us-east-1.elb.amazonaws.com"

# Número total de requisições
TOTAL_REQUESTS = 30

# Número de threads simultâneas
NUM_THREADS = 10

def make_request():
    """Função que faz uma requisição GET ao Load Balancer"""
    try:
        response = requests.get(LOAD_BALANCER_URL, timeout=5)
        print(f"Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erro: {e}")

def start_load_test():
    """Cria múltiplas threads para enviar requisições simultâneas"""
    threads = []
    for _ in range(TOTAL_REQUESTS):
        thread = threading.Thread(target=make_request)
        thread.start()
        threads.append(thread)

        # Limitar a taxa de requisições
        if len(threads) >= NUM_THREADS:
            for t in threads:
                t.join()  # Espera as threads terminarem
            threads = []  # Limpa a lista para criar novas threads

    # Espera todas as threads finalizarem
    for t in threads:
        t.join()

if __name__ == "__main__":
    print(f"Iniciando teste de carga em {LOAD_BALANCER_URL} com {TOTAL_REQUESTS} requisições.")
    start_time = time.time()
    
    start_load_test()
    
    print(f"Teste concluído em {time.time() - start_time:.2f} segundos.")
