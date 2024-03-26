import json
import os
import random
import shutil
import sys
import socket
import multiprocessing
import time

#https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
a = 1

level_num = 0
room_name = ""
#level_base = f"./maps/level{level_num}.json"

save_dir = "./saves"

old_room = ""
deathcount = 0

has_displayed = multiprocessing.Condition()

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

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
    def _randomise(self, opt) -> str:
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
        return f"{self._randomise(options)}\n{bcolours.YELLOW}You remain in the same room{bcolours.ENDC}"

    def invalid_move(self) -> str:
        options = [
            "You attempt a move that defies the laws of the game universe. The game, however, insists on following said laws. Nice try!",
            "Your character contemplates a daring manoeuvre, but the game responds with a gentle reminder that such acrobatics are not within the established rules. Better luck next time!",
            "You try to perform a move that would make a gymnast proud, but the game, being a stickler for reality, denies your request. Your character sighs and considers more conventional actions.",
            "The game system rejects your unconventional move with a virtual shake of its head. It seems the rules are more rigid than your character's imagination.",
            "Your character attempts a move straight out of a fantasy novel, only to be met with the cold, hard reality of game mechanics. The system kindly informs you that such actions are beyond its programming. Time for plan B!"
        ]
        return f"{self._randomise(options)}\n{bcolours.BRIGHTRED}Not a valid move{bcolours.ENDC}"

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
        return f"{self._randomise(options)}\nor you made a typo"
    
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
        return f"{self._randomise(options)}\nIt wont move"
    
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
            "Your search proves fruitless; the item is not present."
        ]
        return f"{self._randomise(options)}\nOr, a typo, perhaps you just dont have it in your inventory"

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
        return f"{self._randomise(options)}\nor a simple typo happened"

    def item_interaction_with_object_fail(self,item,obj) -> str:
        options = [
            f"You try to use the {item} on the {obj}, but it doesn't seem to have any effect.",
            f"Your attempt to use the {item} on the {obj} yields no results.",
            f"The {item}'s function doesn't seem compatible with the {obj} you're trying to use it on.",
            f"You attempt to use the {item} on the {obj}, but it's like trying to fit a square peg in a round hole.",
            f"Using the {item} on the {obj} proves unsuccessful; they just don't seem meant to interact.",
            f"The {item}'s purpose doesn't align with the {obj}'s function, resulting in a failed attempt.",
            f"You give it a try, but the {item} and the {obj} don't seem to see eye to eye.",
            f"No matter how you try to use the {item} on the {obj}, it simply doesn't work.",
            f"Your attempt to use the {item} on the {obj} meets with confusion and lack of progress.",
            f"It's clear that the {item} and the {obj} have different agendas; your attempt fails to bridge the gap."
        ]
        return f"{self._randomise(options)}"
    
    def none_of_that_enemy_here(self) -> str:
        options= [
            "Your search yields nothing; the enemy seems elusive.",
            "Despite your efforts, the enemy remains elusive.",
            "No luck - the enemy is nowhere to be found.",
            "Your thorough search turns up empty-handed.",
            "The enemy you seek eludes your searching gaze.",
            "Unfortunately, the enemy is not in this vicinity.",
            "You scour the area but find no trace of the enemy.",
            "The item seems to be playing a game of hide and seek.",
            "Your search proves fruitless; the enemy is not present."
        ]
        return f"{self._randomise(options)}\nor a megre typo happened"
    
    def enemy_miss_dodge(self, enemy:str) ->str:
        options = [
            f"You deftly evade the {enemy}'s attack, sidestepping just in time.",
            f"You dodge the {enemy}'s attack effortlessly, leaving them off-balance.",
            f"The {enemy}'s strike misses.",
            f"You easily evade the {enemy}'s clumsy attack, feeling a rush of satisfaction.",
            f"Your quick reflexes allow you to dodge the {enemy}'s attack with ease.",
            f"You sidestep the {enemy}'s attack."
        ]
        return f"{self._randomise(options)}"
    
    def enemy_miss(self, enemy:str) -> str:
        options = [
            f"The {enemy}'s attack misses its mark, narrowly avoiding you.",
            f"The {enemy}'s strike misses.",
            f"The {enemy} swings, but their attack whiffs harmlessly past you.",
            f"The {enemy}'s swing misses its mark, their frustration evident.",
            f"The {enemy}'s attack falls short, leaving them frustrated."
        ]
        return f"{self._randomise(options)}"

    def generic_enemy_hit(self, enemy:str) -> str:
        """
        when enemy hits player
        """
        options = [
            f"The {enemy}'s attack connects, dealing damage to you.",
            f"You feel the impact as the {enemy}'s strike lands.",
            f"The {enemy}'s attack hits home, causing you pain.",
            f"You take damage as the {enemy}'s attack connects.",
            f"The {enemy}'s blow lands squarely, leaving you reeling.",
            f"You feel the sting of the {enemy}'s successful attack.",
            f"The {enemy}'s strike finds its mark, inflicting harm upon you.",
            f"You grit your teeth as the {enemy}'s attack lands true.",
            f"You suffer the consequences as the {enemy}'s attack connects.",
            f"The {enemy}'s attack hits, causing you to wince in pain."
        ]
        return f"{self._randomise(options)}"
    
    def generic_player_hit(self, enemy:str) -> str:
        """
        when player hits enemy
        """
        options = [
            f"Your attack strikes true, dealing damage to the {enemy}.",
            f"You hit the {enemy}, causing them to stagger from the blow.",
            f"Your strike connects, inflicting damage upon the {enemy}.",
            f"The {enemy} recoils as your attack lands squarely.",
            f"You successfully hit the {enemy}",
            f"The {enemy} takes damage as your attack connects.",
            f"Your strike finds its mark, causing the {enemy} to falter.",
            f"You land a solid hit on the {enemy}, rattling them.",
            f"The {enemy} feels the impact of your successful attack."
        ]
        return f"{self._randomise(options)}"

    def player_miss(self, enemy:str) -> str:
        options = [
            f"Your attack misses, leaving you off-balance.",
            f"You swing wide, narrowly missing the {enemy}.",
            f"The {enemy} evades your attack, leaving you frustrated.",
            f"Your strike falls short, much to your dismay.",
            f"You whiff your attack, cursing your poor aim.",
            f"You swing and miss, feeling a pang of frustration.",
            f"Your attack fails to connect",
            f"Your strike misses its mark, leaving you momentarily exposed."
        ]
        return f"{self._randomise(options)}"

    def player_miss_dodge(self, enemy:str) -> str:
        options = [
            f"The {enemy} sidesteps your blow, avoiding harm.",
            f"The {enemy} deftly dodges your attack, mocking your effort."
        ]
        return f"{self._randomise(options)}"
    
    def player_death(self) -> str:
        options = [
            "You have fallen in battle, your journey ends here.",
            "Your life force fades away as darkness claims you.",
            "Death embraces you, your adventure comes to an end.",
            "Defeat overwhelms you, your story reaches its final chapter.",
            "Your quest ends abruptly as you succumb to fate.",
            "The shadows consume you, your legacy fades into obscurity.",
            "You breathe your last, leaving behind an unfinished tale.",
            "Your journey concludes, lost to the annals of history.",
            "In the end, mortality claims you, your saga ends.",
            "Your valiant effort ends in defeat, your legend fades away."
        ]
        return f"{self._randomise(options)}\n{bcolours.BRIGHTRED}Game over.{bcolours.ENDC}"

    def enemy_death(self, enemy:str) -> str:
        options = [
            f"The {enemy} falls, vanquished by your hand.",
            f"Victory is yours as you defeat the {enemy}.",
            f"Your strike proves fatal, the {enemy} is no more.",
            f"The {enemy} crumbles before your might, defeated.",
            f"You emerge triumphant, the {enemy} lies defeated.",
            f"With a final blow, the {enemy} meets its end.",
            f"The {enemy} meets its demise at your hands.",
            f"Your skill in combat prevails, the {enemy} is slain."
        ]
        return f"{self._randomise(options)}\nDropped items are on the floor"

    def retreat_success(self) -> str:
        options = [
            "You make a hasty retreat, fleeing from combat.",
            "With a quick turn, you escape from the battle.",
            "You beat a hasty retreat, avoiding further confrontation.",
            "Deciding discretion is the better part of valor, you flee from combat.",
            "You flee the battle, seeking safety in retreat.",
            "Recognizing the danger, you hastily withdraw from combat.",
            "You turn tail and run, seeking to avoid further conflict.",
            "Feeling overwhelmed, you choose to flee from the fight.",
            "In the face of danger, you opt for a strategic retreat.",
            "You flee the battlefield, regrouping for another day."
        ]
        return f"{self._randomise(options)}"

    def retreat_fail(self, enemy) -> str:
        options = [
            "Your attempt to flee fails, leaving you trapped in combat."
            f"The {enemy} blocks your escape route, preventing your retreat."
            "You stumble in your attempt to flee, unable to escape combat."
            f"Your retreat is thwarted as the {enemy} closes in on you."
            "Your escape plan falters, leaving you stranded in combat."
            f"The {enemy} intercepts your retreat, blocking your path."
            "You attempt to flee, but fear paralyzes you in place."
            "Your desperate attempt to escape fails, leaving you surrounded."
            "As you turn to flee, you trip and fall, unable to escape combat."
        ]
        return f"{self._randomise(options)}"

def sort_stuff(temp:dict) -> dict:
    """
    bubble sort the dictionaries
    """
    thing = list(temp.items())
    swapped = True
    n = len(thing)
    while swapped and n>=0:
        swapped = False
        for i in range(0,n-1):
            if thing[i][0].split(" ")[0] > thing[i+1][0].split(" ")[0]:
                thing[i], thing[i+1] = thing[i+1], thing[i]
                swapped = True

        n -= 1

    tmp = {}
    for i in range(0,len(thing)):
        tmp[thing[i][0]] = thing[i][1]

    return tmp

def load_stuff(location:str, type) -> dict: #type 0, item, type 1, obj
    """
    Loads the file contents into objects and then an array
    """
    temporary = {}
    try:
        with open(location, "r") as f:
            item_data = json.load(f)
            for i in item_data:
                print(i, item_data[i])
                if type == "obj":
                    temporary[i] = Obj(i, item_data[i])
                elif type == "itm":
                    temporary[i] = Item(i, item_data[i])
                else:
                    temporary[i] = Enemy(i, item_data[i])
    except KeyError as e:
        abort(e, location)
    return sort_stuff(temporary)

class Item:
    """
    an object for an item, and how it performs actions
    """
    def __init__(self, name, itm_obj) -> None:
        self.name = name
        self.type = itm_obj["type"]
        try: self.damage = itm_obj["damage"] # if < 0 it heals, because thats how stuff works
        except: self.damage = [0,0]
        self.description = itm_obj["description"]
        try: self.hit = itm_obj["hit"] # hit bonus
        except: self.hit = 0
        try: self.on_use = itm_obj["on_use"]
        except: self.on_use = None

    def inspect(self) -> str:
        return self.description

class List_of_items:
    """
    contains a list of all items and skills in the game
    """
    def __init__(self) -> None:
        location = "./stuff/items.json"
        self.dict_of_items:Item = load_stuff(location, "itm")
    
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

        try: self.interaction = obj_obj["interaction"]
        except: self.interaction = None

class List_of_objects:
    """
    contains all objects
    """
    def __init__(self) -> None:
        location = "./stuff/objects.json"
        self.dict_of_objects:Obj = load_stuff(location, "obj")
    
    def examine(self, obj) -> (str | bool):
        """
        returns the object if it finds it, otherwise returns false
        """
        print(obj, self.dict_of_objects)
        if obj in self.dict_of_objects:
            return self.dict_of_objects[obj]
        return False

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
        self.health_range = ene_obj["health"]
        self.hit = ene_obj["hit"]
        self.armour = 10 + ene_obj["armour"]
        try: self.atk_pat = ene_obj["attack_pattern"]
        except: self.atk_pat = [self.damage]
        self.atk_chance = ene_obj["attack_chance"]

    def return_health(self) -> int:
        return random.randint(self.health_range[0], self.health_range[1])

class List_of_enemies:
    """
    contains all enemies
    """
    def __init__(self) -> None:
        location = "./stuff/enemies.json"
        self.dict_of_enemies:Enemy = load_stuff(location, "ene")


class Player:
    def __init__(self) -> None:
        self.name = ""
        self.age = 0
        self.health = 10
        self.ac = 10
        self.inventory = [
            [ # items (list of names)
                
            ],
            [ # skills (list of names)
                
            ]
        ]


    def save(self, level:int, room_name:str, deathcount:int) -> None:
        """
        saves the user data to a csv
        
        name,age
        health
        items
        skills
        level,room
        """
        row_one = self.name + "," + str(self.age) +"\n"
        health = str(self.health) +"\n"
        items = ",".join(self.inventory[0]) + "\n"
        skills = ",".join(self.inventory[1]) +"\n"
        map_dat = str(level)+ ","+room_name+","+str(deathcount)

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

    def display_inventory(self, inv_type:str) -> str:
        """
        gets it ready for display
        item = 0
        skill = 1
        """
        def group_items(array) -> list:
            current_pos = 0
            to_return = []
            while True: # loop
                counter = 0
                search = array[current_pos]
                for i in array[current_pos:]:
                    if i == search:
                        counter += 1 # if item = search then add one
                
                current_pos += counter # move our position to end of last search
                to_return.append(f"{str(counter+1 if counter == 0 else counter)}x {search}") #append
                if current_pos >= len(array):# check if at end
                    break
            return to_return
                
        
        def create_list(self:Player, itype:str) -> (list | str):
            to_return = []
            if len(self.inventory[itype]) > 0:
                for i in self.inventory[itype]:
                    if i != "":
                        to_return.append(game_items.dict_of_items[i].name)
            else: to_return == ""
            return to_return

        items = "Your inventory contains:\n"
        skills = "The skills you have are:\n"

        if inv_type != "":
            # check if it is either, otherwise show both
            if inv_type == "item":
                return items+"\n".join(group_items(create_list(self, 0)))
            
            elif inv_type == "skill":
                return skills+ "\n".join(create_list(self, 1))
        else:
            val = items + "\n".join(group_items(create_list(self, 0)))
            val += "\n\n" + skills +"\n".join(create_list(self, 1))
            return val


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
        try: self.dependants = data["dependant"]
        except: self.dependants = None
        try: self.passable = self.properties["passable"]
        except: self.passable = 1
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
        
        self.enemies = []
        print(f"{bcolours.OKGREEN}done{bcolours.ENDC}\n    Loading  Enemies", end=" ")
        try:
            self.enemies = self.properties["enemies"] # list of names
        except:
            self.enemies = []

        self.objects = []
        print(f"{bcolours.OKGREEN}done{bcolours.ENDC}\n    Loading  Objects", end=" ")
        self.objects:list = self.properties["examine"]
        print(f"{bcolours.OKGREEN}done{bcolours.ENDC}\n")
        
        
        
class Level:
    def __init__(self, map, room_name:str="", deathcount:int=0) -> None:
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
        self.deathCount = deathcount


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
                
        if not passable 
            check dependants
            if changes it to 1: success
            else: false

        else: success
                
        """
        success = False
        if move in self._moves:
            move_in = self._moves_dict[move]
            room_to_go = self.current_room.connections[move_in]
            try:

                if self._rooms[room_to_go].passable == 0:
                    if self.check_dependants(room_to_go):
                        try: # getting here means the room isnt passable, so we check if dependants, if there are then check if passable is one of them, then check if it turns it to 1
                            passable = self._rooms[room_to_go].dependants["results"]["passable"]
                            if passable == 1:
                                self.current_room = self._rooms[room_to_go]
                                success = True
                        except:
                            pass
                
                else:
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
                        return check_needs(game_objects.dict_of_objects[i])
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
            return "scouring the room up and down, looking everywhere, you cant find it"



    def place(self, obj, user:Player) -> str:
        """
        place an object from inventory into the world
        """
        try:
            if game_items.dict_of_items[obj].type == "skill":
                return "you cant place a skill down"
        except KeyError: return response_gen.itemnt()

        if obj not in user.inventory[0]:
            return "you dont appear to have that item"

        self.current_room.item_names.append(obj)
        self.data[self.current_room.name]["properties"]["items"] = self.current_room.item_names
        user.inventory[0].remove(obj)
        with open(self._map, "w") as f:
            json.dump(self.data, f, indent=4)
        return "you successfully place down " +obj
    
    def interact(self, item, obj, user:Player) -> str:
        """
        use an item/skill (on an object) and how it affects the world
        """
        try: # validation 
            game_items.dict_of_items[item]
        except KeyError: 
            return response_gen.itemnt()
        
        if game_items.dict_of_items[item].type == "skill":
            if item not in user.inventory[1]:
                return "you dont appear to have that skill"
            # todo: using skills in game
            pass
            
        elif game_items.dict_of_items[item].type == "item":
            if item not in user.inventory[0]:
                return "you dont appear to have that item"
            if obj == "":
                # todo: using items in game
                pass
            else:
                if item in game_objects.dict_of_objects[obj].interaction[0]:
                    self.place(item, user)
                    return game_objects.dict_of_objects[obj].interaction[1]
                else:
                    return response_gen.item_interaction_with_object_fail(item, obj)

    def check_dependants(self, room_name:str) -> bool:
        """
        check dependants and change properties as required
        """
        target = self._rooms[room_name].dependants
        if target is not None:
            if target["item"] in self._rooms[target["room"]].item_names:
                return True
        
        return False

    def get_description(self) -> str:
        """
        Return description
        """
        if self.check_dependants(self.current_room.name):
            description = "\n"+self.current_room.dependants["results"]["description"]
        else:
            description = "\n"+self.current_room.description 

        if len(self.current_room.enemies) > 0:
            description += f"\n{bcolours.BRIGHTRED}Enemies{bcolours.ENDC}" 
            for i in self.current_room.enemies:
                description += f"\n    {i}"
        
        if len(self.current_room.item_names) > 0:
            description += f"\n{bcolours.OKGREEN}Items{bcolours.ENDC}" 
            for i in self.current_room.item_names:
                description += f"\n    {i}"
        
        return description
    



def player_death(level:Level, user:Player) -> tuple[Level, Player]:
    """
    player death
    """
    level.current_room = level._rooms["startingRoom"]
    level.deathCount += 1
    print("deathcount =",level.deathCount)
    match level.deathCount:
        case 1:
            to_display("You died. You find yourself in a familiar place, but you feel weak")
            user.health = 5
            
        case 2:
            to_display("You have again become one with the spirits; You find yourself in a familar place, feeling vastly weakend")
            user.health = 2
        case 3:
            # uh ohh you died too much, game reset
            to_display(response_gen.player_death())
            reset()
    return level, user

def combat(user:Player, level:Level, thing=None) -> tuple[Level, Player]:
    """
    Combat loop and whatnot
    """    
    if thing==None or thing == "":
        return level, user, "You can't attack nothing!"
    
    if thing in game_enemies.dict_of_enemies:
        
        enemy:Enemy = game_enemies.dict_of_enemies[thing]
    else: return level, user, response_gen.none_of_that_enemy_here()

    if thing not in level.current_room.enemies:
        return level, user, response_gen.none_of_that_enemy_here()

    def roll():
        return random.randint(1,20)

    def apply_modifiers(damage:int) -> int:
        if player_defend == True:
            damage = damage * defend_mod
        elif player_dodge == True:
            damage = damage * dodge_mod

        damage = round(damage)
        return damage

    to_display("Exiting will not save combat! (it will save some things like your hp though)")


    combat_is_happening = True
    attack_pattern_position = 0
    tmp = enemy.return_health()
    enemy_data = [
        tmp,              # 0 | max hp
        tmp,              # 1 | hp
        enemy.armour,     # 2 | AC
        enemy.hit,        # 3 | Attack mod
        enemy.atk_pat,    # 4 | attack pattern (damage vals for them)
        enemy.atk_chance, # 5 | chance of attacking
        False,            # 6 | defend
        False,            # 7 | dodge (ac one)
        enemy.name,       # 8 | the enemys name
        enemy.loot        # 9 | list of drops
    ]
    
    enemy_percent_health = int( enemy_data[1]/enemy_data[0] * 100 )
    to_display(f"{user.name}: {user.health} | {enemy_data[8]}: {enemy_percent_health}")

    while combat_is_happening:
        skip = False
        player_dodge = False
        player_defend = False
        # show percentage of player health, and enemy health

        enablePrint()
        vals = input(f"{bcolours.BRIGHTRED}> {bcolours.ENDC}").strip().split(" ")
        blockPrint()
        print(vals)
        u_input = vals.pop(0).lower()
        
        if len(vals) == 1:
            content = vals[0]
        elif len(vals) > 1:
            content = []
            for i in vals:
                content.append(i.lower())
            if u_input != "use":
                content = " ".join(content)
            print(content)
        else: 
            content = ""        

        match u_input:
            case "attack":
                if content == "": # no attack to attack therefore unarmed
                    to_display(f"You dont appear to have an attack! Using unarmed")
                    if roll() >= enemy_data[2] if not enemy_data[7] else enemy_data[2] + dodge_mod:
                        damage = 1
                        enemy_data[1] -= damage
                        to_display(f"you deal {bcolours.OKGREEN}{damage}{bcolours.ENDC} damage")
                    else:
                        to_display(response_gen.player_miss(enemy_data[8]))
                    
                elif content != "":
                    if content in user.inventory[0] or content in user.inventory[1]:
                        data:Item = game_items.dict_of_items[content]

                        if roll() + data.hit >= enemy_data[2] if not enemy_data[7] else enemy_data[2] + dodge_mod:
                            damage = random.randint(data.damage[0], data.damage[1])
                            damage = apply_modifiers(damage)
                            to_display(f"you {'d' if damage >= 0 else 'h'}eal {bcolours.OKGREEN}{damage}{bcolours.ENDC} damage")
                            
                            enemy_data[1] -= damage
                        else: # missing
                            if player_dodge == True:
                                to_display(response_gen.player_miss_dodge(enemy_data[8]))
                            else:
                                if random.randint(0,1):
                                    to_display(response_gen.player_miss(enemy_data[8]))
                                else:
                                    to_display(response_gen.player_miss_dodge(enemy_data[8]))
                            
                    else:
                        to_display(response_gen.cant_find_item())

            case "defend":
                player_defend = True

            case "dodge":
                player_dodge = True
            
            case "use":
                if content in user.inventory[0] or content in user.inventory[1]:
                    data:Item = game_items.dict_of_items[content]
                    
                    damage = random.randint(data.damage[0], data.damage[1])
                    if data.on_use is not None:
                        to_display(data.on_use)
                    to_display(f"you {'d' if damage >= 0 else 'h'}eal {bcolours.OKGREEN}{damage}{bcolours.ENDC} damage")
                    user.health -= damage

                else:
                    to_display(response_gen.cant_find_item())

            case "flee":
                """
                escape combat code
                """
                totalhp = enemy_data[1] + user.health
                player_percent = user.health / totalhp * 100
                if random.randint(1,100) <= player_percent:
                    to_display(response_gen.retreat_success())
                else:
                    to_display(response_gen.retreat_fail(enemy_data[8]))
                break

            case "wait":
                pass
            
            case "help":
                dt = help_combat.split("\n")
                for i in dt:
                    to_display(i)
            case _:
                to_display("Your turn is forfit!")

        if enemy_data[1] > enemy_data[0]: # stop enemy getting higher than max hp
            enemy_data[1] = enemy_data[0]

        enemy_data[6] = False
        enemy_data[7] = False

        if not skip: 
            #enemy move
            attack_check = random.randint(1,100)
            if attack_check <= enemy_data[5]: # check if they attack
                
                atk_roll = roll() + enemy_data[3]
                if atk_roll >= user.ac if player_dodge == False else user.ac + dodge_ac_boost:
                    tmp = enemy_data[4][attack_pattern_position]
                    damage = random.randint(tmp[0], tmp[1])
                    to_display(response_gen.generic_enemy_hit(enemy_data[8]))                

                    damage = apply_modifiers(damage)
                    to_display(f"it deals {bcolours.BRIGHTRED}{damage}{bcolours.ENDC} damage")
                    user.health -= damage # take away damage

                else:
                    if player_dodge == True:
                        to_display(response_gen.enemy_miss_dodge(enemy_data[8]))
                    else:
                        to_display(response_gen.enemy_miss(enemy_data[8]))
                
                attack_pattern_position +=1
                print(attack_pattern_position)
                print(enemy_data)
                if attack_pattern_position >= len(enemy_data[4]):
                    attack_pattern_position = 0
            
            else:   # check if they dodge or defend
                check = random.randint(1,100)
                if check <= enemy_data[5]:
                    enemy_data[6] = True
                else:
                    enemy_data[7] = True
        
        enemy_percent_health = int( enemy_data[1]/enemy_data[0] * 100 )
        to_display(f"{user.name}: {user.health} | {enemy_data[8]}: {enemy_percent_health}%")

        # death

        if user.health <= 0:
            level, user = player_death(level, user)
            break

        if enemy_data[1] <= 0: 
            item_dropped = random.choice(enemy_data[9]) #random item
            user.inventory[0].append(item_dropped) #place item in inv
            print(level.current_room.enemies)
            level.current_room.enemies.remove(enemy_data[8]) #remove enemy from room
            level.place(item_dropped, user)
            print(level.current_room.enemies)
            return level, user, response_gen.enemy_death(enemy_data[8])


    return level, user, ""
                    

       
def to_display(val) -> None:
    """
    parse and send so newlines occur in a space rather than mid word
    """
    enablePrint()
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
    blockPrint()

def abort(e, location) -> None:
    """
    aborts the program
    """
    print(f"{bcolours.BRIGHTRED}Error: {bcolours.ENDC}{e}\nProgram aborting due to error in {bcolours.YELLOW}{location}{bcolours.ENDC} upon loading")
    os._exit(1)

def reset_check() -> None:
    to_display("Are you sure? this process is not reversible [y/N]")
    enablePrint()
    val = input().lower()
    if val == "y":
        val = input("Are you sure you're sure? [y/N]\n").lower()
        if val == "y":
            reset()   

def reset() -> None:
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

def webserver() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #plain = '<!DOCTYPE HTML><html><style>.light-mode {background-color: white;color: black;}.dark-mode{background-color: rgb(41, 41, 41);color: white;}</style><button id="darkMode" onclick="toggle_visuals()">toggle light mode</button><head><script>var element = document.body;function toggle_visuals(){if (element.className == "dark-mode"){element.classList.replace("dark-mode", "light-mode" )} else {element.classList.replace("light-mode", "dark-mode" )}}; </script></head><body class="dark-mode"><p>Text Based Tea Game</p><h1 style="font-family: Courier New, monospace;">%s</h1></body><html>'
        web_start = '<!DOCTYPE HTML><html><style>p{margin:5px 0;}.light-mode {background-color: white;color: black;font-family: sans-serif;}.dark-mode{background-color: rgb(0, 0, 0);color: white;}</style><button id="darkMode" onclick="toggle_visuals()">toggle light mode</button><head><script>var element = document.body;function toggle_visuals(){if (element.className == "dark-mode"){element.classList.replace("dark-mode", "light-mode" )} else {element.classList.replace("light-mode", "dark-mode" )}};function hide_alt_tables(){document.getElementById("enemies").style.display="none";document.getElementById("items").style.display="none";document.getElementById("objects").style.display="none";}function enemy_select(){hide_alt_tables();document.getElementById("enemies").style.display="block";document.getElementById("opt_display").innerHTML="Enemies";};function item_select(){hide_alt_tables();document.getElementById("items").style.display="block";document.getElementById("opt_display").innerHTML="Items";};function object_select(){hide_alt_tables();document.getElementById("objects").style.display="block";document.getElementById("opt_display").innerHTML="Objects";};</script></head><body class="dark-mode" style="font-family:arial"><p>Text Based Tea Game</p><p>playing as '+ user.name+' </p><button id="enemyButton" onclick="enemy_select()">Enemies</button><button id="itemButton" onclick="item_select()">Items</button><button id="objectButton" onclick="object_select()">Objects</button><p id="opt_display">Enemies</p>'
        web_end = '</body></html>'
        
        tmp = game_enemies.dict_of_enemies
        web_start += "<div id='enemies'>"
        for i in tmp:
            web_start += f'<details><summary>{i}</summary><p>{tmp[i].description}</p><p>Drops: {", ".join(tmp[i].loot)}</p><p>Health range: {tmp[i].health_range[0]} to {tmp[i].health_range[1]}</p><p>Attack damage: {tmp[i].damage[0]} to {tmp[i].damage[1]}</p></details>'
        web_start += "</div>"

        tmp = game_items.dict_of_items
        web_start += "<div id='items' style='display:none'>"
        for i in tmp:
            web_start += f'<details><summary>{i}</summary><p>{tmp[i].description}</p><p>Type: {tmp[i].type}{" " if tmp[i].damage == [0,0] else f"</p><p>Hit bonus: {tmp[i].hit}</p><p>Damage range: {tmp[i].damage[0]} to {tmp[i].damage[1]}</p>"}</details>'
        web_start += "</div>"

        tmp = game_objects.dict_of_objects
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
            to_send:str = "HTTP/1.1 200 OK\r\nHost: "+addr[0]+"\r\nContent-Length: "+str(len(data))+"\r\nContent-Type: text/html\r\n\r\n"+data+"\r\n\r\n" 

            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(data)
                conn.sendall(to_send.encode())
                conn.sendall(b"a")

def webserver_caller(has_displayed_var:multiprocessing.Condition) -> None:
    to_display("website at: http://"+HOST+":"+str(PORT))
    with has_displayed_var:
        has_displayed_var.notify_all()
    while True:
        webserver()

"""
blank room object
    "name":{
        "north": "",
        "south":"",
        "east":"",
        "west":""
        "description":"",
        "dependant":{
            "room" : "",
            "item" : "",
            "results":{
                "description" : ""
                "other funny stuff":""
            }
        },
        "properties":{
            "examine":[
                "",
                ""
            ],
            "items" :[
                "",
                ""
            ],
            "enemies":[
                "",
                ""
            ]
        }
    },

    "object":{
        "alias":"string,list,aa",
        "movable":0,
        "interaction":["item", "result"],
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
    "examine",  # examine <object>      | examine an object in the world #object in world can be item in room
    "inspect",  # inspect <i/s>         | inspect an item in inventory
    "combine",  # combine <i/s> <i/s>   | combine items in inventory
    "read",     # read <object>         | read a sign or book or whatever
    "use",      # use <i/s> [object]    | use an item or skill
    "attack",   # attack <enemy>        | Attack an enemy and start combat
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
inventory [i/s]     view inventory
talk <name>         talk with an npc of that name
examine <object>    better look at an object of that name
inspect <i/s>       take a closer look at an item or skill
combine <i/s>       merge two items together
read <object>       read the text on a sign or poster
use <i/s>           use an item/skill
attack <enemy>      initiate combat
help                display this list
exit                save & close

Dying 3 times in a level is permadeath
if you want to restart the game just look in maps_spare/readme.md
"""

combat_commands = [ #i/s = item/skill
    "attack",   # attack [i/s]          | attack the selected enemy with the last used thing, or new one
    "defend",   # defend                | decreases damage input by 50%
    "dodge",    # dodge                 | increase AC, increase damage input by 50%
    "use",      # use <i/s> [object]    | use an item or skill on self
    "flee",     # flee                  | chance to escape combat based on factors
    "wait",     # wait                  | Skip!
    "help"      # help                  | help list
]

help_combat = """
Help menu
i/s means item/skill

attack              Attack the enemy with last used item/skill
defend              reduce damage taken
dodge               less likely to be hit, but increased damage if hit
use i/s             use an item or a skill on self
flee                attempt to escape combat
wait                skip your turn
help                display this list

"""

try:
    with open("./config/config.json", "r") as f:
        data = json.load(f)
    loading_status = data["loading_status"]

    dodge_mod = data["dodge_mod"]
    dodge_ac_boost = data["dodge_ac_boost"]
    defend_mod = data["defend_mod"]

except:
    print("config not found, loading without")
    loading_status = 1 # show debug on start

    # defaults
    dodge_mod = 1.5
    dodge_ac_boost = 5
    defend_mod = 0.5


if not loading_status:
    # Disable print
    def blockPrint():
        sys.stdout = open(os.devnull, 'w')

    # Restore print
    def enablePrint():
        sys.stdout = sys.__stdout__
else:
    def blockPrint():
        pass
    
    def enablePrint():
        pass

del data
blockPrint()

print("Loading responses")
response_gen:Responses = Responses()

user:Player = Player()
print(f"{bcolours.OKGREEN}done{bcolours.ENDC}\nLoading items:")
game_items:List_of_items = List_of_items()
print(f"{bcolours.OKGREEN}done{bcolours.ENDC}\nLoading objects:")
game_objects:List_of_objects = List_of_objects()
print(f"{bcolours.OKGREEN}done{bcolours.ENDC}\nLoading enemies:")
game_enemies:List_of_enemies = List_of_enemies()
print(f"{bcolours.OKGREEN}done{bcolours.ENDC}")

if __name__ == '__main__':
    print(f"loading webpage")
    with has_displayed:
        webserv = multiprocessing.Process(target=webserver_caller, args=(has_displayed,))
        webserv.start()
        has_displayed.wait(timeout=1)

    if first_run:
        enablePrint()
        """
        code that runs once on first run only
        """
        content = """Welcome to the game! 
    if you cant figure out anything try typing help
    keep your eye out for interesting things, and good luck
    if you want to restart the game just look in maps_spare/readme.md
    the help command is useful
    """
        to_display(content)
        enablePrint()
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
                if age < 13 or age > 100:
                    os._exit(1)
            except ValueError:
                print("please use a number")
        user.age = age

        user.save(level_num, "startingRoom", deathcount)
        blockPrint()

    else:
        try:
            level_num, room_name, deathcount = user.load_save()
        except Exception as e:
            abort(e, "./saves/save.csv")



    try:
        print(f"loading level: ./maps/level{level_num}.json")
        level = Level(f"./maps/test.json", room_name, int(deathcount)) #swap /test.json with /level{level_num}.json
        enablePrint()
        while True:
            """
            main loop
            """
            current_room = level.current_room.name
            if current_room != old_room:
                to_display(level.get_description())
                old_room = current_room

            enablePrint()
            vals = input(f"{bcolours.OKCYAN}> {bcolours.ENDC}").strip().split(" ")
            blockPrint()

            u_input = vals.pop(0).lower()
            
            if len(vals) == 1:
                content = vals[0]
            elif len(vals) > 1:
                content = []
                for i in vals:
                    content.append(i.lower())
                if u_input != "use":
                    content = " ".join(content)
                print(content)
            else: 
                content = ""

            if level.current_room.save == 1:
                # if room is a save room
                user.save(level_num, current_room, level.deathCount)
            match u_input:
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
                    to_display(level.get_description())
                case "inventory":
                    val = user.display_inventory(content)
                    to_display(val)
                case "talk":
                    pass # implement with npcs
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
                    # uses the interaction bit of object class, and an item
                    val =level.interact(content[0], content[1], user)
                    to_display(val)
                case "attack":
                    level, user, val = combat(user, level, thing=content)
                    print("deathcount =",level.deathCount)
                    to_display(val)
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
                case "game_reset_sf9riwzceosxepo6":
                    reset_check()
                case _:
                    to_display(response_gen.invalid_move())
                


    except KeyboardInterrupt:
        user.save(level_num, current_room, level.deathCount)
        pass
    finally:
        webserv.kill()
        enablePrint()
        print("bye")