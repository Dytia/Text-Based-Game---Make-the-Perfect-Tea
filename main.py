import json
import os
import random
import shutil
import sys
import time

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


class bcolours:
    """
    contains colours for text
    usage f"{bcolours.OKBLUE}word{bcolours.ENDC}"
    """
    MAGENTA = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    BRIGHTRED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Responses:
    """
    Due to lacking creative writing ability, i used ai to help create more, good, responses to a situation
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
        return f"{self.randomise(options)}\n{bcolours.YELLOW}You remain in the same room{bcolours.ENDC}"

    def invalid_move(self) -> str:
        options = [
            "You attempt a move that defies the laws of the game universe. The game, however, insists on following said laws. Nice try!",
            "Your character contemplates a daring manoeuvre, but the game responds with a gentle reminder that such acrobatics are not within the established rules. Better luck next time!",
            "You try to perform a move that would make a gymnast proud, but the game, being a stickler for reality, denies your request. Your character sighs and considers more conventional actions.",
            "The game system rejects your unconventional move with a virtual shake of its head. It seems the rules are more rigid than your character's imagination.",
            "Your character attempts a move straight out of a fantasy novel, only to be met with the cold, hard reality of game mechanics. The system kindly informs you that such actions are beyond its programming. Time for plan B!"
        ]
        return f"{self.randomise(options)}\n{bcolours.BRIGHTRED}Not a valid move{bcolours.ENDC}"

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
        return f"{self.randomise(options)}\nor you made a typo"
    
    def too_heavy(self, thing) -> str:
        """
        if the thing is tooo heavy to move (aka no moving it.)
        """
        options = [
            f"The {thing} is too heavy to budge.",
            f"Attempting to move the {thing} proves futile; it's too massive."
            f"You strain against the {thing}, but it remains immovable"
            f"No matter the effort, the {thing} stands resolutely in place."
            f"As you attempt to shift the {thing}, its sheer weight proves insurmountable. The solid bulk resists your efforts, reminding you that some things in this world are meant to stay put. Perhaps there's another way to navigate around or interact with it.",
            f"Undeterred by the challenge, you exert considerable force in an attempt to move the {thing}. However, the immensity of the {thing} becomes apparent as it refuses to yield to your efforts. It stands stoically, a testament to the limitations of your physical strength.",
            f"Efforts to shift the {thing} are met with resistance as its formidable size and weight prove beyond your current capabilities. The {thing} seems almost rooted to the ground, offering a silent challenge to find another approach or seek assistance to overcome this obstacle."
        ]
        return f"{self.randomise(options)}\nIt wont move"
    
    def cant_find_item(self) -> str:
        options = [
            "Your search yields nothing; the item seems elusive.",
            "Despite your efforts, the item remains elusive.",
            "No luck - the item is nowhere to be found.",
            "Your thorough search turns up empty-handed.",
            "The item you seek eludes your searching gaze.",
            "Unfortunately, the item is not in this vicinity.",
            "You scour the area but find no trace of the item.",
            "The item seems to be playing a game of hide and seek.",
            "Despite your best efforts, the item stays hidden.",
            "Your search proves fruitless; the item is not present.",
        ]
        return f"{self.randomise(options)}\nOr, a typo"

    def itemnt(self) -> str:
        options = [
            "Your search for the item yields no results; it appears not to exist in this realm.",
            "After a thorough investigation, it becomes clear that the item simply doesn't exist here.",
            "Despite your efforts, it seems the item you're looking for is a figment of imagination in this world.",
            "You conclude that the item is nowhere to be found - it might not even exist in this reality.",
            "It dawns on you that the item you seek may be a product of rumor or misconception; it's not present.",
            "The more you search, the more apparent it becomes that the item is not part of this game's universe.",
            "There's a growing realization that the item might be a mythical concept - it's absent in your current surroundings.",
            "Your quest for the item proves futile; it appears it was never part of this game's design.",
            "The absence of any clues or traces strongly suggests that the item is not programmed into this game.",
            "It seems the item you were hoping to find is beyond the boundaries of this virtual world; it simply doesn't exist here."
        ]
        return f"{self.randomise(options)}\nor a simple typo happened"


def load_stuff(location:str, type:int) -> dict: #type 0, item, type 1, obj
    temporary = {}
    try:
        with open(location, "r") as f:
            item_data = json.load(f)
            for i in item_data:
                print(item_data[i])
                if type:
                    temporary[i] = Obj(i, item_data[i])
                else:
                    temporary[i] = Item(i, item_data[i])
    except KeyError as e:
        abort(e, location)
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
        self.dict_of_items:Item = load_stuff(location, 0)
    
    def inspect(self, name) -> (str):
        """
        inspecting the item gives its description if certain conditions are met
        """
        if (name in user.inventory[0] 
            or name in user.inventory[1]
            or name in level.current_room.item_names
            ):
            try:
                val = self.dict_of_items[name].description
            except KeyError:
                return response_gen.itemnt()
            return val
        else:
            return response_gen.examine()

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


class List_of_objects:
    """
    contains all objects
    """
    def __init__(self) -> None:
        location = "./stuff/objects.json"
        self.dict_of_objects:Obj = load_stuff(location, 1)
    
    def examine(self, obj) -> (str | bool):
        """
        returns the object if it finds it, otherwise returns false
        """
        print(obj, self.dict_of_objects)
        if obj in self.dict_of_objects:
            return self.dict_of_objects[obj]
        return False

class Player:
    def __init__(self) -> None:
        self.name = ""
        self.age = 0
        self.gender = ""
        self.health = 10
        self.inventory = [
            [ # items (list of names)
                
            ],
            [ # skills (list of names)
                
            ]
        ]


    def save(self, level:int, room_name:str) -> None:
        """
        saves the user data to a csv
        
        name,age,gender
        health
        items
        skills
        level,room
        """
        row_one = self.name + "," + str(self.age) + "," + self.gender +"\n"
        health = str(self.health) +"\n"
        items = ",".join(self.inventory[0]) + "\n"
        skills = ",".join(self.inventory[1]) +"\n"
        map_dat = str(level)+ ","+room_name

        content = row_one + health +items + skills + map_dat

        with open("./saves/save.csv", "w") as f:
            f.write(content)


    def load_save(self) -> list:
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

        self.health = int(stuff[1][0])

        self.inventory[0] = stuff[2]
        self.inventory[1] = stuff[3]

        return stuff[4]


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

    def take(self, obj) -> None:
        """
        stores in inventory
        """
        if game_items.dict_of_items[obj].type == "item":
            self.inventory[0].append(obj)
        else:
            self.inventory[1].append(obj)

        self.sort_inventory()

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

    def set_room_data(self, name, data, objects) -> bool:
        """
        connections = north, south, west, east
        """
        self.connections = []
        self.name = name
        print(f"    Loading Room: {self.name}\n    Loading  Data",end=" ")
        self.description = data["description"]
        self.properties = data["properties"]
        print(f"{bcolours.OKGREEN}done{bcolours.ENDC}\n    Loading  Items",end=" ")
        self.item_names:list = self.properties["items"]
        print(f"{bcolours.OKGREEN}done{bcolours.ENDC}\n    Creating connections",end=" ")
        for i in range(0,4):
            try:
                self.connections.append(data[self._values[i]])
            except:
                self.connections.append("")
        try:
            self.save = data["properties"]["save"]
        except:
            self.save = 0
        
        self.objects = {}
        print(f"{bcolours.OKGREEN}done{bcolours.ENDC}\n    Loading  Objects", end=" ")
        self.objects:list = self.properties["examine"]
        print(f"{bcolours.OKGREEN}done{bcolours.ENDC}\n")
        
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
        print("Creating rooms")
        self._create_rooms()
        print(f"Creating Rooms {bcolours.OKGREEN}done{bcolours.ENDC}\nSetting starting room")
        if room_name == "":
            self.current_room:Room = self._rooms["startingRoom"]
        else:
            self.current_room:Room = self._rooms[room_name]
        self.responses = Responses()


    def _create_rooms(self) -> None:
        '''
        creates a list of rooms stored to _rooms
        '''
        self._rooms = {}
        print("  Parsing file", end=" ")
        self.data = self.read_json()
        print(f"{bcolours.OKGREEN}done{bcolours.ENDC}\n  Loading objects",end=" ")
        self.objects = self.read_object_json()
        print(f"{bcolours.OKGREEN}done{bcolours.ENDC}\n  Setting room data")
        for i in self.data:
            temp = Room()
            temp.set_room_data(i, self.data[i], self.objects)
            self._rooms[i] = temp

    def read_json(self) -> dict:
        '''
        Reads the level file and returns all the data in it
        '''
        with open(self._map, "r") as f:
            data = json.load(f)
        return data
    
    def read_object_json(self) -> dict:
        '''
        Reads the object file and returns all the data in it
        '''
        with open("./stuff/objects.json", "r") as f:
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
            try:
                self.current_room = self._rooms[room_to_go]
                success = True
            except KeyError:
                success = False
            if success:
                return True
            else:
                return self.responses.wall()
        else:
            return self.responses.invalid_move()

    def examine(self, obj) -> (bool | str):
        """
        runs the examine thing and checks if its even an object in the room
        or if it is an item in the room
        """
        def check_needs(obj:Obj):
            if obj.needs is not None and obj.needs in self.current_room.item_names:
                # check if needs exist, and if they are available
                return obj.description
            
            elif obj.needs is not None:
                # if needs exist but not there
                return obj.alt_desc
            
            else:
                # default
                return obj.description 
                 
        # create list of object names in room (already done per room)
        # check if on list (if obj in list_obj)
        # check if its an item
        try:
            if obj in self.current_room.objects:
                return check_needs(game_objects.dict_of_objects[obj])

            elif self.current_room.item_names == obj:
                    return game_items[obj].description
            else:
                for i in self.current_room.objects:
                    #check through all objects in room for an alias
                    if obj in game_objects.dict_of_objects[i].alias:
                        return check_needs(game_objects.dict_of_objects[obj])
                raise Exception
            
        except:
            return response_gen.examine()


    
    def take(self, obj, user:Player) -> str:
        """
        take an object from the world, store in the player, and change the map file
        """
        try:
            game_items.dict_of_items[obj]
        except KeyError:
            return response_gen.itemnt()
        if obj in self.current_room.item_names:
            self.current_room.item_names.remove(obj)

            self.data[self.current_room.name]["properties"]["items"] = self.current_room.item_names
            with open(self._map, "w") as f:
                json.dump(self.data, f, indent=4)
            
            user.take(obj)
            return "you successfully take the " + obj
        else:
            # it doesnt exist in this room
            return "scouring the room up and down, looking everywhere, you cant "



    def place(self, obj, user:Player) -> str:
        """
        place an object from inventory into the world
        """
        try:
            game_items.dict_of_items[obj]
        except KeyError:
            return response_gen.itemnt()
        
        if game_items.dict_of_items[obj].type == "skill":
            return "you cant place a skill down"

        self.current_room.item_names.append(obj)
        self.data[self.current_room.name]["properties"]["items"] = self.current_room.item_names
        user.inventory[0].remove(obj)
        with open(self._map, "w") as f:
            json.dump(self.data, f, indent=4)
        return "you successfully place down " +obj

       
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

def abort(e, location) -> None:
    """
    aborts the program
    """
    print(f"{bcolours.BRIGHTRED}Error: {bcolours.ENDC}{e}\nProgram aborting due to error in {bcolours.YELLOW}{location}{bcolours.ENDC} upon loading")
    os._exit(1)

def reset() -> None:
    to_display("Are you sure? this process is not reversible [y/N]")
    val = input().lower()
    if val == "y":
        val = input("Are you sure you're sure? [y/N]\n").lower()
        if val == "y":
            try:
                print("removing save", end=" ")
                try:os.remove("./saves/save.csv")
                except:pass
                print(f"{bcolours.OKGREEN}done{bcolours.ENDC}\nDeleting level files", end=" ")
                shutil.rmtree("./maps/")
                print(f"{bcolours.OKGREEN}done{bcolours.ENDC}\nCopying files", end= " ")
                shutil.copytree("./maps_spare/", "./maps/")
                print(f"{bcolours.OKGREEN}done{bcolours.ENDC}\nCleaning up", end=" ")
                os.remove("./maps/readme.md")
                print(f"{bcolours.OKGREEN}done{bcolours.ENDC}\nexiting game")
                os._exit(1)
            except:
                print("An error occured, exiting game probably best to redownload")
                os._exit(1)


# Disable print
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore print
def enablePrint():
    sys.stdout = sys.__stdout__


"""
blank room object
    "name":{
        "north": "",
        "south":"",
        "east":"",
        "west":""
        "description":"",
        "properties":{
            "examine":[
                "",
                ""
            ],
            "items" :[
                "",
                ""
            ],
        },

        "data":{

        }
    },

    "object":{
        "movable":0,
        "description":"if the needs term is unmet this is shown",
        "needs":"option category",
        "alt_desc":"this is default if needs exists",
    }
"""

commands = [    #item/skill = i/s
    "move",     # move <direction>      | move north, south, east or west
    "take",     # take <item>           | take an item or thing
    "place",    # place <item>          | place an item or thing
    "look",     # look                  | look around an area
    "inventory",# inventory [type]      | show items & skills (inventory items would only show items)
    "talk",     # talk <name>           | talk to an npc 
    "examine",  # examine <name>        | examine an object in the world #object in world can be item in room
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
place <item>        place an item to the world
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

try:
    with open("./config/config.json", "r") as f:
        data = json.load(f)
    loading_status = data["loading_status"]
except:
    print("config not found, loading without")
    loading_status = 1 # show debug on start

del data

if not loading_status:
    blockPrint()

print("Loading responses")
response_gen:Responses = Responses()

user:Player = Player()
print(f"{bcolours.OKGREEN}done{bcolours.ENDC}\nLoading items:")
game_items:List_of_items = List_of_items()
print(f"{bcolours.OKGREEN}done{bcolours.ENDC}\nLoading objects:")
game_objects:List_of_objects = List_of_objects()
print(f"{bcolours.OKGREEN}done{bcolours.ENDC}")

if first_run:
    enablePrint()
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
        name = input(f"{bcolours.OKGREEN}name{bcolours.ENDC}? ")
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
            age = int(input(f"{bcolours.OKGREEN}age{bcolours.ENDC}? "))
            fail = False
            if age < 16 or age > 100:
                os._exit(1)
        except ValueError:
            print("please use a number")
    user.age = age

    # get character gender (uses three options for overall vs precise)
    gender = input(f"(for best experience use female, male or non-binary)\n{bcolours.OKGREEN}gender{bcolours.ENDC}? ")
    user.gender = gender

    user.save(level_num, "startingRoom")
    blockPrint()

else:
    try:
        level_num, room_name = user.load_save()
    except Exception as e:
        abort(e, "./saves/save.csv")


try:
    print(f"loading level: ./maps/level{level_num}.json")
    level = Level(f"./maps/level{level_num}.json", room_name)
    enablePrint()
    while True:
        """
        main loop
        """
        current_room = level.current_room.name
        if current_room != old_room:
            to_display(level.current_room.description)
            old_room = current_room
        u_input = input(f"{bcolours.OKCYAN}> {bcolours.ENDC}").split(" ")
        try:
            content = u_input[1].lower()
        except IndexError:
            content = ""

        if level.current_room.save == 1:
            # if room is a save room
            user.save(level_num, current_room)
        
        match u_input[0]:
            case "move":
                val = level.move_room(content)
                if val != True:
                    to_display(val)
            case "take":
                # if object moveable = 0, use the too_heavy(<objname>) function
                val = level.take(content, user)
                to_display(val)
            case "place":
                val = level.place(content, user)
                to_display(val)
            case "look":
                to_display(level.current_room.description)
            case "inventory":
                if content == "items":
                    to_display("Your inventory contains:\n"+"\n".join(user.inventory[0]))
                elif content == "skills":
                    to_display("The skills you have are:\n"+ "\n".join(user.inventory[1]))
                else:
                    to_display("Did you mean items or skills?")
            case "talk":
                pass # implement with npc
            case "examine":
                #print(level.current_room.objects)
                val = level.examine(content)
                to_display(val)
            case "inspect":
                val = game_items.inspect(content)
                to_display(val)
            case "combine":
                pass # implement when more items
            case "read":
                pass # when sign
            case "use":
                pass # soon
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
            case "":
                continue
            case "Game_Reset_sf9RIWzCEoSxepo6":
                reset()
            case _:
                to_display(response_gen.invalid_move())
            



except KeyboardInterrupt:
    user.save(level_num, current_room)
    pass
finally:
    print("bye")