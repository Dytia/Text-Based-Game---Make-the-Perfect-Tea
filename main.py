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

save_dir = "./saves"

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
    def __init__(self) -> None:
        self.inventory = [
            [ # items

            ],
            [ # skills

            ]
        ]

    def load_player(self) -> None:
        pass


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
        self.description = data["description"]
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



def to_display(val):
    """
    parse and send so newlines occur in a space rather than mid word
    """
    size = os.get_terminal_size().columns
    last_space = 0
    if len(val) > size:
        while True:
            p = True
            for i in range(0,len(val)):
                if i > size:
                    print(val[:last_space])
                    p = False
                    break
                if val[i] == " ":
                    last_space = i
            if p:
                print(val)
                break
            val = val[last_space+1:]
    else:
        print(val)



commands = [    #item/skill = i/s
    "move",     # move <direction>      | move north, south, east or west
    "take",     # take <item>           | take an item or thing
    "look",     # look                  | look around an area
    "inventory",# inventory [type]      | show items & skills (inventory items would only show items)
    "talk",     # talk <name>           | talk to an npc 
    "examine",  # examine <name>        | examine an object in the world
    "inspect",  # inspect <i/s>         | inspect an item in inventory
    "combine",  # combine <i/s> <i/s>   | combine items in inventory
    "read",     # read <object>         | read a sign or book or whatever
    "use",      # use <i/s>             | use an item or skill
    "wait",     # wait <h> <m>          | wait x amount of time
    "help",     # help                  | display commands
    "drink"     # drink <tea>           | drink tea, or if coffee specified, quit without saving
]
help_data = """
Help menu
i/s means item/skill

move <direction>    move north, south, east or west
take <item>         take an item from the world
look                look around
inventory [type]    view inventory, and optionally specify type (ie skills or items)
talk <name>         talk with an npc of that name
examine <name>      better look at an object of that name
inspect <i/s>       take a closer look at an item or skill
combine <i/s>       merge two items together
read <object>       read the text on a sign or poster
use <i/s>           use an item/skill
wait <h> [m]        pass the time
help                display this list
"""
response_gen = Responses()



try:
    print(level_base.encode())
    level = Level(level_base)
    while True:
        """
        main loop
        """
        to_display(level.current_room.description)
        u_input = input().split(" ")
        content = u_input[1].lower()
        match u_input[0]:
            case "move":
                pass
            case "take":
                pass
            case "look":
                pass
            case "inventory":
                pass
            case "talk":
                pass
            case "examine":
                pass
            case "inspect":
                pass
            case "combine":
                pass
            case "read":
                pass
            case "use":
                pass
            case "wait":
                pass
            case "help":
                dt = help_data.split("\n")
                for i in dt:
                    to_display(i)
            case "drink":
                if content == "tea":
                    to_display() # tea response
                elif content == "coffee":
                    os._exit(1)
            case _:
                to_display(response_gen.invalid_move())



except KeyboardInterrupt:
    pass
finally:
    print("bye")