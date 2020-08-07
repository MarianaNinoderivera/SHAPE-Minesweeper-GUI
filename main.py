import random
from tkinter import Tk, Canvas

def createboard(width, height):
    gameboard = []
    for row in range(height):  #height = 3
        gameboard.append([])
        for col in range(width):  #width = 3
            
            gameboard[row].append(None)

    return gameboard

#board = createboard(3, 4)


# one control structure to bury mines n times
def bury_mines(gameboard, n):
  
  
  row = len(gameboard)
  column = len(gameboard[0])
  mine = -1
    

  mine_count = 0
  while mine_count < n:   
    random_column = random.randint(0, column - 1)
    random_row = random.randint(0, row - 1)
    #if random position has a mine
    while gameboard[random_row][random_column] == mine:
      random_column = random.randint(0, column - 1)
      random_row = random.randint(0, row - 1)

    #add a mine to random position
    gameboard[random_row][random_column] = mine
    
    mine_count += 1

def get_mine_count(gameboard, r,c):
  count = 0
  for i in [-1,0,1]:
    for j in [-1,0,1]:
      if (i!=0 or j!=0):            
        new_r = r+i
        new_c = c+j
        if new_r >= 0 and new_r < len(gameboard) and \
          new_c >= 0 and new_c < len(gameboard[0]):
              if gameboard[new_r][new_c] == -1: 
                count += 1
  return count
       

#uncover board at position (x,y)
def uncover_board(gameboard,r,c):

  #if this location has already been uncovered, stop
  if gameboard[r][c] != None:
    return 

  count = get_mine_count(gameboard, r, c)

  if count > 0:
    gameboard[r][c]= count
  else:
    gameboard[r][c] = 0
    
    #look at every neighbor and get mine count
    for i in [-1,0,1]:
      for j in [-1,0,1]:
        if (i!=0 or j!=0):            
          new_r = r+i
          new_c = c+j
          if new_r >= 0 and new_r < len(gameboard) and \
             new_c >= 0 and new_c < len(gameboard[0]):
            uncover_board(gameboard, new_r, new_c)

def check_won(gameboard):
  
  won = True
  for k in range(len(gameboard)):
    for i in range(len(gameboard[0])):
      #every cell hasn't been uncovered
      if gameboard[k][i]== None:        
        won = False

  return won

#Displaying the Board
#draws grid on canvas 
def display_board(board, canvas, width, height): 

  for r in range(len(board)):
    for c in range(len(board[0])):
      #top left and lower right coordinates for each cell
      if board[r][c]== None or board[r][c]== -1:
        canvas.create_rectangle(width*c,height*r, width*(c+1), height*(r+1), fill="#b5e8e8")
      elif board[r][c] > 0:
        canvas.create_rectangle(width*c,height*r, width*(c+1), height*(r+1), fill="#e8b5e8")
        canvas.create_text(width*c+(width//2),height*r+(height//2),text=str(board[r][c]), font=('Times',20))
      else: 
        canvas.create_rectangle(width*c,height*r, width*(c+1), height*(r+1), fill="white")



def display_end_board(board, canvas, width, height): 

  for r in range(len(board)):
    for c in range(len(board[0])):
      #top left and lower right coordinates for each cell
      if board[r][c]== -1:
        canvas.create_rectangle(width*c,height*r, width*(c+1), height*(r+1), fill="#e7b1cb")
        
        canvas.create_text(width*c+(width//2), height*r+(height//2), text = "Bomb")
      else: 
        canvas.create_rectangle(width*c,height*r, width*(c+1), height*(r+1), fill="white")


  

#Setting up a new game
def run():
  #create gameboard and bury mines
  width = 8 
  height = 10
  board = createboard(width, height)
  bury_mines(board, 9)    

  # Create GUI widgets
  root = Tk()
  root.wm_title("Minesweeper")
  heightpxls = 500
  widthpxls = 600
  canvas = Canvas(master=root, height=heightpxls, width = widthpxls)
  canvas.pack()

  cellwidth = widthpxls//len(board[0])
  cellheight = heightpxls//len(board)

  display_board(board, canvas, cellwidth, cellheight)


  def handle_click(event):
    #take pixel location
    event.x
    event.y
    #print(event.x, event.y)

    #translate into row and column index
    logical_x = event.x // cellwidth
    logical_y = event.y // cellheight
    print(logical_x, logical_y)
    
    
    uncover_board(board,logical_y,logical_x)

    display_board(board, canvas, cellwidth, cellheight)

    if check_won(board):
      canvas.unbind("<Button-1>")
      canvas.create_text(widthpxls//2,heightpxls//2,text="You Won!",font=('Times',70))
      
    elif board[logical_y][logical_x] ==-1:
      canvas.unbind("<Button-1>")

      display_end_board(board, canvas, cellwidth, cellheight)

      canvas.create_text(widthpxls//2,heightpxls//2,text="You Lose!",font=('Times',70))


  canvas.bind("<Button-1>", handle_click)


  root.mainloop()

run()

