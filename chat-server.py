import socket
import threading

HOST = '0.0.0.0'
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.bind((HOST, PORT))
    sock.listen(1)
except:
    print("Error binding to port")
    exit(1)

conn1, addr1 = sock.accept()
print("First conn received", addr1)

conn2, addr2 = sock.accept()
print("Second conn received", addr2)


def handle_client1_data():
    while True:
        data = conn1.recv(1024)
        if not data:
            break
        message = data.decode()
        print(f"Client 1 sent {message}")
        conn2.send(data)


def handle_client2_data():
    while True:
        data = conn2.recv(1024)
        if not data:
            break
        message = data.decode()
        print(f"Client 2 sent {message}")
        conn1.send(data)


th1 = threading.Thread(target=handle_client1_data)
th1.start()

th2 = threading.Thread(target=handle_client2_data)
th2.start()

th1.join()
th2.join()

conn1.close()
conn2.close()