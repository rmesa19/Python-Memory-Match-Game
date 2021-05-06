
import turtle
import random
import time

def draw_leaderboard(pen):
    try:
        with open('leaderboard.txt', mode = 'r') as standing:
            board_array = []
            for lines in standing:
                board_array.append(lines)
        pen.color('blue')
        pen.goto(240,280)
        pen.down()
        for i in range(len(board_array)):
            pen.write(board_array[i],font=('Arial',12))
            pen.up()
            pen.goto(240, pen.ycor()-20)
            pen.down()
    except:
        error = turtle.Turtle()
        error.shape('leaderboard_error.gif')
        time.sleep(2)
        quit()
        
def custom_images():
    try:
        with open('config.txt', mode ="r") as custom:
            bank = []
            for lines in custom:
                lines = lines.strip()
                bank.append(lines)
        return bank
    except:
        error = turtle.Turtle()
        error.shape('file_error.gif')
        time.sleep(2)
        quit()

def save_leaderboard(mainclass):
    def reverse_bubble_sort(my_list):
        for passnum in range(len(my_list)-1,0,-1):
            for i in range(passnum):
                if my_list[i][1]>my_list[i+1][1]:
                    temp = my_list[i]
                    my_list[i] = my_list[i+1]
                    my_list[i+1] = temp
        return my_list[-1::-1]
    try:
        with open('leaderboard.txt', mode = 'r') as standing:
            board_array = []
            for lines in standing:
                lines = lines.replace(':','')
                scoreline = lines.split()
                board_array.append(scoreline)
            board_array.append([mainclass.guess, mainclass.player_name])
            for i in range(len(board_array)):
                if type(board_array[i][0]) == str:
                    board_array[i][0]= board_array[i][0][:2]
                    board_array[i][0] = int(board_array[i][0])
            new_listing = reverse_bubble_sort(board_array)
            if len(new_listing) == 9:
                new_listing.pop(8)
                
        with open('leaderboard.txt', mode = 'w') as outfile:
            for i in range(len(new_listing)):
                outfile.write(str(new_listing[i][0])+': '+str(new_listing[i][1])\
                            +'\n')
    except:
        error = turtle.Turtle()
        error.shape('leaderboard_error.gif')
        time.sleep(2)
        quit()
    
def draw_match(turtle):
    turtle.goto(-70,-320)
    turtle.down()
    turtle.write("0", font=('Arial',12,'bold'))

def draw_guess(turtle):
    turtle.goto(-270,-320)
    turtle.down()
    turtle.write("0", font=('Arial',12,'bold'))
    
def create_quad(pen, xside, yside):
    pen.down()
    for i in range(2):
        pen.forward(xside)
        pen.left(90)
        pen.forward(yside)
        pen.left(90)
    pen.up()

def build_board(pen, x, y):
    pen.pensize(4)
    pen.setposition(-.45*x,-.3*y)
    create_quad(pen, .65*x, .75*y)
    pen.setposition(.25*x,-.3*y)
    create_quad(pen, .2*x, .75*y)
    pen.setposition(-.45*x,-.45*y)
    create_quad(pen, .65*x, .1*y)
    
    def draw_status(pen,x,y,msg):
        pen.goto(x,y)
        pen.down()
        pen.write(msg,font=('Arial',12,'bold'))
        pen.up()
    draw_status(pen,-350,-300,"Status: ")
    draw_status(pen,-350,-320,"Guesses: ")
    draw_status(pen,-150,-320,"Matched: ")
    pen.goto(300,-320)
    pen.shape('quitbutton.gif')
    pen.st()

def card_eval(class_index, cardlist,x,y):
    for i in range(len(cardlist)):
            if cardlist[i].flipped == True:
                class_index.append(i)
    if len(class_index) < 2:
        for i in range(len(cardlist)):
            if (cardlist[i].turtle.xcor()-50 < x \
            <cardlist[i].turtle.xcor()+50 ) \
            and (cardlist[i].turtle.ycor()-75 < \
                y < cardlist[i].turtle.ycor()+75) and \
                cardlist[i].turtle.isvisible():
                cardlist[i].turtle.shape(cardlist[i].front)
                cardlist[i].flipped = True
                class_index.append(i)

def twocard_eval(mainclass):
    def update_guess(mainclass):
        mainclass.turtle_bank[1].clear()
        mainclass.guess += 1
        mainclass.turtle_bank[1].write(mainclass.guess,font=('Arial',12,'bold'))
        
    def update_match(mainclass):
        mainclass.turtle_bank[2].clear()
        mainclass.match += 1
        mainclass.turtle_bank[2].write(mainclass.match,font=('Arial',12,'bold'))
        
    if len(mainclass.flipped_index) == 2:
        update_guess(mainclass)
        time.sleep(1)
        if mainclass.gamecard_bank[mainclass.flipped_index[0]].front == \
           mainclass.gamecard_bank[mainclass.flipped_index[1]].front:
            update_match(mainclass)
            for element in mainclass.flipped_index:
                mainclass.gamecard_bank[element].turtle.ht()
                mainclass.gamecard_bank[element].flipped = False
        else:
            for element in mainclass.flipped_index:
                mainclass.gamecard_bank[element].turtle.shape(mainclass.\
                                                              gamecard_bank[element]\
                                                              .back)
                mainclass.gamecard_bank[element].flipped = False
                
                
def winner(mainclass):
    if mainclass.match == int(mainclass.game_size/2):
        mainclass.turtle_bank[3].shape('winner.gif')
        mainclass.turtle_bank[3].st()
        save_leaderboard(mainclass)
        draw_leaderboard(mainclass.turtle_bank[5])
        time.sleep(3)
        quit()
        
        
        
def quitbutton(mainclass, x, y):
    if mainclass.turtle_bank[0].xcor()-30 < x < mainclass.turtle_bank[0].xcor()+30\
       and mainclass.turtle_bank[0].ycor()-20 < y < \
        mainclass.turtle_bank[0].ycor()+ 20:
        mainclass.turtle_bank[4].shape('quitmsg.gif')
        mainclass.turtle_bank[4].st()
        time.sleep(3)
        quit()
        
    
                    
class StatusBox:
    '''
    Main Object Class used to handle drawing of gameboard
    and management of game variables.
    '''
    def __init__(self):
        self.window = turtle.Screen()
        self.window.setup(800,800)
        self.player_name = turtle.textinput("Game Setup","Enter your name.")
        self.game_size = 0
        self.guess = 0
        self.match = 0
        self.flipped_index = []
        self.turtle_bank = []
        self.cardface_bank = custom_images()
        self.settings_bank = ['file_error.gif','card_warning.gif',\
                              'card_back.gif','leaderboard_error.gif',\
                              'quitbutton.gif','quitmsg.gif','winner.gif']
        self.gamecard_bank = []
        for i in range(len(self.cardface_bank)):
            self.window.addshape(self.cardface_bank[i])
        for i in range(len(self.settings_bank)):
            self.window.addshape(self.settings_bank[i])
                     
        for i in range(6):
            self.turtle_bank.append(turtle.Turtle())
            self.turtle_bank[i].speed(0)
            self.turtle_bank[i].ht()
            self.turtle_bank[i].up()
            
        while self.game_size != 8 or self.game_size != 10 or self.game_size != 12:
            self.game_size = int(turtle.numinput("Game Setup",\
                                    "Enter Number of Cards to Play (8, 10, or 12)",\
                                    8, 8, 12))
            if self.game_size == None:
                continue
            if self.game_size == 8 or self.game_size == 10 or self.game_size == 12:
                break
            
                
            
        build_board(self.turtle_bank[0], 800, 800)
        draw_guess(self.turtle_bank[1])
        draw_match(self.turtle_bank[2])
        draw_leaderboard(self.turtle_bank[5])
        
        
        
class card:
    def __init__(self, turtle, front, back):
        self.turtle = turtle
        self.front = front
        self.back = back
        self.flipped = False
    
    
def place_cards(deck):
    for k in range(len(deck)):
        deck[k].turtle.speed(0)
        deck[k].turtle.penup()
        deck[k].turtle.ht()
        deck[k].turtle.shape(deck[k].back)
        deck[k].turtle.goto(((k%4)-\
                                    4)*100+100, 100)
        deck[k].turtle.st()
    for i in range(4,8):
        deck[i].turtle.sety(250)
    if len(deck)>8:
        for i in range(8,len(deck)):
            deck[i].turtle.sety(-50)
    
def main():
    
    Status_Box = StatusBox()
    random.shuffle(Status_Box.cardface_bank)
    
    for i in range(int(Status_Box.game_size/2)):
        for j in range(2):
            Status_Box.gamecard_bank.append(card(turtle.Turtle(),\
                                                 Status_Box.cardface_bank[i],\
                                                 'card_back.gif'))

    random.shuffle(Status_Box.gamecard_bank)        
    place_cards(Status_Box.gamecard_bank)
    
    def click(x,y):
        Status_Box.flipped_index = []
        quitbutton(Status_Box, x, y)
        card_eval(Status_Box.flipped_index, Status_Box.gamecard_bank,x,y)
        twocard_eval(Status_Box)
        winner(Status_Box)
        
    Status_Box.window.onclick(click)
    Status_Box.window.listen()


if __name__ == "__main__":
    main()
