import pygame
import random

#lambda, list comprehenssion


# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main 
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

#97791914

# SHAPE FORMATS each list is a rotation 

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....', 
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece(object):
    def __init__(self,x ,y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0
        

def create_grid(locked_pos={}):
    grid = [[(0,0,0) for _ in range (10)] for _ in range (20)]
    #A list comprehension is a syntactic construct available in some
    #programming languages for creating a list based on existing lists. 
    #List comprehension in Python is a concise way of creating lists
    #from the ones that already exist. 
    for i in range (len(grid)):
        for j in range(len(grid[i])):
            if(j,i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] =c
    return grid

def convert_shape_format(shape):
    positions = []
    #                    this will return the index we should get from the list to get tge right ont
    #               in case t have 4 sub lists 0~3  so 4%3=1 which is the index we are searcing for 
    format = shape.shape[shape.rotation % len(shape.shape)] #give us the sub list of the list

    for i, line in enumerate(format):
        row = list(line)
        for j, columns in enumerate(row):
            if columns == '0':
                positions.append((shape.x + j, shape.y + i))

                
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] -2, pos[1]-4)

    return positions

def valid_space(shape, grid):#add this position as available if the position is empty by cheking the color of the square      
    accepted_pos = [[(j, i )for j in range(10) if grid[i][j] == (0,0,0)]for i in range(20)]# getting every single posible position for a 10*20 gid 
    #convering this into a 1d list
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] >-1:
                return False
    return True

        

def check_lost(positions):#if we went above the screen we loss
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(5,0,random.choice(shapes))

def draw_text_middle(text, size, color, surface):  
    pass
   
def draw_grid(surface,grid):
    sx = top_left_x
    sy = top_left_y

    for i in range (len(grid)):#rows
        pygame.draw.line(surface,(128,128,128),(sx,sy+i*block_size), (sx+play_width, sy+ i*block_size))
        for j in range(len(grid[i])): #columns in each row
            pygame.draw.line(surface,(128,128,128),(sx+j*block_size, sy), (sx+j*block_size, sy+ play_height))



def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1 ,-1 ,-1):# loop the grid backwords
        row = grid[i]
        if (0,0,0) not in row:# there is no black squares in the row 
            inc += 1
            ind = i
            for j in range(len(row)): #loop through each square in the row 
                try:
                    del locked[(j,i)] #and delete the row from the locked positions
                except:
                    continue

    #we need to shift evenry thing 1 step bellow when we delete a row
    if inc > 0:
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
            x,y =key#getting the x and y of each key in locked positions 
            if y < ind:# the y value of oue key is above th e index of the row we removed(if we removed row 17 every thing above that will only will shift)
                newKey = (x,y+inc) # getting a new key with the same x but y is incremented by certain value to shift it down
                locked[newKey] = locked.pop(key)

    return inc
            


                    
def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsan',30)
    label = font.render('next shape', 1, (255,255,255))
    #where are we gonna draw the shape and the 'next line' string
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':#if the element =0 draw a rectangle 
                pygame.draw.rect(surface, shape.color,(sx+j*30, sy+i*block_size, block_size,block_size),0)
    #drawing the shape and the string on the screen 
    surface.blit(label, (sx+10, sy-30))
    #we didnt do it like we did to draw the falling shape because here we dont
    #need to save the positions of the squares we only need to display the next shape


    

def draw_window(surface, grid, score = 10):
    surface.fill((0,0,0))
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255,255,255))

    surface.blit(label,(top_left_x + play_width/2 - (label.get_width()/2),30))

    font = pygame.font.SysFont('comicsan',30)
    label = font.render('score '+ str(score), 1, (255,255,255))
    #where are we gonna draw the shape and the 'next line' string
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    surface.blit(label,(sx+20,sy+160))

    for i in range(len(grid)):
        for j in range (len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y+i*block_size, block_size, block_size),0)


    pygame.draw.rect(surface,(255,0,0),(top_left_x, top_left_y, play_width, play_height),4)
    
    
    draw_grid(surface, grid)
    #pygame.display.update()


def main(win):
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27 #how long is it gonna take before each piece starts falling
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()# gets the time since the last time the clock got ticked, and add the amount of time the loop took to loop
        level_time +=  clock.get_rawtime()
        clock.tick()

        if level_time/1000 >0:
            level_time = 0
            if fall_speed >0.12:
                fall_speed -= 0.005                


                
        if fall_time/1000 > fall_speed:
            fall_time =0
            current_piece.y += 1
            #if we moved to a position that is not valid that meens we either hit the bottom or we hit another piece
            #so we need to stop this piece and change it so set the change piece bool to True 
            if not (valid_space(current_piece, grid)) and current_piece.y >0:
                current_piece.y -= 1 # becuase we incremented it so we are decrementing it as the place is not valid, so we incr and decre all before the win was updated so noting happend on the screen only in code 
                change_piece = True # since the place is not valid we will change the piece and get another to fall and set the bool for true to later lock the position of the piece 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_LEFT:
                    current_piece.x -=1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x +=1

                if event.key ==pygame.K_RIGHT:
                    current_piece.x +=1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -=1

                if event.key ==pygame.K_DOWN:
                    current_piece.y +=1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -=1

                if event.key ==pygame.K_UP:
                    current_piece.rotation +=1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -=1


        shape_pos = convert_shape_format(current_piece)#the shape structure (what cubes should be colored)
        for i in range(len(shape_pos)):
            x,y = shape_pos[i]
            if y > -1:#we are not above the screen 
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) *10
            #why call this function when the changs piece hits the ground
            #becuase you could be moving down the screen and at some point you while the piece is stil moving it could complete a row and delete it even though it is the wrong row 
            
        
        draw_window(win, grid, score)
        draw_next_shape(next_piece, win)#should be after the draw window to show 
        pygame.display.update()
        
        if check_lost(locked_positions):
            run = False

    pygame.display.quit()
     

def main_menu(win):
    main(win)


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)  # start game
