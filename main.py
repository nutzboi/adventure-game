import time
import random

player_name = "player"

stat = {
    "inventory_stick": 0,
    "inventory_empty": 1,
    "monster_alive": 1,
    "monster_beaten": 0,
    "candy_eaten": 0,
    "candy_cave": 1 
}

situation = ""
score = 0

situations = {
    '''
    This dictionary contains the possible situations the player may face.
    Each situation is a dictionary that contains the number of cases,
    the functions to be executed in the situation, the description of
    the situation, the prompt, and the resulting situation of each choice.
    '''
    "initial":
    {
        "cases": 1,
        "func": [""],
        "desc": [["You're lost in the mountains.",
                  "In front of you are two caves.",
                  "There seems to be a fire lit inside the left cave.",
                  "The right cave is so dark you can't see anything.",
                  "Which cave will you enter?"]],
        "prompt": [["Left Cave.", "Left Cave." "Right Cave.", "Right Cave."]],
        "results": [["cave1", "cave1_walk" "cave2", "cave2_empty"]],
        "availability": [["monster_alive", "monster_beaten",
                          "cave_stick","inventory_stick"]]
    },
    "cave1":
    {
        "cases": 1,
        "func": [""],
        "desc": [["You step inside the cave.",
                  "You hear distant footsteps from inside. What to do?"]],
        "prompt": [["Shout \"Hello\".", "Continue Walking.", "Go back."]],
        "results": [["cave1_hello", "cave1_walk", "initial"]],
        "availability": [["", "", ""]]
    },
    "cave2":
    {
        "cases": 1,
        "func": [""],
        "desc": [["You step inside the cave. You're scared.",
                  "You step on an object. What to do?"]],
        "prompt": [["Pick it up.", "Continue walking.",
                    "Continue walking.", "Go back."]],
        "results": [["cave2_obj", "cave2_walk",
                     "cave2_walk_empty", "initial"]],
        "availability": [["", "candy_cave",
                          "candy_eaten", ""]]
    },
    "cave2_empty":
    {
        "cases": 1,
        "func": [""],
        "desc": [["You're inside the cave.",
                  "It's dark. What to do?"]],
        "prompt": [["Continue walking.", "Continue walking.", "Go back."]],
        "results": [["cave2_walk", "cave2_walk_empty", "initial"]],
        "availability": [["candy_cave", "candy_eaten", ""]]
    },
    "cave2_obj":
    {
        "cases": 1,
        "func": ["pickup_stick","score+1"],
        "desc": [["You now have a stick.",
                  "Fantastick! (+1 point ^ω^)"]],
        "prompt": [["Continue."]],
        "results": [["cave2_empty"]],
        "availability": [[""]]
    },
    "cave2_walk":
    {
        "cases": 1,
        "func": ["score+1", "pickup_candy"],
        "desc": [["You walk further inside the cave.",
                  "You find some candy to take with you.",
                  "Nice. (+1 point ^ω^)"]],
        "prompt": [["Continue."]],
        "results": [["cave2_empty"]],
        "availability": [[""]]
    },
    "cave2_walk_empty":
    {
        "cases": 1,
        "func": ["score+1"],
        "desc": [["You walk further inside the cave.",
                  "There's nothing here."]],
        "prompt": [["Go back.","Go back."]],
        "results": [["cave2","cave2_empty"]],
        "availability": [["inventory_empty","inventory_stick"]]
    },
    "cave1_hello":
    {
        "cases": 2,
        "func": [""],
        "desc": [["The footsteps get louder. ",
                  "You see a monster running towards you.",
                  "What to do?."],
                 ["Your voice echoes through the cave. ",
                 "The footsteps become quieter.",
                  "What to do?."]],
        "prompt": [["Run.", "Fight it with your fist.",
                    "Beat it with your stick."],
                    ["Continue walking inside.", "Go back."]],
        "results": [["escape_monster", "fight_monster", "beat_monster"],
                    ["cave1_inside", "initial"]],
        "availability": [["", "", "inventory_stick"], ["", ""]]
    },
    "cave1_walk":
    {
        "cases": 1,
        "func": ["show_score"],
        "desc": [["You walk deep inside the left cave.", "You find a map.",
                  "Now you can find your way home!", "Yᴏᴜ Wɪɴ."]],
        "prompt": [["Main menu."]],
        "results": [["menu"]],
        "availability": [[""]]
    },
    "escape_monster":
    {
        "cases": 1,
        "func": [""],
        "desc": [["You are now outside.",
                 "The monster is still after you. What to do?"]],
        "prompt": [["Go into the other cave.",
                   "Fight it with your fist.",
                   "Beat it with your stick.", "Give up."]],
        "results": [["escape_cave2", "fight_monster",
                     "beat_monster", "give_up"]],
        "availability": [["", "", "inventory_stick", ""]]
    },
    "fight_monster":
    {
        "cases": 1,
        "func": ["score-1"],
        "desc": [["You try to fight the monster with your fist.",
        "It's too strong for you.","You are hurt (-1 point T_T)."]],
        "prompt": [["Beat it with your stick.","Give up."]],
        "results": [["beat_monster","give_up"]],
        "availability": [["inventory_stick",""]]
    },
    "beat_monster":
    {
        "cases": 1,
        "func": ["score+1"],
        "desc": [["You beat the monster with your stick.",
        "It falls to the ground.","(+2 points ^ω^)"]],
        "prompt": [["Continue."]],
        "results": [["relax"]],
        "availability": [[""]]
    },
    "escape_cave2":
    {
        "cases": 2,
        "func": [],
        "desc": [["Dead End. The monster eats you.", "Gᴀᴍᴇ Oᴠᴇʀ."],
                 ["The monster loses its sight of you.",
                  "It wanders into the forest.",
                  "You escaped the monster. (+1 points ^ω^)"]],
        "prompt": [["Main menu."], ["Continue."]],
        "results": [["menu"],["relax"]],
        "availability": [[""],[""]]
    },
    "relax":
    {
        "cases": 1,
        "func": ["score+1"],
        "desc": [["You sit outside for a while to take your breath.",
                 "You're proud of yourself and ready to get up agian.",]],
        "prompt": [["Continue."]],
        "results": [["initial"]],
        "availability": [[""]]
    },
    "give_up":
    {
        "cases": 1,
        "func": ["show_score"],
        "desc": [["You are hopeless.", "You let the monster eat you.",
                   "Gᴀᴍᴇ Oᴠᴇʀ."]],
        "prompt": [["Main menu."]],
        "results": ["menu"],
        "availability": [""]
    }
}


def print_pause(s, t=1):
    '''
    Function to print a string "s" and wait for "t" seconds
    '''
    print(s)
    time.sleep(t)


def prompt(options,available):
    '''
    Input function to keep prompting users with prompts "options"
    until a valid option number is chosen.
    '''
    option_numbers = []
    last_number = 1
    for i in available:
        if(stat[i]):
            option_numbers.append(last_number)
            last_number+=1
        else:
            option_numbers.append(-1)
    while True:
        for i in range(len(options)):
            if i == -1:
                continue
            print("("+str(option_numbers[i])+") "+options[i])
        choice = input("Input choice number: ")
        if choice < last_number:
            return option_numbers.index(choice)
        else:
            print("Please choose a valid option")


def init():
    '''
    Game Initialization
    '''
    global player_name
    print_pause("Welcome to the game.", 3)
    player_name = str(input("Please enter your name: "))

def func(f):
    '''
    Execute functions demanded by the game situation. 
    '''
    for s in f:
        if(s == "show_score"):
            print("Your score is: " + str(score) + "points.")
        if(s == "pickup_stick"):
            stat["inventory_empty"] = 0
            stat["inventory_stick"] = 1
        if(s == "pickup_candy"):
            stat["candy_eaten"] = 1
            stat["candy_cave"] = 0
        if(s[:5] == "score"):
            if(s[5] == "+"):
                score+=int(s[6:])
            else:
                score-=int(s[6:])
    
def gameplay():
    '''
    Process Gameplay.
    '''
    situation = "initial"
    while situation != "menu":
        func(situations[situation]["func"])
        situation_case = random.randrange(0,situations["situation"]["cases"])
        for i in situations[situation]["desc"][situation_case]:
            print_pause(i,1 if len(i) < 35 else 2)
        choice = prompt(situations[situation]["prompt"][situation_case],
                        situations[situation]["availability"][situation_case])
        situation = situations["situation"]["results"][choice]


def menu():
    '''
    Menu Screen
    '''
    global player_name
    print_pause("Hi, " + player_name +
                "! Please choose one of the options below"+
                " by typing its number:")
    menu_choice = int(prompt("1. Start New Game\n2. Exit", ["1", "2"]))
    if menu_choice == 1:
        print_pause("Starting game...", 3)
        gameplay()
        return
    elif menu_choice == 2:
        quit()


if player_name == "player":
    init()
while(True):
    menu()
