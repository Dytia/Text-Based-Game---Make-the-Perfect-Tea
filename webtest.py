import os
import asyncio
import multiprocessing
import socket
import json
import time

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

current_room = "startingRoom"
table_array = [["objects", ["bed", "desk"]], ["items", ["notebook", "stick"]]]

#from doctype to table

def load_stuff(location:str, type) -> dict: #type 0, item, type 1, obj
    temporary = {}
    try:
        with open(location, "r") as f:
            item_data = json.load(f)
            for i in item_data:
                print(item_data[i])
                if type == "obj":
                    temporary[i] = Obj(i, item_data[i])
                elif type == "itm":
                    temporary[i] = Item(i, item_data[i])
                else:
                    temporary[i] = Enemy(i, item_data[i])
    except KeyError as e:
        print(e, location)
    return temporary

class Item:
    """
    an object for an item, and how it performs actions
    """
    def __init__(self, name, itm_obj) -> None:
        self.name = name
        self.type = itm_obj["type"]
        try: self.damage = itm_obj["damage"] # if < 0 it heals, because thats how stuff works
        except: self.damage = 0
        self.description = itm_obj["description"]
    
    def inspect(self) -> str:
        return self.description

class List_of_items:
    """
    contains a list of all items and skills in the game
    """
    def __init__(self) -> None:
        location = "./stuff/items.json"
        self.dict_of_items:Item = load_stuff(location, "itm")
    

class Obj:
    """
    how objects perform actions
    """
    def __init__(self, name, obj_obj) -> None:
        self.name = name
        self.movable = obj_obj["movable"]
        self.description = obj_obj["description"]
        try:
            self.needs = obj_obj["needs"]
            self.alt_desc = obj_obj["alt_desc"]
        except:
            self.needs = None
            self.alt_desc = None

        try: self.alias = obj_obj["alias"]
        except: self.alias = None

        try: self.interaction = obj_obj["interaction"]
        except: self.interaction = None


class List_of_objects:
    """
    contains all objects
    """
    def __init__(self) -> None:
        location = "./stuff/objects.json"
        self.dict_of_objects:Obj = load_stuff(location, "obj")
    

class Enemy:
    """
    an object for an Enemy, and how it performs actions
    """
    def __init__(self, name, ene_obj) -> None:
        self.name = name
        self.loot = ene_obj["loot"]
        try: self.damage = ene_obj["damage"] # if < 0 it heals, because thats how stuff works
        except: self.damage = 0
        self.description = ene_obj["description"]
        self.health = ene_obj["health"]

class List_of_enemies:
    """
    contains all enemies
    """
    def __init__(self) -> None:
        location = "./stuff/enemies.json"
        self.dict_of_enemies:Enemy = load_stuff(location, "ene")

list_of_enemies = List_of_enemies()
list_of_items   = List_of_items()
list_of_objects = List_of_objects()

class player:
    def __init__(self) -> None:
        self.name = "ada"

user = player()

print(os.environ.get('USERNAME'))
def webserver(counter) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #plain = '<!DOCTYPE HTML><html><style>.light-mode {background-color: white;color: black;}.dark-mode{background-color: rgb(41, 41, 41);color: white;}</style><button id="darkMode" onclick="toggle_visuals()">toggle light mode</button><head><script>var element = document.body;function toggle_visuals(){if (element.className == "dark-mode"){element.classList.replace("dark-mode", "light-mode" )} else {element.classList.replace("light-mode", "dark-mode" )}}; </script></head><body class="dark-mode"><p>Text Based Tea Game</p><h1 style="font-family: Courier New, monospace;">%s</h1></body><html>'
        web_start = '<!DOCTYPE HTML><html><style>p{margin:5px 0;}.light-mode {background-color: white;color: black;font-family: sans-serif;}.dark-mode{background-color: rgb(0, 0, 0);color: white;}</style><button id="darkMode" onclick="toggle_visuals()">toggle light mode</button><head><script>var element = document.body;function toggle_visuals(){if (element.className == "dark-mode"){element.classList.replace("dark-mode", "light-mode" )} else {element.classList.replace("light-mode", "dark-mode" )}};function hide_alt_tables(){document.getElementById("enemies").style.display="none";document.getElementById("items").style.display="none";document.getElementById("objects").style.display="none";}function enemy_select(){hide_alt_tables();document.getElementById("enemies").style.display="block";document.getElementById("opt_display").innerHTML="Enemies";};function item_select(){hide_alt_tables();document.getElementById("items").style.display="block";document.getElementById("opt_display").innerHTML="Items";};function object_select(){hide_alt_tables();document.getElementById("objects").style.display="block";document.getElementById("opt_display").innerHTML="Objects";};</script></head><body class="dark-mode" style="font-family:arial"><p>Text Based Tea Game</p><p>Hello '+os.environ.get('USERNAME') + ' </p><p>playing as '+ user.name+' </p><button id="enemyButton" onclick="enemy_select()">Enemies</button><button id="itemButton" onclick="item_select()">Items</button><button id="objectButton" onclick="object_select()">Objects</button><p id="opt_display">Enemies</p>'
        web_end = '</body></html>'
        
        tmp = list_of_enemies.dict_of_enemies
        web_start += "<div id='enemies'>"
        for i in tmp:
            web_start += f'<details><summary>{i}</summary><p>{tmp[i].description}</p><p>Drops: {", ".join(tmp[i].loot)}</p><p>Health range: {tmp[i].health[0]} to {tmp[i].health[1]}</p><p>Attack damage: {tmp[i].damage[0]} to {tmp[i].damage[1]}</p></details>'
        web_start += "</div>"

        tmp = list_of_items.dict_of_items
        web_start += "<div id='items' style='display:none'>"
        for i in tmp:
            web_start += f'<details><summary>{i}</summary><p>{tmp[i].description}</p><p>Type: {tmp[i].type}</p>{"" if tmp[i].damage == 0 else f"<p>Damage: {tmp[i].damage}</p>"}</details>'
        web_start += "</div>"

        tmp = list_of_objects.dict_of_objects
        web_start += "<div id='objects' style='display:none'>"
        for i in tmp:
            web_start += f'<details><summary>{i}</summary><p>{tmp[i].description}</p></details>'
        web_start += "</div>"
        
        web_start += web_end

        data = web_start


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
    try:
        val = multiprocessing.Process(target=a)
        val.start()

        for i in range(0,1000000):
            g_counter = i
            #print(i)
            time.sleep(0.5)
    except:
        val.kill()