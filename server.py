import socket
import pyautogui
import io
import struct
import json
import threading

# Evita travar o mouse nas bordas da tela
pyautogui.FAILSAFE = False

HOST = '0.0.0.0'
PORTA = 9999

# Thread para enviar a tela continuamente
def enviar_tela(conexao):
    try:
        while True:
            # Captura a tela (qualidade 50 para reduzir lag)
            printScreen = pyautogui.screenshot()
            fluxo_bytes = io.BytesIO()
            printScreen.save(fluxo_bytes, format='JPEG', quality=50)
            dados_imagem = fluxo_bytes.getvalue()
            
            # Envia o tamanho seguido dos dados da imagem
            conexao.sendall(struct.pack('>I', len(dados_imagem)) + dados_imagem)
    except:
        pass

# Thread para receber comandos do cliente (mouse e teclado)
def receber_comandos(conexao):
    dados_acumulados = ""
    try:
        while True:
            pacote = conexao.recv(1024).decode('utf-8')
            if not pacote:
                break
            dados_acumulados += pacote
            
            # Processa comandos separados por quebra de linha
            while "\n" in dados_acumulados:
                linha, dados_acumulados = dados_acumulados.split("\n", 1)
                if not linha.strip():
                    continue
                
                comando = json.loads(linha)
                tipo = comando.get("tipo")
                
                if tipo == "mouse_move":
                    pyautogui.moveTo(comando["x"], comando["y"])
                elif tipo == "mouse_click":
                    pyautogui.click(comando["x"], comando["y"], button=comando["botao"])
                elif tipo == "teclado":
                    pyautogui.write(comando["texto"])
                elif tipo == "tecla_especial":
                    pyautogui.press(comando["tecla"])
    except:
        pass

# Inicialização do Servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORTA))
server.listen(1)
print(f"[*] Servidor controle total aguardando conexão na porta {PORTA}...")

conexao, cliente_ip = server.accept()
print(f"[*] Conectado por: {cliente_ip}")

# Cria sockets separados para dados visuais e comandos
# (Para simplificar o código de estudo, usamos a mesma conexão para receber comandos)
t1 = threading.Thread(target=enviar_tela, args=(conexao,), daemon=True)
t2 = threading.Thread(target=receber_comandos, args=(conexao,), daemon=True)

t1.start()
t2.start()

# Mantém o script principal vivo
t1.join()
t2.join()
conexao.close()
server.close()