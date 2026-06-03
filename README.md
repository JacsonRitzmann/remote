# 🖥️ Sistema de Acesso Remoto em Python

Este é um projeto didático de um sistema de controle e acesso remoto utilizando Python. O sistema é dividido em duas partes: um **Servidor** (máquina que será controlada) e um **Cliente** (máquina que controla e visualiza a tela).

## 🚀 Funcionalidades
* 📺 Transmissão de tela em tempo real (via OpenCV e PyAutoGUI).
* 🖱️ Controle remoto do mouse (movimentação e cliques).
* ⌨️ Controle remoto do teclado (letras e teclas especiais).

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter o **Python 3.x** instalado em ambas as máquinas.

### Dependências do Servidor (Máquina Controlada)
Abra o terminal ou prompt de comando na máquina servidora e instale:
```bash
pip install pyautogui opencv-python pillow
```

### Dependências do Cliente (Máquina Controladora)
Abra o terminal ou prompt de comando na máquina cliente e instale:
```bash
pip install opencv-python numpy pynput
```

---

## 📦 Como Instalar e Configurar

1. Crie uma pasta para o projeto.
2. Salve o código do servidor em um arquivo chamado `server.py`.
3. Salve o código do cliente em um arquivo chamado `client.py`.

### ⚠️ Configuração Importante de IP:
Antes de rodar, você precisa apontar o Cliente para o endereço IP correto do Servidor.

1. Na máquina **Servidora**, descubra o IP local dela:
   * **Windows**: Abra o CMD e digite `ipconfig` (procure por IPv4, ex: `192.168.1.50`).
   * **Linux/Mac**: Abra o terminal e digite `hostname -I`.
2. Abra o arquivo `client.py` na máquina **Cliente**.
3. Altere a linha 8 com o IP que você acabou de encontrar:
   ```python
   IP_SERVIDOR = '192.168.1.50' # Substitua pelo IP real do servidor
   ```
*(Nota: Se for testar ambos na mesma máquina, pode deixar como `'127.0.0.1'`).*

---

## 🛠️ Como Usar (Passo a Passo)

Siga rigorosamente a ordem abaixo para estabelecer a conexão:

### Passo 1: Iniciar o Servidor
Na máquina que **será controlada**, execute o script do servidor:
```bash
python server.py
```
O terminal exibirá a mensagem: `[*] Servidor controle total aguardando conexão na porta 9999...`

### Passo 2: Iniciar o Cliente
Na máquina **controladora**, execute o script do cliente:
```bash
python client.py
```

### Passo 3: Controlar
* Uma janela chamada **"Controle Remoto Ativo"** será aberta no Cliente exibindo a tela do Servidor.
* Mexa o mouse ou digite para enviar os comandos em tempo real.
* Para **encerrar a conexão**, clique na janela de vídeo e pressione a tecla **`ESC`**.

---

## 🛑 Resolução de Problemas Comuns

* **Erro de conexão recusada / Timeout**: Verifique se o Firewall do sistema operacional do Servidor não está bloqueando a porta `9999`. Se necessário, crie uma regra de entrada para essa porta ou desative o firewall temporariamente para testes.
* **O mouse clica no lugar errado**: Este script básico funciona melhor quando o computador Cliente e o Servidor possuem a **mesma resolução de tela** (ex: ambos 1920x1080). Caso as telas sejam diferentes, as coordenadas do mouse podem ficar desalinhadas.
* **Atraso (Lag) na imagem**: A velocidade depende da sua rede local. Você pode abrir o `server.py` e diminuir o valor do parâmetro `quality=50` (linha 22) para valores menores como `30` para reduzir o tamanho dos dados enviados.
