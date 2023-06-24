import socket
import threading

# Выбор никнейма
nickname = input("Выберите ваш псевдоним: ")

# Подключение к серверу
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

# Прослушивание сервера и отправка никнейма


def receive():
    while True:
        try:
            # Получить сообщение от сервера
            # Если "NICK", отправьте никнейм
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            # Закройте соединение при возникновении ошибки
            print("Произошла ошибка!")
            client.close()
            break


def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('utf-8'))


# Запуск потоков для прослушивания и записи
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
