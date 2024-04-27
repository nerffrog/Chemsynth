import random
import tkinter as GUI
from time import sleep
from threading import Thread
import os
def tank_generator():
    global points
    points = 100
    global tanks
    tanks = [0,0,0,0,0,0,0,0,0,0] #felt easier than an empty list
    global tanks_required
    tanks_required = [0,0,0,0,0,0,0,0,0,0] #same here - placeholder for the goal
    global colors
    colors = ["red", "yellow", "green", "blue", "pink"] #used in random assignment and comparison
    global colors_iterated
    colors_iterated = ["red", "yellow", "green", "blue", "pink", "red"] #specifically here for catalyst
    for i in range(0,10):
        tanks[i] = colors[random.randint(0,4)]
        tanks_required[i] = colors[random.randint(0,4)]
    start_button.destroy()
    global game_running
    game_running = True
    Rainbow_Thread = Thread(target = rainbow_movement, args = (2,), daemon = True, name = "Rainbow Movement")
    Rainbow_Thread.start()
    tank_screen() #puts the tanks on the screen

def select_tool(current = None):
    global current_tool
    current_tool = current #gets current tool depending on last tool button pressed
    return current_tool #returning probably isn't necessary

def use_tool(pos):
    global rainbow1_pos, rainbow2_pos
    if pos == rainbow1_pos or pos == rainbow2_pos:
        try:
            if current_tool == "stirrer":
                stirrer(pos)
            elif current_tool == "centrifuge":
                centrifuge(pos)
            elif current_tool == "replicator":
                replicator(pos)
            elif current_tool == "solvent":
                solvent(pos)
            elif current_tool == "catalyst":
                catalyst(pos)
        except NameError: #in case no tool has been selected yet
            return
        
def rainbow_movement(interval_seconds):
    global rainbow1_pos, rainbow2_pos
    n = 0
    possible_position = [1, 2, 3, 4, 5]
    rainbow1_pos = possible_position[n]
    rainbow2_pos = rainbow1_pos + 5
    rainbow1 = GUI.Label(root, image = rainbow_image, background = "purple")
    rainbow1.place(x = n * 80, y = 180, width = 80, height = 20)
    rainbow2 = GUI.Label(root, image = rainbow_image, background = "purple")
    rainbow2.place(x = n * 80 + 400, y = 180, width = 80, height = 20)

    while game_running == True:
        sleep(interval_seconds)
        if game_running == True:
            n =  n + 1
            if n == 5:
                n = 0
            rainbow1_pos = possible_position[n]
            rainbow2_pos = rainbow1_pos + 5
            rainbow1.place(x = n * 80, y = 180, width = 80, height = 20)
            rainbow2.place(x = n * 80 + 400, y = 180, width = 80, height = 20)
    
    if game_running == False:
        rainbow1.destroy()
        rainbow2.destroy()
        return #closes thread I believe


def stirrer(pos):
    if pos == 1 or pos == 10: #can't stir if there aren't tanks on each side
        tank_screen()
    else:
        placeholder = tanks[pos - 2] #normally -1 and +1 but this is adjusted for the difference between position input and actual index
        tanks[pos - 2] = tanks [pos]
        tanks[pos] = placeholder
        global points
        points = points - 2
        tank_screen()
def centrifuge(pos):
    if pos == 1 or pos == 10: #can't centrifuge unless there's tanks on each side
        tank_screen()
    else:
        min_distance = min(pos - 1, 10 - pos) #originally pos and 9 - pos but this adjusts for human input
        for i in range(min_distance, 0, - 1): #not including step size doesn't allow the list to form (ask me)
            #the whole point of this is to count tanks on either side and swap accordingly
            placeholder = tanks[pos - i - 1] #don't get confused - the negative one comes from pos adjustment
            tanks[pos - i - 1] = tanks[pos + i - 1]
            tanks[pos + i - 1] = placeholder
        global points #global needed because you're not just reading the variable - you're reassigning it locally
        points = points - 2
        tank_screen()
def replicator(pos):
    if pos == 10: #can't replicate final tank (notice 10 instead of 9 because this isn't an index)
        tank_screen()
    else:
        for i in range(10, pos, - 1): #originally 9 and pos = index - negative ones were shifted onto the i's
            tanks[i - 1] = tanks[i - 2] #important to start from R to L unless you want all tanks to become a single color
        global points
        points = points - 2
        tank_screen()
def solvent(pos):
    global points
    if pos == 10: #no need to push anything
        tanks[pos - 1] = colors[random.randint(0,4)]
        points = points - 2
        tank_screen()
    else:
        for i in range(pos - 1, 9): #this makes me want to do rep the same way - probably possible and more consistent
            tanks[i] = tanks[i + 1]
        tanks[9] = colors[random.randint(0,4)] #randomize final tank
        points = points - 2
        tank_screen()
def catalyst(pos):
    #hardest of all
    tanks_num = [] #converts colors to numbers to be compared
    tanks_same = [] #collects indices of tanks with matching color to highlighted tank
    tanks_affected = [] #decides if tanks are consecutive or not
    color_selected = 10 #placeholder - 10 is not an option
    for i in range(0, 10): #all tanks
        for k in range(0, 5): #manual way of converting color to number
            if tanks[i] == colors[k]:
                tanks_num.append(k)
                if i == pos - 1: #-1 to adjust for user input vs index
                    color_selected = k

    for i in range(0,10): #gathers tanks matching color decided
        if tanks_num[i] == color_selected:
            tanks_same.append(i)
    
    for i in tanks_same: #dumb way to check if consecutive for each tank
        if i <= pos - 1: #simply less than pos should do the same and look cleaner
            interval = list(range(i, pos - 1))
        else:
            interval = list(range(i, pos - 1, - 1))
        #form interval of numbers between each tank and the highlighted one - check if all the numbers in the chain are same color
        if set(tanks_same).issuperset(set(interval)):
            tanks_affected.append(i)
    for i in tanks_affected:
        tanks[i] = colors_iterated[color_selected + 1] #colors_iterated instead of colors in order to go from pink to red
    global points
    points = points - 2
    tank_screen()       

#todo basic algorithms (if possible)

def tank_screen():
    global points #i couldn't get it to recognize the value any other way
    global total_points
    global game_running

    if tanks == tanks_required:
        game_running = False
        for widget in root.winfo_children():
            widget.destroy() #win - clears screen for next screen
        global current_tool
        current_tool = None
        total_points = total_points + points
        points_message = "Total Score: " + str(total_points)
        points_label = GUI.Label(root, text = points_message, font = ("Helvetica", 25))
        points_label.configure(background = "purple")
        points_label.place(x = 250, y = 150, height = 200, width = 300)

        play_again_button = GUI.Button(root, text = "Play Again", font = ("Helvetica", 20), command = tank_generator)
        play_again_button.configure(background = "cyan")
        play_again_button.place(x = 300, y = 350, height = 100, width = 200)

    else:
        stirrer = GUI.Button(root, image = stirrer_image, command = lambda: select_tool("stirrer")) #lambda lets me select function and send it an argument
        stirrer.configure(background = "purple", borderwidth= 0)
        stirrer.place(x = 360, y = 350, height = 150, width = 120)

        centrifuge = GUI.Button(root, image = centrifuge_image, command = lambda: select_tool("centrifuge"))
        centrifuge.configure(background = "purple", borderwidth= 0)
        centrifuge.place(x = 480, y = 350, height = 150, width = 120)

        replicator = GUI.Button(root, image = replicator_image, command = lambda: select_tool("replicator"))
        replicator.configure(background = "purple", borderwidth= 0)
        replicator.place(x = 240, y = 350, height = 150, width = 120)

        solvent = GUI.Button(root, image = solvent_image, command = lambda: select_tool("solvent"))
        solvent.configure(background = "purple", borderwidth= 0)
        solvent.place(x = 0, y = 350, height = 150, width = 120)

        catalyst = GUI.Button(root, image = catalyst_image, command = lambda: select_tool("catalyst"))
        catalyst.configure(background = "purple", borderwidth= 0)
        catalyst.place(x = 120, y = 350, height = 150, width = 120)

        #tanks 1-10 as currently seen
        tank1 = GUI.Button(root, command = lambda: use_tool(1)) #pos doesn't start from 0 obviously (took some time to make it this way)
        tank1.configure(background = tanks[0])
        tank1.place(x = 0, y = 200, height = 80, width = 80)

        tank2 = GUI.Button(root, command = lambda: use_tool(2))
        tank2.configure(background = tanks[1])
        tank2.place(x = 80, y = 200, height = 80, width = 80)

        tank3 = GUI.Button(root, command = lambda: use_tool(3))
        tank3.configure(background = tanks[2])
        tank3.place(x = 160, y = 200, height = 80, width = 80)

        tank4 = GUI.Button(root, command = lambda: use_tool(4))
        tank4.configure(background = tanks[3])
        tank4.place(x = 240, y = 200, height = 80, width = 80)

        tank5 = GUI.Button(root, command = lambda: use_tool(5))
        tank5.configure(background = tanks[4])
        tank5.place(x = 320, y = 200, height = 80, width = 80)

        tank6 = GUI.Button(root, command = lambda: use_tool(6))
        tank6.configure(background = tanks[5])
        tank6.place(x = 400, y = 200, height = 80, width = 80)

        tank7 = GUI.Button(root, command = lambda: use_tool(7))
        tank7.configure(background = tanks[6])
        tank7.place(x = 480, y = 200, height = 80, width = 80)

        tank8 = GUI.Button(root, command = lambda: use_tool(8))
        tank8.configure(background = tanks[7])
        tank8.place(x = 560, y = 200, height = 80, width = 80)

        tank9 = GUI.Button(root, command = lambda: use_tool(9))
        tank9.configure(background = tanks[8])
        tank9.place(x = 640, y = 200, height = 80, width = 80)

        tank10 = GUI.Button(root, command = lambda: use_tool(10))
        tank10.configure(background = tanks[9])
        tank10.place(x = 720, y = 200, height = 80, width = 80)

        #tanks 1-10 as actually required
        req1 = GUI.Label(root)
        req1.configure(background = tanks_required[0])
        req1.place(x = 25, y = 280, height = 20, width = 30)

        req2 = GUI.Label(root)
        req2.configure(background = tanks_required[1])
        req2.place(x = 105, y = 280, height = 20, width = 30)

        req3 = GUI.Label(root)
        req3.configure(background = tanks_required[2])
        req3.place(x = 185, y = 280, height = 20, width = 30)

        req4 = GUI.Label(root)
        req4.configure(background = tanks_required[3])
        req4.place(x = 265, y = 280, height = 20, width = 30)

        req5 = GUI.Label(root)
        req5.configure(background = tanks_required[4])
        req5.place(x = 345, y = 280, height = 20, width = 30)

        req6 = GUI.Label(root)
        req6.configure(background = tanks_required[5])
        req6.place(x = 425, y = 280, height = 20, width = 30)

        req7 = GUI.Label(root)
        req7.configure(background = tanks_required[6])
        req7.place(x = 505, y = 280, height = 20, width = 30)

        req8 = GUI.Label(root)
        req8.configure(background = tanks_required[7])
        req8.place(x = 585, y = 280, height = 20, width = 30)

        req9 = GUI.Label(root)
        req9.configure(background = tanks_required[8])
        req9.place(x = 665, y = 280, height = 20, width = 30)

        req10 = GUI.Label(root)
        req10.configure(background = tanks_required[9])
        req10.place(x = 745, y = 280, height = 20, width = 30)

        #current score
        points_message = "Score: " + str(points)
        points_label = GUI.Label(root, text = points_message, font= ("Helvetica", 25))
        points_label.configure(background = "purple")
        points_label.place(x = 250, y = 0, height = 150, width = 300)

total_points = 0
root = GUI.Tk() #creates the window/parent
root.title("Chemsynth")
root.geometry("800x500") #x by y
root.resizable(False, False) #one for each dimension
root.configure(background = "purple") #configure is usable for all widgets


current_dir = os.path.dirname(os.path.abspath(__file__))
stirrer_image = GUI.PhotoImage(file = os.path.join(current_dir, "Stirrer.png"))
centrifuge_image = GUI.PhotoImage(file = os.path.join(current_dir, "Centrifuge.png"))
replicator_image = GUI.PhotoImage(file = os.path.join(current_dir, "Replicator.png"))
solvent_image = GUI.PhotoImage(file = os.path.join(current_dir, "Solvent.png"))
catalyst_image = GUI.PhotoImage(file = os.path.join(current_dir, "Catalyst.png"))
rainbow_image = GUI.PhotoImage(file = os.path.join(current_dir, "Rainbow.png"))


start_button = GUI.Button(root, text = "Play", command = tank_generator, font = ("Helvetica", 25)) #first argument is parent it belongs to - command is name of function WITHOUT ()
start_button.configure(background = "cyan")
start_button.place(x = 300, y = 225, width = 200, height = 50) #also possible to use pack() and grid()

root.mainloop() #runs the window