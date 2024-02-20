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
            "Your search proves fruitless; the item is not present."
        ]
        return f"{self.randomise(options)}\nOr, a typo, perhaps you just dont have it in your inventory"

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
        return f"{self.randomise(options)}"
    
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
        return f"{self.randomise(options)}\nor a megre typo happened"
    
    def enemy_miss_dodge(self, enemy:str) ->str:
        options = [
            f"You deftly evade the {enemy}'s attack, sidestepping just in time.",
            f"You dodge the {enemy}'s attack effortlessly, leaving them off-balance.",
            f"The {enemy}'s strike misses.",
            f"You easily evade the {enemy}'s clumsy attack, feeling a rush of satisfaction.",
            f"Your quick reflexes allow you to dodge the {enemy}'s attack with ease.",
            f"You sidestep the {enemy}'s attack."
        ]
        return f"{self.randomise(options)}"
    
    def enemy_miss(self, enemy:str) -> str:
        options = [
            f"The {enemy}'s attack misses its mark, narrowly avoiding you.",
            f"The {enemy}'s strike misses.",
            f"The {enemy} swings, but their attack whiffs harmlessly past you.",
            f"The {enemy}'s swing misses its mark, their frustration evident.",
            f"The {enemy}'s attack falls short, leaving them frustrated."
        ]
        return f"{self.randomise(options)}"

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
        return f"{self.randomise(options)}"
    
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
        return f"{self.randomise(options)}"

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
        return f"{self.randomise(options)}"

    def player_miss_dodge(self, enemy:str) -> str:
        options = [
            f"The {enemy} sidesteps your blow, avoiding harm.",
            f"The {enemy} deftly dodges your attack, mocking your effort."
        ]
        return f"{self.randomise(options)}"

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
        except: self.damage = [0,0]
        self.description = itm_obj["description"]
        try: self.hit = itm_obj["hit"] # hit bonus
        except: self.hit = 0
    
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


    def save(self, level:int, room_name:str) -> None:
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
        def create_list(self:Player, itype:str) -> str:
            to_return = []
            if len(self.inventory[itype]) >0:
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
                return items+"\n".join(create_list(self, 0))
            
            elif inv_type == "skill":
                return skills+ "\n".join(create_list(self, 1))
        else:
            val = items + "\n".join(create_list(self, 0))
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
            return "scouring the room up and down, looking everywhere, you cant "



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


def combat(user:Player, room:Room, thing=None) -> str:
    """
    Combat loop and whatnot
    """    
    if thing==None or thing == "":
        return "You can't attack nothing!"
    
    if thing in game_enemies.dict_of_enemies:
        
        enemy:Enemy = game_enemies.dict_of_enemies[thing]
    else: return response_gen.none_of_that_enemy_here()


    def roll():
        return random.randint(1,20)
    
    def set_player_attack_data(player:list, hit:int, damage_range:list) -> list:
        player[0] = hit
        player[1] = damage_range
        player[3] = 1
        return player

    def apply_modifiers(damage:int) -> int:
        if player_defend == True:
            damage = damage * defend_mod
        elif player_dodge == True:
            damage = damage * dodge_mod

        damage = round(damage)
        return damage

    to_display("Exiting will not save combat!")


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
        enemy.name        # 9 | the enemys name
    ]

    player_last_attack = [
        0, # atk mod
        [0,0], # damage range
        0, # if somethins is here
        1  # free uses left
    ]

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
        else: 
            content = ""        

        
        match u_input:
            case "attack":
                if content == "" and player_last_attack[2] == 0: # no attack to attack
                    to_display(f"You dont appear to have an attack! {'skipping round 0/1 free skips left' if player_last_attack[3] ==1 else '' }")
                    if player_last_attack[3]:
                        player_last_attack[3] = 0
                        skip = True
                    
                elif content != "" or player_last_attack[2] == 1:
                    if content in user.inventory[0] or content in user.inventory[1]:
                        data:Item = game_items.dict_of_items[content]
                        player_last_attack = set_player_attack_data(player_last_attack, data.hit, data.damage)

                        if roll() + player_last_attack[0] >= enemy_data[2] if not enemy_data[7] else enemy_data[2] + dodge_mod:
                            damage = random.randint(player_last_attack[1][0], player_last_attack[1][1])
                            damage = apply_modifiers(damage)
                            to_display(f"you deal {bcolours.OKGREEN}{damage}{bcolours.ENDC} damage")
                            
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
                pass

            case "flee":
                pass

            case "wait":
                pass
            
            case "help":
                dt = help_combat.split("\n")
                for i in dt:
                    to_display(i)
            case _:
                pass


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
                
                print("b",attack_pattern_position)
                attack_pattern_position +=1
                print("a",attack_pattern_position)
                print(enemy_data)
                if attack_pattern_position >= len(enemy_data[4]):
                    attack_pattern_position = 0
        

            
            else:   # check if they dodge or defend
                check = random.randint(1,100)
                if check <= enemy_data[5]:
                    enemy_data[6] = True
                else:
                    enemy_data[7] = True
        
        enemy_percent_health = enemy_data[1]/enemy_data[0] * 100
        print(f"{user.name}: {user.health} | {enemy_data[8]}: {enemy_percent_health}")
            
                    


       
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

def reset() -> None:
    to_display("Are you sure? this process is not reversible [y/N]")
    enablePrint()
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
"""

combat_commands = [ #i/s = item/skill
    "attack",   # attack [i/s]          | attack the selected enemy with the last used thing, or new one
    "defend",   # defend                | decreases damage input by 50%
    "dodge",    # dodge                 | increase AC, increase damage input by 50%
    "use",      # use <i/s>             | use an item or skill
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
use i/s             use an item or a skill
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

    user.save(level_num, "startingRoom")
    blockPrint()

else:
    try:
        level_num, room_name = user.load_save()
    except Exception as e:
        abort(e, "./saves/save.csv")

#call website

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
            to_display("\n"+level.current_room.description)
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
                content = content[0]
        else: 
            content = ""

        if level.current_room.save == 1:
            # if room is a save room
            user.save(level_num, current_room)
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
                to_display(level.current_room.description)
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
                val = combat(user, level.current_room, thing=content)
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
                reset()
            case _:
                to_display(response_gen.invalid_move())
            


except KeyboardInterrupt:
    user.save(level_num, current_room)
    pass
finally:
    enablePrint()
    print("bye")