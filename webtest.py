import os
import asyncio
import multiprocessing
import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

current_room = "startingRoom"
table_array = [["objects", ["bed", "desk"]], ["items", ["notebook", "stick"]]]

#from doctype to table


def webserver(counter) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #plain = '<!DOCTYPE HTML><html><style>.light-mode {background-color: white;color: black;}.dark-mode{background-color: rgb(41, 41, 41);color: white;}</style><button id="darkMode" onclick="toggle_visuals()">toggle light mode</button><head><script>var element = document.body;function toggle_visuals(){if (element.className == "dark-mode"){element.classList.replace("dark-mode", "light-mode" )} else {element.classList.replace("light-mode", "dark-mode" )}}; </script></head><body class="dark-mode"><p>Text Based Tea Game</p><h1 style="font-family: Courier New, monospace;">%s</h1></body><html>'
        web_start = '<!DOCTYPE HTML><html><style>.light-mode {background-color: white;color: black;}.dark-mode{background-color: rgb(41, 41, 41);color: white;}td {padding: 5px;}.light-mode table, .light-mode tr {border-bottom: 1px solid black;border-collapse: collapse;}.dark-mode table, .dark-mode tr {border-bottom: 1px solid white;border-collapse: collapse;}.dark-mode #head {padding: 5px;text-align: left;border-right: 1px solid white;border-bottom: 1px solid white;border-collapse: collapse;}.light-mode #head {padding: 5px;text-align: left;border-right: 1px solid black;border-bottom: 1px solid black;border-collapse: collapse;}</style><button id="darkMode" onclick="toggle_visuals()">toggle light mode</button><head><script>var element = document.body;function toggle_visuals(){if (element.className == "dark-mode"){element.classList.replace("dark-mode", "light-mode" )} else {element.classList.replace("light-mode", "dark-mode" )}};     </script></head><body class="dark-mode" style="font-family:arial"><p>Text Based Tea Game</p><h1 style="font-family: Courier New, monospace;">Hello!, '+str(g_counter)+'</h1><table>'

        web_end = '</table></body></html>'
        for i in table_array:
            web_start = web_start + '<tr>'
            for j in i:
                if len(j[0]) > 1:
                    for k in j:
                        web_start = web_start + '<td>' + k + '</td>'
                else:
                    web_start = web_start + '<td id="head">' + j + '</td>'
            web_start = web_start + '</tr>'

        data = web_start + web_end

        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            #data = plain%counter
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

def a():
    print("http://"+HOST+":"+str(PORT))
    for i in range(0,10):
        webserver(i)

g_counter = 0
if __name__ == '__main__':
    val = multiprocessing.Process(target=a)
    val.start()

    for i in range(0,1000000):
        g_counter = i