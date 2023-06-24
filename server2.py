#!/bin/python3
import socket
import threading


# Данные подключения
host = '127.0.0.1'
port = 55555


# Запуск сервера
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


# Списки клиентов и их никнеймов
clients = {}  # Используем словарь вместо списка для удобства доступа
nicknames = {}


# Отправка сообщений всем подключенным клиентам
def broadcast(message):
    for client_socket in clients.values():
        client_socket.send(message)


# Обработка сообщений от клиентов
def handle(client_socket):
    while True:
        try:
            # Передача сообщений всем клиентам
            message = client_socket.recv(1024)
            broadcast(message)
        except:
            # Удаление и закрытие клиента
            nickname = nicknames[client_socket]
            del clients[client_socket]
            del nicknames[client_socket]
            client_socket.close()
            broadcast('{} покинул чат!'.format(nickname).encode('utf-8'))
            break


# Функция приема подключений
def receive():
    while True:
        # Принятие подключения
        client_socket, address = server.accept()
        print("Подключено: {}".format(str(address)))

        # Запрос и сохранение никнейма
        client_socket.send('NICK'.encode('utf-8'))
        nickname = client_socket.recv(1024).decode('utf-8')
        nicknames[client_socket] = nickname
        clients[client_socket] = client_socket

        # Печать и передача никнейма всем клиентам
        print("Никнейм: {}".format(nickname))
        broadcast("{} присоединился!".format(nickname).encode('utf-8'))
        client_socket.send('Подключено к серверу!'.encode('utf-8'))

        # Запуск потока для обработки клиента
        thread = threading.Thread(target=handle, args=(client_socket,))
        thread.start()


print("Сервер ожидает подключений...")
receive()
