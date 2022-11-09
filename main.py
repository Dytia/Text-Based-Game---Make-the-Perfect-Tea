import time
import os
import json


a = 1
jsonFileLocation = "./config/positions.json"

class Level:
    # impassable = no value
    '''
    "sample room":{
        "up": "room1",
        "down":"",
        "left":"room2",
        "right":"",
        "properties":"item",
        "data":"you see",
    }

    blank template:
    "":{
        "up": "",
        "down":"",
        "left":"",
        "right":"",
        "properties":"",
        "data":""
    },    
    '''
    def __init__(self, jsonLocation):
        self._jsonLocation = jsonLocation

    def read_json(self):
        with open(self._jsonLocation, "r") as f:
            data = json.load(f)
            print(data["Start"])
            #data["Start"] for starting area
        return data

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
a = Level(jsonFileLocation)
data = a.read_json()
print(data["Start"]["startingRoom"])
#os.system("CLS")
print("a")

input()