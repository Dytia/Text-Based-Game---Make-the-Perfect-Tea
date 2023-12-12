import time
import os
import json
import random

#https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
a = 1

level_num = 0
room_name = ""
#level_base = f"./maps/level{level_num}.json"

save_dir = "./saves"

old_room = ""

if os.path.isfile("./saves/save.csv"):
    first_run = False #save to variable for later use
else: 
    first_run = True


class Responses:
    """
    Due to lacking imagination, i used ai to help create more, good, responses to a situation
    This class, the strings are the only thing made with help of AI
    """
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

    def examine(self) -> str:
        """
        list of examine fails
        """
        options = [
            "Upon closer inspection, the object appears to be rather mundane. It doesn't reveal any hidden details or surprises.",
            "You give the object a thorough look, but it seems to be exactly what it appears to be, no secrets or surprises.",
            "Your attempt to examine the object results in a straightforward observation. It is exactly as it seems, with no hidden complexities.",
            "No surprises here; the object is precisely what you thought it would be. A simple, unremarkable item.",
            "A closer look at the object reveals its simplicity. There's nothing remarkable or unusual about it."
        ]
        return f"{self.randomise(options)}\n or you made a typo"


class Player:
    def __init__(self) -> None:
        self.name = ""
        self.age = 0
        self.gender = ""
        self.inventory = [
            [ # items (list of names)
                "1", "2", "3"
            ],
            [ # skills (list of names)
                "fafsfd", "adasf", "sfdf"
            ]
        ]

    def save(self, level:int, room_name:str) -> None:
        """
        saves the user data to a csv
        
        name,age,gender
        items
        skills
        level,room
        """
        row_one = self.name + "," + str(self.age) + "," + self.gender +"\n"
        items = ",".join(self.inventory[0]) + "\n"
        skills = ",".join(self.inventory[1]) +"\n"
        map_dat = str(level)+ ","+room_name

        content = row_one + items + skills + map_dat

        with open("./saves/save.csv", "w") as f:
            f.write(content)

    def load_save(self) -> None:
        """
        reads the user data from a csv,
    
        """
        stuff = []
        with open("./saves/save.csv", "r") as f:
            data = f.read()
            split_data = data.split("\n")

            for i in split_data:
                stuff.append(i.split(","))
            
            self.name = stuff[0][0]
            self.age = stuff[0][1]
            self.gender = stuff[0][2]

            self.inventory[0] = stuff[1]
            self.inventory[1] = stuff[2]

            return stuff[3]


    def sort_inventory(self) -> None:
        """
        sorts the players inventory alphabetically
        bubble sort
        """
        for inv in self.inventory:
            n = len(inv) +1
            swapped = True
            while swapped and n>=0:
                swapped = False
                for i in range(0,n-2):
                    if inv[i].lower() > inv[i+1].lower():
                        tmp = inv[i]
                        inv[i] = inv[i+1]
                        inv[i+1] = tmp
                        swapped = True

                n -= 1

    def use_thing(self) -> None:
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
        self.properties = data["properties"]
        self.item_names = data["item_names"]
        for i in range(0,4):
            try:
                self.connections.append(data[self._values[i]])
            except:
                self.connections.append("")
        try:
            self.save = data["properties"]["save"]
        except:
            self.save = 0


class Level:
    def __init__(self, map, room_name:str="") -> None:
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
        
        self._create_rooms()
        if room_name == "":
            self.current_room:Room = self._rooms[0]
        else:
            for i in range(0, len(self._rooms)):
                if self._rooms[i].name == room_name:
                    self.current_room:Room = self._rooms[i]
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
        

    def read_json(self) -> dict:
        '''
        Reads the config file and returns all the data in it
        '''
        with open(self._map, "r") as f:
            data = json.load(f)
        return data
    

    def move_room(self, move) -> (bool | str):
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

    def examine(self, obj) -> (bool | str):
        """
        runs the examine thing and checks if its even an object in the room
        """
        examine = self.current_room.properties["examine"]
        if obj in examine:
            return examine[obj]
        else: 
            return response_gen.examine()



def to_display(val) -> None:
    """
    parse and send so newlines occur in a space rather than mid word
    """
    size = os.get_terminal_size().columns
    last_space = 0
    vals = val.split("\n")
    for val in vals:
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


"""
blank room object
    "name":{
        "north": "",
        "south":"",
        "east":"",
        "west":""
        "description":"",
        "properties":{
            "examine":{
                "":"",
                "":""
            }
        },
        "item_names" :[
        
        ],
        "data":{
            "look":""
        }
    },
"""

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
    "help",     # help                  | display commands
    "drink",    # drink <tea>           | drink tea, or if coffee specified, quit without saving
    "exit"      # exit                  | saves & quits the game
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
help                display this list
exit                save & close
"""
response_gen = Responses()

user = Player()

if first_run:
    """
    code that runs once on first run only
    """
    content = """Welcome to the game! 
if you cant figure out anything try typing help
keep your eye out for interesting things, and good luck
if you want to restart just change the name of saves.json to something else
"""
    to_display(content)
    fail = True
    print("Character creation")
    # get character name
    while fail:
        name = input(f"{bcolors.OKGREEN}name{bcolors.ENDC}? ")
        for i in name:
            if ord(i) in range(65, 123) and not ord(i) in range(91,97):
                fail = False
            else:
                fail = True
        if fail: print("please only use letters")
    user.name = name
    
    # get character age
    fail = True
    while fail:
        try:
            age = int(input(f"{bcolors.OKGREEN}age{bcolors.ENDC}? "))
            fail = False
            if age < 16 or age > 100:
                os._exit(1)
        except ValueError:
            print("please use a number")
    user.age = age

    # get character gender (uses three options for overall vs precise)
    gender = input(f"(for best experience use female, male or non-binary)\n{bcolors.OKGREEN}gender{bcolors.ENDC}? ")
    user.gender = gender

    user.save(level_num, "startingRoom")

else:
    level_num, room_name =  user.load_save()


try:
    print(f"./maps/level{level_num}.json".encode())
    level = Level(f"./maps/level{level_num}.json", room_name)
    while True:
        """
        main loop
        """
        current_room = level.current_room.name
        if current_room != old_room:
            to_display(level.current_room.description)
            old_room = current_room
        u_input = input(f"{bcolors.OKCYAN}> {bcolors.ENDC}").split(" ")
        try:
            content = u_input[1].lower()
        except IndexError:
            content = ""

        if level.current_room.save == 1:
            user.save(level_num, current_room)
        
        match u_input[0]:
            case "move":
                val = level.move_room(content)
                if val != True:
                    to_display(val)
            case "take":
                pass
            case "look":
                to_display(level.current_room.description)
            case "inventory":
                pass
            case "talk":
                pass
            case "examine":
                val = level.examine(content)
                to_display(val)
            case "inspect":
                pass
            case "combine":
                pass
            case "read":
                pass
            case "use":
                pass
            case "help":
                dt = help_data.split("\n")
                for i in dt:
                    to_display(i)
            case "drink":
                if content == "tea":
                    to_display() # tea response
                elif content == "coffee":
                    try: os.remove("./saves/save.csv")
                    except: pass
                    finally: os._exit(1)
            case "exit":
                raise KeyboardInterrupt
            case _:
                to_display(response_gen.invalid_move())



except KeyboardInterrupt:
    user.save(level_num, current_room)
    pass
finally:
    print("bye")