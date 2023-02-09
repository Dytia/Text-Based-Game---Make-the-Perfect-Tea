import time
import os
import json

#https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
a = 1
jsonFileLocation = "./config/positions.json"
jsonFileLocationOptional = "./config/optional.json"

'''
vase = "" | "held" | "correct" (made in china)
'''


class Player:
    def __init__(self, jsonFileLocationOptional):
        self._baseHealth = 100
        self._jsonLocation = jsonFileLocationOptional
        self._options = [
            "inspect",
            "pick up",
            "put down"
        ]
    
    def check_valid_option(self, user_option):
        for i in self._options:
            if i == user_option:
                return True


class bcolors:
    MAGENTA = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    BRIGHTRED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Level:
    # impassable = no value
    '''
    "sample room":{
        "north": "room1",
        "south":"",
        "west":"room2",
        "east":"",
        "properties":"item",
        "data":"you see",
    }

    blank template:
    "":{
        "north": "",
        "south":"",
        "west":"",
        "east":"",
        "properties":{},
        "data":{}
    },    
    '''
    def __init__(self, jsonLocation, level):
        '''
        1: location of config file
        2: what level this object is focused on
        '''
        self._levelChoice = level
        self._jsonLocation = jsonLocation
        self._values = [
            "north",
            "south",
            "west",
            "east",
            "properties",
            "data"
            ]

    def read_json(self):
        '''
        Reads the config file and returns all the data in it
        '''
        with open(self._jsonLocation, "r") as f:
            data = json.load(f)
            #print(data["Start"])
            #data["Start"] for starting area
        return data

    def write_json(self, data):
        '''
        using the data got from the read_json() function,
        it will save any data changed

        Do NOT change:
        "north"
        "south"
        "west"
        "east"
        "properties"
        '''
        with open(self._jsonLocation, "w") as f:
            json.dump(data, f, indent=2)
        return 1

    def get_room_values(self, room):
        '''
        Gets the values of the selected room
        e.g. north, south, west, etc
        '''
        data = self.read_json()
        data_value = data[self._levelChoice][room]
        return data_value

    def check_valid_move(self, room, choice):
        '''
        using the room name and the move, 
        this validates if the move command is valid, if it isnt it
        returns 0

        room = "startingRoom"
        choice = "north"
        if it is a valid choice and valid move it returns 1
        if there is a wall, it returns 2
        '''
        for i in self._values:
            if choice == str(i):
                success = True
                break
            else: success = False

        if success:
            data = self.get_room_values(room)
            if data[choice] == "": return 2 # 2 means wall
            else: return 1                  # 1 means valid
        else:     return 0                  # 0 means not even a move
            


def user_input(situation):
    '''
    A module to print the current situation,
    and then to return the user input

    Automatically adds a newline and converts it to string
    '''
    usrInp = input(str(situation) + "\n")
    return usrInp

print("Hello, welcome to the game. Press Enter key to continue")
input()
a = Level(jsonFileLocation, "Start")
data = a.read_json()
d = a.get_room_values("startingRoom")
print(d)
b = input()
c = a.check_valid_move("startingRoom",b)
if c == 1: print("moved to: ", d[b] )
if c == 2: print("you walk into a wall, it hurts a little")
#if b == "di":
tmp = data["Start"]["vase"]
print(tmp["north"], tmp["south"])
#print(data["Start"]["startingRoom"])
#os.system("CLS")
print("a")
room = "startingRoom"

playerData = Player(jsonFileLocationOptional)

while True:
    room_values = a.get_room_values(room)

    item = room_values["data"]["item"]
    if item != "":
        print("item: " + item)

    secretItem = room_values["data"]["secretItem"]
    if secretItem != "": print(f"{bcolors.MAGENTA}" + secretItem +f"{bcolors.ENDC}")
    print(room_values)
    print(room)
    playerInput = input("make move: ")
    print("")
    if playerInput == "exit":
        break
    
    checkedPlayerInput = a.check_valid_move(room, playerInput)
    #if checkedPlayerInput == 0:
    #    if playerData.check_valid_option(playerInput):
    #        if room_values["data"]["item"] != "" and playerInput != "put down":
                
                

    if checkedPlayerInput==1:
        room = room_values[playerInput]
        print("you moved to: ", room)

    elif checkedPlayerInput == 2:
        room = room
        print("wall")

        

#input()