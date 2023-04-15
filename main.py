import time

player_name = "player"

def print_pause(s,t = 1):
    '''
    Function to print a string "s" and wait for "t" seconds
    '''
    print(s)
    time.sleep(t)

def prompt(s,options):
    '''
    Input function to keep prompting users with prompt "s"
    until a valid input (among the "options") is received
    '''
    while True:
        ret = input(s+"\n")
        if ret in options:
            return ret
        else:
            print("Please choose a valid option")

def Init():
    '''
    Initialization
    '''
    global player_name
    print_pause("Welcome to the game.", 3)
    player_name = str(input("Please enter your name: "))
def Menu():
    '''
    Menu Screen
    '''
    global player_name
    print_pause("Hi, " + player_name + "! Please choose one of the options below by typing its number:")
    menu_choice = int(prompt("1. Start New Game\n2. Exit", ["1","2"]))
    if menu_choice == 1:
        print_pause("Starting game...", 3)
        return
    elif menu_choice == 2:
        quit()


Init()
Menu()