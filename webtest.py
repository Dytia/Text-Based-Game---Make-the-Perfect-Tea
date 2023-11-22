import os
import asyncio
import multiprocessing
import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


def webserver(counter) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        plain = '<!DOCTYPE HTML><html><body><h1 style="font-family: Courier New, monospace;">%s</h1></body><html>'

        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            data = plain%counter
            counter = counter +1
            to_send:str = "HTTP/1.1 200 OK\r\nHost: "+addr[0]+"\r\nContent-Length: "+str(len(data))+"\r\nContent-Type: text/html\r\n\r\n"+data+"\r\n\r\n" 

            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(data)
                conn.sendall(to_send.encode())
                conn.sendall(b"a")

for i in range(0,10):
    webserver(i)