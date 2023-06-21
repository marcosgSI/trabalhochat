#Importa bibliotecas
import os
import socket
import threading
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

# instância do aplicativo Flask
app = Flask(__name__)
CORS(app,resources={r"/": {"origins": ""}})
# Inicializa uma lista de mensagens e um conjunto para os usuários conectados
messages = []
connected_users = set()

# Função para lidar com mensagens recebidas
def handle_message(data):
    # Exibe a mensagem recebida no console
    print('Mensagem recebida:', data)
    # Adiciona a mensagem à lista de mensagens
    messages.append(data)

# Rota de mensagens
@app.route('/messages')
def get_messages():
    # Retorna as mensagens como um objeto JSON
    return jsonify(messages)

# Rota de usuarios
@app.route('/connected_users', methods=['GET'])
def handle_connected_users():
    print(connected_users)
    if request.method == 'POST':
        username = request.json['username']
        connected_users.add(username)
        return jsonify(list(connected_users))
    else:
        return jsonify(list(connected_users))

# Rota de mensagens
@app.route('/messages', methods=['POST'])
def send_message():
    # Obtém os dados da mensagem do corpo da solicitação
    data = request.json
    # Inicia uma nova thread para lidar com a mensagem recebida

    # .start metodo para iniciar execução de uma nova thread
    threading.Thread(target=handle_message, args=(data,)).start()
    # Retorna os dados da mensagem como um objeto JSON
    return jsonify(data)

# Rota index
@app.route('/')
def index():
    # Renderiza o template HTML da página principal
    return render_template('index.html')

# Função para iniciar o servidor de sockets
def start_server():
    # instancia socket com parametros
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # binda socket
    server_socket.bind(('0.0.0.0', 5000))
    # Coloca o socket em modo listen(escuta)
    server_socket.listen()
    print('Servidor Online')
    # Laço para aceitar conexões de clientes
    while True:
        # Aceita uma conexão de cliente
        client_socket, client_address = server_socket.accept()
        # Inicia uma nova thread para lidar com a conexão do cliente
        threading.Thread(target=handle_cliente, args=(client_socket,)).start()

# def conexão do cliente
def handle_cliente(client_socket):
    # Loop para receber dados do cliente
    while True:
        # Recebe dados do cliente PELA FUNCAO RECV recebendo até 1024 bytes de dados do cliente através do client_socket
        data = client_socket.recv(1024)
        # Verifica se os dados recebidos estão vazios, indicando que o cliente se desconectou
        if not data:
            # Fecha o socket do cliente
            client_socket.close()
            # Encerra a função
            return
        message = data.decode().strip()
        # Inicia uma nova thread para lidar com a mensagem recebida
        threading.Thread(target=handle_message, args=(message,)).start()

# Função para executar o servidor Flask em uma thread separada
def servidor_flask():
    print('Iniciando servidor Flask')
    # Inicia o servidor Flask
    app.run(host='0.0.0.0', port=int(os.getenv('PORT')), debug=False)

if __name__ == '__main__':
    # Inicia duas threads separadas para executar o servidor Flask e lidar com conexões de clientes
    threading.Thread(target=servidor_flask, daemon=True).start()
    threading.Thread(target=start_server, daemon=True).start()  # Chama a função start_server() em uma nova thread

    # Loop infinito para manter o programa em execução
    while True:
        pass
