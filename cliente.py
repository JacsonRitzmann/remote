import socket
import struct
import cv2
import numpy as np
import json
from pynput import mouse, keyboard

IP_SERVIDOR = '127.0.0.1' # Altere para o IP do Servidor
PORTA = 9999

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((IP_SERVIDOR, PORTA))
print(f"[*] Conectado ao controle de {IP_SERVIDOR}")

# Funções para capturar seus eventos locais e enviar para o servidor
def ao_mover(x, y):
    try:
        cmd = json.dumps({"tipo": "mouse_move", "x": x, "y": y}) + "\n"
        cliente.sendall(cmd.encode('utf-8'))
    except: return False

def ao_clicar(x, y, botao, pressionado):
    if pressionado:
        try:
            btn_str = "left" if botao == mouse.Button.left else "right"
            cmd = json.dumps({"tipo": "mouse_click", "x": x, "y": y, "botao": btn_str}) + "\n"
            cliente.sendall(cmd.encode('utf-8'))
        except: return False

def ao_pressionar(tecla):
    try:
        if hasattr(tecla, 'char') and tecla.char is not None:
            cmd = json.dumps({"tipo": "teclado", "texto": tecla.char}) + "\n"
        else:
            # Converte teclas como enter, espaço, backspace
            nome_tecla = tecla.name
            cmd = json.dumps({"tipo": "tecla_especial", "tecla": nome_tecla}) + "\n"
        cliente.sendall(cmd.encode('utf-8'))
    except: return False

# Inicia os listeners de mouse e teclado em segundo plano
ouvinte_mouse = mouse.Listener(on_move=ao_mover, on_click=ao_clicar)
ouvinte_teclado = keyboard.Listener(on_press=ao_pressionar)
ouvinte_mouse.start()
ouvinte_teclado.start()

# Loop principal para receber e desenhar a tela recebida
dados_recebidos = b""
tamanho_cabecalho = struct.calcsize('>I')

try:
    while True:
        while len(dados_recebidos) < tamanho_cabecalho:
            dados_recebidos += cliente.recv(4096)
        cabecalho_tamanho = dados_recebidos[:tamanho_cabecalho]
        dados_recebidos = dados_recebidos[tamanho_cabecalho:]
        tamanho_imagem = struct.unpack('>I', cabecalho_tamanho)[0]
        
        while len(dados_recebidos) < tamanho_imagem:
            dados_recebidos += cliente.recv(4096)
        dados_imagem = dados_recebidos[:tamanho_imagem]
        dados_recebidos = dados_recebidos[tamanho_imagem:]
        
        vetor_numpy = np.frombuffer(dados_imagem, dtype=np.uint8)
        frame = cv2.imdecode(vetor_numpy, cv2.IMREAD_COLOR)
        
        if frame is not None:
            cv2.imshow("Controle Remoto Ativo", frame)
            
        if cv2.waitKey(1) == 27: # ESC para sair
            break
finally:
    ouvinte_mouse.stop()
    ouvinte_teclado.stop()
    cliente.close()
    cv2.destroyAllWindows()