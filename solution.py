import time
import math
from random import randint
import sys
fname = input('File name to save the game to: ')
f = open(fname, 'a')
def print(x='', end='\n'):
  sys.stdout.write(str(x) + end)
  f.write(str(x) + end)
def initarr(f, x, y):
  return [[f]*x for i in range(y)]
# function that creates the board evertime until you win
def layout(gridLayout):
  storeNumOut = 0;
  # prints the row and column numbers
  #System.out.print("0 1 2 3 4 5 6 7 8 9");
  print("  ",end='');
  for i in range(len(gridLayout)):
    print(i,end='');
    if (i != len(gridLayout) - 1):
      print(" ",end='');
  
  
  # Nested for loop that prints the board
  for r in range(len(gridLayout)):
    # These lines prthe numbers of the columns by starting
    # each row with a number
    print();
    print(storeNumOut,end='');
    storeNumOut += 1;
  
    """
     * Checks if the tile is True or False: by default all tiles are False
     * (Note: This allows the next board that is printed to have the "-" and
     * "x" in the spot that is a hit or miss from the previous attempt)
     """
    for c in range(len(gridLayout[r])):
      # if statement that marks "-" if tile False and "x" if tile is True
      # (Note: Tiles that are True are the tiles that have ships on them)
      if (gridLayout[r][c] == 2):
        print("\u001B[31m O \u001B[0m",end='');
      elif (gridLayout[r][c] == 0):
        print(" - ",end='');
      elif (gridLayout[r][c] == 1):
        print("\u001B[32m X \u001B[0m",end='');
  print();

def readcoord(size):
  working = False
  while not working:
    #err = False
    try:
      rowInput = int(input('Pick a row: '))
      columnInput = int(input("Pick a column: "))
    except ValueError:
      print('You may only enter integers. Please try again')
      #global err
      #err = True
      working = False
      continue
    # Checks if the user inputs are in bound from 0 to 9
    if (rowInput > size-1 or rowInput < 0 or columnInput > size-1 or columnInput < 0):
      print("Input not allowed in grid. Please try again");
      #rowInput = int(input('Pick a row: '))
      #columnInput = int(input("Pick a column: "))
      working = False
      continue
    working = True
  return (rowInput, columnInput)
def readships(size):
  coords = []
  print('Please enter in one coordinate of your two-spaced ship and the direction the other coordinate is in.')
  coord12 = readcoord(size)
  dir = input('Direction (Up/Down/Left/Right): ')
  while not (dir == 'Up' or dir == 'Down' or dir == 'Left' or dir == 'Right'):
    dir = input('Direction (Up/Down/Left/Right): ')
  if dir == 'Up':
    coord22 = (coord12[0]-1,coord12[1])
  elif dir == 'Down':
    coord22 = (coord12[0]+1,coord12[1])
  elif dir == 'Left':
    coord22 = (coord12[0],coord12[1]-1)
  elif dir == 'Right':
    coord22 = (coord12[0],coord12[1]+1)
  coords.append(coord12)
  coords.append(coord22)
  print('Enter the coordinate for the edge of the three-spaced ship:')
  coord1 = readcoord(size)
  dir = input('Direction (Up/Down/Left/Right): ')
  while not (dir == 'Up' or dir == 'Down' or dir == 'Left' or dir == 'Right'):
    dir = input('Direction (Up/Down/Left/Right): ')
  if dir == 'Up':
    coords.extend([coord1, (coord1[0]-1, coord1[1]), (coord1[0]-2, coord1[1])])
  elif dir == 'Down':
    coords.extend([coord1, (coord1[0]+1, coord1[1]), (coord1[0]+2, coord1[1])])
  elif dir == 'Left':
    coords.extend([coord1, (coord1[0], coord1[1]-1), (coord1[0]-2, coord1[1]-2)])
  elif dir == 'Right':
    coords.extend([coord1, (coord1[0], coord1[1]+1), (coord1[0]-2, coord1[1]+2)])
  return coords
def guess(size):
  if len(guessqueue)>0:
    while len(guessqueue) > 0 and aiHistory[guessqueue[0][0]][guessqueue[0][1]] != 0:
      del guessqueue[0]
    if len(guessqueue)>0:
      return guessqueue[0]
    #del guessqueue[0]
  x = randint(0, size-1)
  y = randint(0, size-1)
  while aiHistory[x][y] != 0:
    x = randint(0, size-1)
    y = randint(0, size-1)
  return (x,y)
  #return (randint(0, size-1), randint(0, size-1))
def workingcoord(size,coord):
  return (0 <= coord[0] and coord[0] <= size-1 and 0 <= coord[1] and coord[1] <= size-1)
#print(readcoord(9))
NONE = 0;
HIT = 1;
MISS = 2;
# This is the main method where we can call functions
# n is a Scanner object
print(
"Welcome to Battleship!  Your objective is to sink all of the enemy's ships."
+ "There's one 2-spaced ship and one 3-spaced ship hidden below the surface."
);
print();
#print("Please enter the length of the board (Between 3-9): ");
size = 0;
first = True;
aihits = 0;
while True:
  if not first:
    print("You may only have a board with length between 3-9.");
  else:
    first = False;
  try:
    size = int(input("Please enter the length of the board (Between 3-9): "));
  except ValueError:
    print("You may only enter integers.");
    first = True;
  if not (first or not (3 <= size and size <= 9)):
    break

# Here we create a grid of 10 by 10 where each tile is a bool
gridLayout = initarr(0, size, size); # 0 = none, 1 = hit, 2 = miss

# Prthe grid
layout(gridLayout);

numberOfTry = 0;
numberOfHits = 0;
# number of ships on the board
numberOfSquares = 5;
guessqueue=[]
# Create the grid where the ships can be placed (same as the gridLayout)
shipArray = initarr(False, size, size);
miss = initarr(0, size, size); # 0 = none, 1 = hit, 2 = miss
yourShips = initarr(False, size, size)
aiHistory = initarr(0, size, size)
# read in ships
for coord in readships(size):
  yourShips[coord[0]][coord[1]] = True
#print(yourShips)
# One random position on the grid
# Start poof the shipsrandint(0, size-1)
randStartRow = randint(0, size-1);
randStartCol = randint(0, size-1);
storeShip1Row = randint(0, size-1);
storeShip1Col = randint(0, size-1);
#storeShip1Col = 1;
# Set the tile that storeShip1 and storShip2 are on to True
if size != 3:
  shipArray[storeShip1Row][randStartCol] = True;
  shipArray[randStartRow][storeShip1Col] = True;
  
  # Check if the storeShip1Row is on on row 9: If it is then add another ship
  # that is 1 to the left and set that tile to True ; if not then add a ship 1 to
  # the right and set that tile to True (Note: the storeShip1Row is 2 tiles long)
  if (storeShip1Row == size-1):
    storeShip1Row -= 1;
    shipArray[storeShip1Row][randStartCol] = True;
  else:
    storeShip1Row += 1;
    shipArray[storeShip1Row][randStartCol] = True;
  #print(storeShip1Col);
  # Check if the storeShip1Col is on the 9th tile: if it is not then add 3 ships
  # down and set all to True else add 3 ships up and set them to True
  if (storeShip1Col + 2 <= size-1): #+3 or +2? I think it's +2
    #print("choose1");
    shipArray[randStartRow][storeShip1Col + 1] = True;
    shipArray[randStartRow][storeShip1Col + 2] = True;
  elif (storeShip1Col - 2 >= 0):
    #print("choose2");
    shipArray[randStartRow][storeShip1Col - 1] = True;
    shipArray[randStartRow][storeShip1Col - 2] = True;
else:
  type = randint(0,1);
  if (type == 1):
    # row
    shipArray[randStartRow][0] = True;
    shipArray[randStartRow][1] = True;
    shipArray[randStartRow][2] = True;
    type2 = randint(0,1);
    exclude = randint(0,2);
    if exclude == 1: exclude = 2
    #print(exclude)
    second = False
    for i in range(0,3):
      if i == randStartRow: continue
      if (type2 == 1):
        for j in range(0,3):
          if (j != exclude):
            shipArray[i][j] = True;
        break;
      else:
        if second:
          for j in range(0,3):
            if (j != exclude):
              shipArray[i][j] = True;
        else:
          second = True
    # repeat with second row
  else:
  # column
    shipArray[0][randStartCol] = True;
    shipArray[1][randStartCol] = True;
    shipArray[2][randStartCol] = True;
    type2 = randint(0,1)
    exclude = randint(0,2);
    if exclude == 1: exclude = 2
    #print(exclude)
    #excludelargerow = randint(0,2);
    second = False;
    for i in range(0,3):
      if (i == randStartCol): continue;
      if (type2>0.5): 
        for j in range(0,3):
          if (j != exclude):
            shipArray[j][i] = True;
            #print(i+" "+j);
        break;
      else:
        if (second):
          for j in range(0,3):
            if (j != exclude):
              shipArray[j][i] = True;
              #print(j+" "+i);
          break;
        else:
          second=True;
  
# for debug
"""
for i in range(size):
  for j in range(size):
    print(str(shipArray[i][j]) + " ", end = "");
  print();
"""



start = int(time.time())
"""
 * Check if the user hits all of the ships equal to the numberOfSquares
 * (which is the number of ships).
 * While the numberOfHits is not equal to numberOfSqaures,
 * then keep printing the user inputs of row and column
 """
rowInput = 0
columnInput = 0
while (numberOfHits != numberOfSquares):
  print();
  working = False
  while not working:
    err = False
    try:
      rowInput = int(input('Pick a row: '))
      columnInput = int(input("Pick a column: "))
    except ValueError:
      print('You may only enter integers. Please try again')
      err = True
      working = False
      continue
    # Checks if the user inputs are in bound from 0 to 9
    if (rowInput > size-1 or rowInput < 0 or columnInput > size-1 or columnInput < 0):
      print("Input not allowed in grid. Please try again");
      #rowInput = int(input('Pick a row: '))
      #columnInput = int(input("Pick a column: "))
      working = False
      continue
    working = True
  
  
  # Checks if the rowInput and columInput hit a ship on the shipArray grid and
  # not the gridLayout
  if (shipArray[rowInput][columnInput] and not (gridLayout[rowInput][columnInput] == HIT)):
    numberOfTry += 1;
    print("It's a hit!");
    # Increase numberOfHits everytime a ship is hit
    numberOfHits += 1;
    #print(numberOfHits);
    # Set the tile on the gridLayout to True(same spot where the ship is)
    gridLayout[rowInput][columnInput] = HIT;
    # pra new grid with all of the new information
    print('Your tries:')
    layout(gridLayout);
    # else statment that checks if you already have a hit on that spot
  elif (gridLayout[rowInput][columnInput] == HIT):
    print("You have already got a hit in this stop");
    print('Your tries:')
    layout(gridLayout);
    numberOfTry += 1;
  
  
  # if condition for missing
  if (not shipArray[rowInput][columnInput]):
    print("It's a miss!");
    gridLayout[rowInput][columnInput] = MISS;
    print('Your tries:')
    layout(gridLayout);
    # Always increase numberOfTry everytime you miss
    numberOfTry += 1;
    #hits[rowInput][columnInput] = 1;
    miss[rowInput][columnInput] = True;
  
  #print(start)
  # check if we won (Hint: this is the final part of the program)
  if (numberOfHits == numberOfSquares):
    end = int(time.time())
    """print(numberOfHits);
    print(numberOfTry);"""
    #print(numberOfHits/numberOfTry);
    #print(end)
    print("Congratulations! \nYour hit percentage was: " + str(round((numberOfHits/numberOfTry) * 100)) + "%! \nThe total guesses you took were: " + str(numberOfTry) + "!\nYour overall time was: " + str(math.floor(round(end - start)/(60))) + " minutes and " + str(round((end-start) % 60)) + " seconds!");
    # breaks the loops
    break;
  # time for ai to play
  move = guess(size);
  previous = aiHistory[move[0]][move[1]]
  if yourShips[move[0]][move[1]]:
    if previous == 1:
      print('The AI hit ' + str(move) + ' again')
    else:
      print('The AI hit ' + str(move) + '!')
      aiHistory[move[0]][move[1]] = 1
      # add possible good guesses to guessqueue
      possible = [
        (move[0]+1,move[1]),
        (move[0]-1,move[1]),
        (move[0],move[1]+1),
        (move[0],move[1]-1)
      ]
      for guess1 in possible:
        if workingcoord(size,guess1) and aiHistory[guess1[0]][guess1[1]] == 0:
          guessqueue.append(guess1)
      aihits += 1
  else:
    print('The AI fired at ' + str(move) + ' and missed!')
    aiHistory[move[0]][move[1]] = 2
  print("The AI's Tries: ")
  layout(aiHistory)
  if aihits == numberOfSquares:
    print('The AI won!')
    print('Your Stats:')
    end = int(time.time())
    print("Your hit percentage was: " + str(round((numberOfHits/numberOfTry) * 100)) + "% \nThe total guesses you took were: " + str(numberOfTry) + "\nYour overall time was: " + str(math.floor(round(end - start)/(60))) + " minutes and " + str(round((end-start) % 60)) + " seconds")
    break;
f.close()
