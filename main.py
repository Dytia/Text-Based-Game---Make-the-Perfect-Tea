import time
import os
import json
import random

#https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
a = 1
jsonFileLocation = "./config/positions.json"
jsonFileLocationOptional = "./config/optional.json"

level_num = 0
level_base = f"./maps/level{level_num}.json"

'''
vase = "" | "held" | "correct" (made in china)
'''

class Responses:
    def __init__(self) -> None:
        pass

    def randomise(self, opt) -> str:
        '''
        select random things
        '''
        return random.choice(opt)

    def wall(self) -> str:
        '''
        list of wall responses
        '''
        options = [
            "You bravely face the challenge of walking through a wall, but alas, the wall remains unyielding. Perhaps your character needs to reassess their spatial awareness skills or invest in a better map.",
            "As you take another step forward, you suddenly find your progress halted by an unyielding force. It appears you've encountered the elusive Wall of Immobile Stubbornness. you character contemplates the mysteries of architecture.",
            "You confidently march forward, ready to face whatever challenges lie ahead. Little did you expect that the most formidable adversary on this quest would be a seemingly innocent wall. Your character contemplates the strategic advantages of not walking into solid objects.",
            "You decide to test the structural integrity of the space around you and, to your dismay, discover that walls are, indeed, quite good at being walls. Your character reassesses their approach to environmental navigation and considers the benefits of looking before leaping.",
            "In a surprising turn of events, your character attempts a daring feat: walking through a wall. Unfortunately, the laws of physics and common sense prevail, and your character finds themselves nose-to-wall. Ouch. Perhaps a more traditional path is in order.",
            "In a moment of sheer optimism, your character decides to embrace the wall, figuratively speaking. Unfortunately, the wall remains unresponsive to your character's attempts at friendship. Your character, undeterred, wonders if there's a door or an open path around this seemingly insurmountable obstacle.",
            "You walk face-first into a wall. Ouch. Lesson learned: Walls are solid.",
            "Forward march! Except, wait, that's a wall. Your character's face meets reality.",
            "Unexpected plot twist: Your character discovers walls are still impassable.",
            "You attempt to phase through the wall, RPG-style. Turns out, this isn't a superhero game.",
            "Reality check: Your character finds that walls are surprisingly good at their job."
        ]
        return f"{self.randomise(options)}\n{bcolors.YELLOW}You remain in the same room{bcolors.ENDC}"

    def invalid_move(self) -> str:
        options = [
            "You attempt a move that defies the laws of the game universe. The game, however, insists on following said laws. Nice try!",
            "Your character contemplates a daring maneuver, but the game responds with a gentle reminder that such acrobatics are not within the established rules. Better luck next time!",
            "You try to perform a move that would make a gymnast proud, but the game, being a stickler for reality, denies your request. Your character sighs and considers more conventional actions.",
            "The game system rejects your unconventional move with a virtual shake of its head. It seems the rules are more rigid than your character's imagination.",
            "Your character attempts a move straight out of a fantasy novel, only to be met with the cold, hard reality of game mechanics. The system kindly informs you that such actions are beyond its programming. Time for plan B!"
        ]
        return f"{self.randomise(options)}\n{bcolors.BRIGHTRED}Not a valid move{bcolors.ENDC}"


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



class Room:
    """
    a room file, stores the data for what happens in a room
    """
    def __init__(self) -> None:
        self.explored = False
        self._values = [
            "north",
            "south",
            "west",
            "east"
        ]

    def set_room_data(self, name, data) -> bool:
        """
        connections = north, south, west, east
        """
        self.connections = []
        self.name = name
        for i in range(0,4):
            try:
                self.connections.append(data[self._values[i]])
            except:
                self.connections.append("")
        


class Level:
    def __init__(self, map) -> None:
        '''
        1: location of map file
        startingRoom will always be the first room
        '''
        self._map = map

        self._commands = [
            "move",
            "take",
            "look",
            "inventory",
            "talk",
            "examine",
            "inspect",
            "combine",
            "read",
            "use",
            "wait",
            "help"
        ]

        self._moves = [
            "n", "s", "w", "e", "north", "south", "west", "east"
        ]
        self._moves_dict = {
            "n" : 0,
            "s" : 1,
            "w" : 2,
            "e" : 3,
            "north" :0,
            "south" :1,
            "west"  :2,
            "east"  :3
        }
        self._values = [
            "north",
            "south",
            "west",
            "east",
            "properties",
            "data"
            ]
        
        self._create_rooms()
        self.current_room:Room = self._rooms[0]
        self.responses = Responses()


    def _create_rooms(self) -> None:
        '''
        creates a list of rooms stored to _rooms
        '''
        self._rooms = []
        self.data = self.read_json()
        for i in self.data:
            temp = Room()
            temp.set_room_data(i, self.data[i])
            self._rooms.append(temp)
        

    def read_json(self):
        '''
        Reads the config file and returns all the data in it
        '''
        with open(self._map, "r") as f:
            data = json.load(f)
        return data
    

    def move_room(self, move) -> bool:
        """
        checks if its a valid room and moves to that room

        """
        success = False
        if move in self._moves:
            move_in = self._moves_dict[move]
            room_to_go = self.current_room.connections[move_in]
            for i in self._rooms:
                
                if i.name == room_to_go:
                    self.current_room = i
                    success = True
            if success:
                return True
            else:
                return self.responses.wall()
        else:
            return self.responses.invalid_move()




class old_Level:
    # impassable = no value
    '''
    "sample room":{
        "north": "room1",
        "west":"room2",
        "description":"you enter the dark room",
        "properties":"item",
        "data":"you see",
    }

    blank template:
    "":{
        "north":"",
        "south":"",
        "west":"",
        "east":"",
        "description":"",
        "properties":{},
        "data":{}
    },    
    '''
    def __init__(self, map):
        '''
        1: location of config file
        2: what level this object is focused on
        '''
        self._map = map
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
        with open(self._map, "r") as f:
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


# temp func

def room_show():
    directions = ["north", "east", "south", "west"]
    for i in directions:
        print(i + ": " + f"{bcolors.YELLOW}" + room_values[i] + f"{bcolors.ENDC}")




room = Room()

with open("./maps/level0.json", "r") as f:
    b = json.loads(f.read())
    for i in b:
        #print(i,end=" ")
        #print(b[i])
        room.set_room_data(i, b[i])

a = Level("./maps/level0.json")

z = "{'aaa'}"
print(f"{z}")

#while True:
print(a.current_room.name)
b = input()
c = a.move_room(b)
if c == True:
    print(a.current_room.name)
else:
    print(c)
print("\n")

try:
    print(level_base.encode())
    level = Level(level_base)
    while True:
        """
        main loop
        """

except KeyboardInterrupt:
    pass
finally:
    print("bye")

try:
    print("Hello, welcome to the game. Press Enter key to continue")
    input()
    a = old_Level(jsonFileLocation, "Start")
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

        try: 
            item = room_values["data"]["item"]
            if item != "": print("item: " + item)
        except:
            print("",end="")

        try:
            secretItem = room_values["data"]["secretItem"]
            if secretItem != "": print(f"{bcolors.MAGENTA}" + secretItem +f"{bcolors.ENDC}")
        except: 
            print("",end="")

        room_show()
        #print(room_values)
        print("current room: " + f"{bcolors.OKGREEN}"+room+f"{bcolors.ENDC}")
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
            print("you moved to: "+ f"{bcolors.OKGREEN}"+room+f"{bcolors.ENDC}")

        elif checkedPlayerInput == 2:
            room = room
            print(f"{bcolors.BRIGHTRED}"+" you walk into wall" + f"{bcolors.ENDC}")

except KeyboardInterrupt:
    pass
finally:
    print("bye") 

#input()