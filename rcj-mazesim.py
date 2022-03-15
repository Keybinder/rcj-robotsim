"""
functions to implement:

(robot)
- cam_front(), cam_left, cam_right - returns "wall", "tile", "rampup" etc.
- col_front(), _left, _right - returns "black", "white", "green" etc.
- move(units, type="tile") - negative moves backwards, must have "ramp" move type to move on ramps

"""

# Change filename on line 226 to change which maze is loaded in

from tkinter import *
import random

# GLOBAL VARS
tick = 200
gheight, gwidth = 600, 800
buf=20

class Maze():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tiles = [["white" for i in range(y)] for j in range(x)]
        self.walls = [[[False, False, False, False] for i in range(y)] for j in range(x)]
        self.visited = [[False for i in range(y)] for j in range(x)]
    def draw(self):
        cv.delete("maze")
        for x in range(self.x):
            for y in range(self.y):
                if self.visited[x][y]:
                    cv.create_rectangle(maze2st(maze,[x,y]),maze2st(maze,[x+1,y+1]),fill="light blue",outline="grey",tags="maze")
                else:
                    cv.create_rectangle(maze2st(maze,[x,y]),maze2st(maze,[x+1,y+1]),fill=maze.tiles[x][y],outline="grey",tags="maze")
                if maze.walls[x][y][0]:
                    cv.create_line(maze2st(maze,[x,y+1]),maze2st(maze,[x+1,y+1]),fill="black",width=3,tags="maze")
                if maze.walls[x][y][1]:
                    cv.create_line(maze2st(maze,[x+1,y+1]),maze2st(maze,[x+1,y]),fill="black",width=3,tags="maze")
                if maze.walls[x][y][2]:
                    cv.create_line(maze2st(maze,[x,y]),maze2st(maze,[x+1,y]),fill="black",width=3,tags="maze")
                if maze.walls[x][y][3]:
                    cv.create_line(maze2st(maze,[x,y+1]),maze2st(maze,[x,y]),fill="black",width=3,tags="maze")
        hf.update_idletasks()
        hf.update()
        
class Bot():
    def __init__(self,maze,x,y,direction):
        self.maze=maze
        self.x=x
        self.y=y
        self.direction=direction
    def draw(self):
        cv.delete("robot")
        if self.direction == 0:
            apex = maze2st(self.maze,[self.x+0.5,self.y+0.9])
        elif self.direction ==1:
            apex = maze2st(self.maze,[self.x+0.9,self.y+0.5])
        elif self.direction ==2:
            apex = maze2st(self.maze,[self.x+0.5,self.y+0.1])
        elif self.direction ==3:
            apex = maze2st(self.maze,[self.x+0.1,self.y+0.5])

        if self.direction%2==1: # left or right
            cv.create_line(maze2st(self.maze,[self.x+0.5,self.y+0.1]),maze2st(self.maze,[self.x+0.5,self.y+0.9]),fill="red",width=3,tags=("robot"))
            cv.create_line(maze2st(self.maze,[self.x+0.5,self.y+0.1]),apex,fill="red",width=3,tags=("robot"))
            cv.create_line(apex,maze2st(self.maze,[self.x+0.5,self.y+0.9]),fill="red",width=3,tags=("robot"))
        else:
            cv.create_line(maze2st(self.maze,[self.x+0.1,self.y+0.5]),maze2st(self.maze,[self.x+0.9,self.y+0.5]),fill="red",width=3,tags=("robot"))
            cv.create_line(maze2st(self.maze,[self.x+0.1,self.y+0.5]),apex,fill="red",width=3,tags=("robot"))
            cv.create_line(apex,maze2st(self.maze,[self.x+0.9,self.y+0.5]),fill="red",width=3,tags=("robot"))
        hf.update_idletasks()
        hf.update()

    def move(self, units):
        while units > 0:
            if maze.walls[self.x][self.y][self.direction]:
                print("CRASH!!!")
                break
            if self.direction==0:
                self.y += 1
            elif self.direction ==1:
                self.x += 1
            elif self.direction ==2:
                self.y -= 1
            elif self.direction ==3:
                self.x -= 1
            units -= 1
        self.maze.visited[self.x][self.y] = True
        self.maze.draw()
        self.draw()
        hf.after(tick)
        
    def cam(self, pointed):
        if pointed == "forward":
            if maze.walls[self.x][self.y][self.direction]:
                return "wall"
            else:
                return "tile"
        elif pointed == "left":
            if maze.walls[self.x][self.y][(self.direction-1)%4]:
                return "wall"
            else:
                return "tile"
        elif pointed =="right":
            if maze.walls[self.x][self.y][(self.direction+1)%4]:
                return "wall"
            else:
                return "tile"
        hf.after(tick)
        
    def turn(self, degrees):
        degrees = degrees / 90
        self.direction = (self.direction + int(degrees)) % 4
        self.draw()
        hf.after(tick)

def gen_rand_maze(cols,rows):
    maze = Maze(cols,rows)
    global mazex
    global mazey
    mazex, mazey = cols, rows
    magic0 = 0.4
    # set perimeter of maze to walls
    # top and bottom edges
    for x in range(cols):
        maze.walls[x][-1][0] = True
        maze.walls[x][0][2] = True
    # right and left edges
    for y in range(rows):
        maze.walls[-1][y][1] = True
        maze.walls[0][y][3] = True

    # set all tiles randomly FIRST
    for x in range(cols-1):
        for y in range(rows-1):
            if random.random() <= magic0:
                #print("set " + str(x) + " " + str(y) + " right")
                maze.walls[x][y][1] = True
                maze.walls[x+1][y][3] = True
            if random.random() <= magic0:
                #print("set " + str(x) + " " + str(y) + " top")
                maze.walls[x][y][0] = True
                maze.walls[x][y+1][2] = True
    
    # TODO: generate snaking path to exit
    # possibility: generate straightline path then keep adding kinks?
        
    # remove some percentage of this path's walls
    
    return maze

def load_maze(maze_file):
    with open(maze_file, 'r') as infile:
        line0 = infile.readline()
        cols = len(line0)//2 -1
        lines = infile.readlines()
        rows = int(len(lines)/2)
    global mazex
    global mazey
    mazex, mazey = cols, rows
    maze = Maze(cols, rows)
    # proc 1st line
    for i in range(cols):
        if line0[2*i+1] == '#':
            maze.walls[i][rows-1][0] = True
    # proc right and left edge
    for i in range(0, rows*2, 2):
        if lines[i][0] == '#':
            #print("set 0 " + str((rows-i)//2+1) + " left")
            maze.walls[0][(rows-i+1)//2+1][3] = True
        if lines[i][-2] == '#': # this is -2 to bypass the '\n'
            #print("set 3 " + str((rows-i)//2+1) + " right")
            maze.walls[-1][(rows-i+1)//2+1][1] = True
    # proc vertical lines in middle section
    for frow1 in range(0, rows*2, 2):
        #print(str(frow1))
        #vertical walls
        for fcol1 in range(2, cols*2, 2):
            #print("!: " + lines[frow1][fcol1])
            #print("col, row = " + str(fcol1//2-1) + " " + str((rows-frow1)//2))
            if lines[frow1][fcol1] == '#':
                maze.walls[fcol1//2-1][(rows-frow1+1)//2+1][1] = True
                maze.walls[fcol1//2][(rows-frow1+1)//2+1][3] = True
    # proc horizontal lines in middle section excluding last line
    for frow1 in range(1, rows*2-1, 2):
        #print(str(frow1))
        #vertical walls
        for fcol1 in range(1, cols*2, 2):
            #print("!: " + lines[frow1][fcol1])
            #print("col, row = " + str(fcol1//2) + " " + str((rows-frow1+1)//2))
            if lines[frow1][fcol1] == '#':
                maze.walls[fcol1//2][(rows-frow1)//2+1][0] = True
                maze.walls[fcol1//2][(rows-frow1)//2+2][2] = True
    # proc bottom horizontals of last line
    for i in range(cols):
        if lines[-1][2*i+1] == '#':
            maze.walls[i][0][2] = True
    return maze
        
def maze2st(maze, p):
    return mx0+p[0]*tile_pixlen, my0-p[1]*tile_pixlen

def display_init():
    global hf
    hf = Tk()
    global cv
    cv = Canvas(hf, width=gwidth, height=gheight, bg="gray")
    cv.pack()

def display_maze(maze):
    # draw tiles
    for x in range(maze.x):
        for y in range(maze.y):
            cv.create_rectangle(maze2st(maze,[x,y]),maze2st(maze,[x+1,y+1]),fill=maze.tiles[x][y],outline="grey")
            if maze.walls[x][y][0]:
                cv.create_line(maze2st(maze,[x,y+1]),maze2st(maze,[x+1,y+1]),fill="black",width=3)
            if maze.walls[x][y][1]:
                cv.create_line(maze2st(maze,[x+1,y+1]),maze2st(maze,[x+1,y]),fill="black",width=3)
            if maze.walls[x][y][2]:
                cv.create_line(maze2st(maze,[x,y]),maze2st(maze,[x+1,y]),fill="black",width=3)
            if maze.walls[x][y][3]:
                cv.create_line(maze2st(maze,[x,y+1]),maze2st(maze,[x,y]),fill="black",width=3)

#maze = gen_rand_maze(mazex,mazey)
maze = load_maze("maze0.txt")

# set up display
if (gwidth-2*buf)/mazex < (gheight-2*buf)/mazey:
    tile_pixlen = (gwidth-2*buf)/mazex
    mx0 = buf
    my0 = gheight-(gheight-mazey*tile_pixlen)/2
else:
    tile_pixlen = (gheight-2 *buf)/mazey
    mx0 = (gwidth-mazex*tile_pixlen)/2
    my0 = gheight-buf

display_init()

bot = Bot(maze, mazex//2, 0, 0)
maze.visited[mazex//2][0] = True
maze.draw()

############

def bot_prog():
    bot.turn(90)
    while True:
        if bot.cam("forward") == "wall":
            bot.turn(-90)
        else:
            bot.move(1)
            bot.turn(90)
            
############

bot.draw()
hf.after(1000)

bot_prog()
