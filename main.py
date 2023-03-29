import pygame
import sqlite3
from PIL import Image
from os import remove
from random import choice, uniform
from sys import exit
from pygame.locals import QUIT
pygame.init()

con=sqlite3.connect("AIDatabase.db")
cur=con.cursor()


#cur.execute("CREATE TABLE Moves(amountMoved, changeInDirection, cornersTurned, branchesTurned)")#statement to create table delete old table and use this to reset ai progreess


#loop to allow it to run without needing to press start each time
#'ctrl' + '[' to un indent
while True:
  clock=pygame.time.Clock()
  #variable to hold how many move it took to solve maze
  moves=0
  cornerTurned=0
  branchesTurned=0
  #statement here to makes sure variable exist to be deleted
  changeDirection=0
  lastMove=0
  del lastMove
  del changeDirection
  #counter to prevent ai moving to fast
  counter=0
  robotMove=""
  screen=pygame.display.set_mode((400, 400))
  pygame.display.set_caption("maze")
  screen.fill("red")
  #starting postion of robotSurface, can be changed for more complicated mazes
  xAxis=190
  yAxis=190
  robotSurface=pygame.Surface((10,10))
  robotSurface.fill("blue")
  wallSurface=pygame.Surface((10,10))
  wallSurface.fill("white")
  endSurface=pygame.Surface((10,10))
  endSurface.fill("green")
  replacerSurface=pygame.Surface((10,10))
  replacerSurface.fill("red")
  
  
  
  def screenshot():
    end=""
    moveArray=[]
    pygame.image.save(screen, "maze.png")
    mazePic=Image.open("maze.png")
    mazePicLoaded=mazePic.load()
    colourUp=(mazePicLoaded[xAxis,yAxis-10])
    colourDown=(mazePicLoaded[xAxis,yAxis+10])
    colourLeft=(mazePicLoaded[xAxis-10,yAxis])
    colourRight=(mazePicLoaded[xAxis+10,yAxis])
    remove("maze.png")
    if colourUp==(255,0,0):
      moveArray.append("up")
    elif colourUp==(0,255,0):
      end="up"
    if colourDown==(255,0,0):
      moveArray.append("down")
    elif colourDown==(0,255,0):
      end="down"
    if colourLeft==(255,0,0):
      moveArray.append("left")
    elif colourLeft==(0,255,0):
      end="left"
    if colourRight==(255,0,0):
      moveArray.append("right")
    elif colourRight==(0,255,0):
      end="right"
    return moveArray, end
  
  
  
  def ai():
    try:
      movableSpaces=screenshot()
      res=cur.execute("SELECT amountMoved FROM Moves")
      total=0
      counter1=0
      counter2=-1
      moveArray=[]
      changeInDirectionArray=[]
      for i in res.fetchall():
        num=str(i)
        num=num.replace("(","")
        num=num.replace(")","")
        num=num.replace(",","")
        num=int(num)
        moveArray.append(num)
        total+=num
        counter1+=1
      meanMoves=total/counter1
      
      res=cur.execute("SELECT changeInDirection FROM Moves")
      counter1=0
      for i in res.fetchall():
        num=str(i)
        num=num.replace("(","")
        num=num.replace(")","")
        num=num.replace(",","")
        num=int(num)
        changeInDirectionArray.append(num)
        total+=num
        counter1+=1
      meanchangeInDirectionArray=total/counter1
  
      counter3=0
      counter4=0
      for i in moveArray:
        counter2+=1
        if i<meanMoves:
          if meanchangeInDirectionArray>=changeInDirectionArray[counter2]:
            counter3+=1
          elif meanchangeInDirectionArray<changeInDirectionArray[counter2]:
            counter4+=1

            
      total=counter3+counter4
      changeDirectionProability=counter4/total#currently probility becomes zero as no data that had change direction exist below the mean, though I don't think that is an issue
      changeDirectionProability=int(round(changeDirectionProability, 0))
      num=uniform(0,1)

      
      if num<=changeDirectionProability:
        if movableSpaces[1]=="":
          try:
            movableSpaces.remove(lastMove)
            return choice(movableSpaces[0])
          except:
            return choice(movableSpaces[0])
        else:
          return movableSpaces[1]
      else:
        try:
          for i in movableSpaces[0]:
            if i ==lastMove:
              return lastMove
          if movableSpaces[1]==lastMove:
            return lastMove
          return choice(movableSpaces[0])
        except:
          return choice(movableSpaces[0])
    except:
      if movableSpaces[1]=="":
        return choice(movableSpaces[0])
      else:
        return movableSpaces[1]
  
      
  '''
  for i in range(0,40):
    #if statement to add the end of maze
    if i*10!=190:
      screen.blit(wallSurface, (i*10,0))
    else:
      screen.blit(endSurface, (i*10,0))
  for i in range(0,40):
    screen.blit(wallSurface, (i*10,390))
  for i in range(0,40):
    screen.blit(wallSurface, (0,i*10))
  for i in range(0,40):
    screen.blit(wallSurface, (390,i*10))
  
  for i in range(0,40):
    screen.blit(wallSurface, (180,i*10))
  for i in range(0,40):
    screen.blit(wallSurface, (200,i*10))
  '''
  mazeArray=[   ['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w', 'w','w','e' ,'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'], ['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'], ['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','p', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w'],['w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w',            'w', 'w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w','w']]
  
  '''
make modifying array easier
['0','1','2','3','4','5','6','7','8','9','0','1','2','3','4','5','6','7','8','9',
'0','1','2','3','4','5','6','7','8','9','0','1','2','3','4','5','6','7','8','9']
  '''
  counter1=0
  for i in mazeArray:
    counter2=0
    for j in i:
      if j=='w':
        screen.blit(wallSurface,(counter2*10,counter1*10))
      elif j=='e':
        screen.blit(endSurface,(counter2*10,counter1*10))
      counter2+=1
    counter1+=1
  
  
  counter1=0
  for i in mazeArray:
    counter2=0
    for j in i:
      if j=='w':
        screen.blit(wallSurface,(counter2*10,counter1*10))
      elif j=='e':
        screen.blit(endSurface,(counter2*10,counter1*10))
      counter2+=1
    counter1+=1
  
    
  screen.blit(robotSurface, (xAxis,yAxis))
  pygame.display.update()
  
  
  
  while True:
    clock.tick(60)
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        exit() 
        
      #to allow for human testing of the controls(should no longer be needed)
      '''
      if event.type== pygame.KEYDOWN:
        key=pygame.key.get_pressed()
        if key[pygame.K_UP]:
          robotMove="up"
        elif key[pygame.K_DOWN]:
          robotMove="down"
        elif key[pygame.K_RIGHT]:
          robotMove="right"
        elif key[pygame.K_LEFT]:
          robotMove="left"
      '''
    if counter==0:
      robotMove=ai()
      counter=5
      try:
        if (robotMove=="up" or robotMove=="down") and (lastMove=="left" or lastMove=="right") and len(screenshot()[0])<=2:
          cornerTurned+=1
          lastMove=robotMove
        elif (robotMove=="left" or robotMove=="right") and (lastMove=="up" or lastMove=="down") and len(screenshot()[0])<=2:
          cornerTurned+=1
          lastMove=robotMove
        elif lastMove!=robotMove and len(screenshot()[0])<=2:
          changeDirection+=1
          lastMove=robotMove
        if len(screenshot()[0])>2 and ((robotMove=="left" or robotMove=="right") and (lastMove=="up" or lastMove=="down") or (robotMove=="up" or robotMove=="down") and (lastMove=="left" or lastMove=="right")):
          branchesTurned+=1
          lastMove=robotMove
      except:
        lastMove=robotMove
        changeDirection=0
      
      
    
    
    else:
      counter-=1
    
    if robotMove=="up":
      yAxis-=10
      screen.blit(replacerSurface,(xAxis, yAxis+10))
      screen.blit(robotSurface, (xAxis,yAxis))
      robotMove=""
      moves+=1
        
    elif robotMove=="down":
      yAxis+=10
      screen.blit(replacerSurface,(xAxis, yAxis-10))
      screen.blit(robotSurface, (xAxis,yAxis))
      robotMove=""
      moves+=1
      
    elif robotMove=="left":
      xAxis-=10
      screen.blit(replacerSurface,(xAxis+10, yAxis))
      screen.blit(robotSurface, (xAxis,yAxis))
      robotMove=""
      moves+=1
          
    elif robotMove=="right":
      xAxis+=10
      screen.blit(replacerSurface,(xAxis-10, yAxis))
      screen.blit(robotSurface, (xAxis,yAxis))
      robotMove=""
      moves+=1
     
    pygame.display.update()
    if xAxis==190 and yAxis==0:
      #print how many moves it took to solve maze
      #print('\n'*2+str(moves)+'\n'+str(changeDirection)+'\n'*2)
      pygame.quit()
      break
  
  
  cur.execute("INSERT INTO Moves(amountMoved, changeInDirection, cornersTurned, branchesTurned) VALUES("+str(moves)+","+str(changeDirection)+","+str(cornerTurned)+","+str(branchesTurned)+")")
  con.commit()
  
  '''
  SELECT...
  FROM...
  WHERE...
  '''
  res=cur.execute("SELECT * FROM Moves")
  print(res.fetchall())
  #res=cur.execute("SELECT amountMoved FROM Moves")
  #print(res.fetchall())
  #res=cur.execute("SELECT changeInDirection FROM Moves")
  #print(res.fetchall())