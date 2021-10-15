import turtle
from math import *
from beamDictKeys import *

oneGrpUnt=35 # one graph unit is equal to 35 px

def drawGraph(clr='black'):
  ''' Draws the graph axes and initialises turtles. Use this before using drawFun, or you'll get an error '''

  global wn, mango, banana, alpha, nala

  wn=turtle.Screen()
  wn.screensize(750,750)

  mango=turtle.Turtle() #turtle named mango. He draws the function
  mango.hideturtle()
  mango.speed(0)

  banana=turtle.Turtle() #turtle named banana. He draws the axes
  banana.hideturtle()
  banana.speed(0)

  alpha=turtle.Turtle() #turtle named alpha. He labels the graph
  alpha.hideturtle()
  alpha.speed(0)
  
  nala=turtle.Turtle() #turtle named nala. She draws supports
  nala.hideturtle()
  nala.pensize(3)
  nala.color('#a5a5a5')
  nala.speed(0)
  
  turtle.tracer(0, 0)
  
  banana.color(clr)

  banana.goto(0,-oneGrpUnt*10)
  for i in range(21):
    banana.forward(10)
    banana.forward(-10)
    banana.left(90)
    banana.forward(oneGrpUnt)
    banana.right(90)

  banana.goto(0,0)
  banana.goto(-oneGrpUnt*10,0)
  banana.right(90)

  for i in range(21):
    banana.forward(10)
    banana.forward(-10)
    banana.left(90)
    banana.forward(oneGrpUnt)
    banana.right(90)
  
  banana.goto(0,0)

  banana.left(90)

  turtle.update()

def drawFun(fun_y, x_str, x_fin, oneXUnt=1, oneYUnt=1, clr='black', autoScaleX=False, autoScaleY=False, retScl=False):
  ''' Draws graph of input function in specified range. Also accepts scaling '''
  
  if autoScaleX:
    maxLim = max([-x_str,x_fin])
    oneXUnt = scl(maxLim)
  
  if autoScaleY:
    oneYUnt = scl(funMaxLim(fun_y, x_str, x_fin))
  
  x = x_str
  
  mango.color(clr)

  dx = (x_fin - x_str)/1000
  
  mango.up()
  mango.goto(x*oneGrpUnt/oneXUnt,fun_y(x)*oneGrpUnt/oneYUnt)
  mango.down()
  
  while x+dx < x_fin:
  
    dy = ( fun_y(x+dx) )-( fun_y(x) )
    
    #slope of scaled graph at point x (doesnt represent actual slope of function except if the x and y graph units are equal)
    dy_scaled = dy * oneGrpUnt / oneYUnt
    dx_scaled = dx*oneGrpUnt/oneXUnt
    slp = dy_scaled / dx_scaled
    
    # distance in pixels to be traveled by mango in an iteration
    dD = sqrt(dx_scaled**2 + dy_scaled**2)
    #angle at which to move
    theta = degrees(atan(slp))
    
    mango.left(theta)
    mango.forward(dD)
    mango.right(theta)
    
    x+=dx

  mango.up()
  mango.goto(0,0)
  mango.down()
  
  turtle.update()
  
  if retScl:
    return (oneXUnt, oneYUnt)

def svGraph(fLoc):
  ''' Saves graph at 'fLoc' location '''
  mango.getscreen().getcanvas().postscript(file=fLoc)

def labelGraph(string,loc,clr='black'):
  ''' Adds labels to graph, (eg. scale) '''
  alpha.color(clr)
  alpha.up()
  alpha.goto(*loc)
  alpha.down()
  style = ('Courier', 10, 'italic')
  alpha.write(string, font=style, align='center')
  alpha.up()
  alpha.goto(0,0)
  alpha.down()
  turtle.update()
  
def funMaxLim(in_fun,lLim,uLim):
  ''' Finds the absolute maximium of a function, useful for determining scale '''
  dx = (uLim - lLim)/1000
  x=lLim
  mx=in_fun(lLim)
  mn=in_fun(lLim)
  for _ in range(int((uLim-lLim)/dx)):
    fn_val=in_fun(x)
    if fn_val>mx:
      mx=fn_val
    if fn_val<mn:
      mn=fn_val
    x+=dx
  if mn<0:
    mn=mn*-1
  if mx>=mn:
    mxLm=mx
  else:
    mxLm=mn
  return mxLm

def scl(mxLm):
  ''' Judges suitable scale based on absolute maximium given as input '''
  if mxLm>1:
    mxLm=int(mxLm//1+1) #rounds off mxLm to next highest integer
    dig=len(str(mxLm))  #finds no. of digits in mxLm

    if dig>1:
      mxLm=mxLm//(10**(dig-1))+1 #finds the most significant digit and rounds off to next highest integer

    if mxLm<=2:
      retscl=2/10*10**(dig-1)
    elif mxLm>=3 and mxLm<=5:
      retscl=5/10*10**(dig-1)
    else:
      retscl=10/10*10**(dig-1)

  else:

    for i in range(99999999999):
      if mxLm//1>=1:
        mxLm=int(mxLm//1+1)
        pw=-i
        break
      mxLm=mxLm*10

    if mxLm<=2:
      retscl=2/10*10**pw
    elif mxLm>=3 and mxLm<=5:
      retscl=5/10*10**pw
    else:
      retscl=10/10*10**pw

  return retscl

def drawSup(x, oneXUnt):
  ''' Developed for my beam analysis proogram '''

  nala.up()
  nala.goto(x*oneGrpUnt/oneXUnt,0)
  nala.down()
  
  nala.right(90)
  nala.forward(25)
  nala.up()
  nala.left(180)
  nala.forward(25)
  nala.right(90)
  nala.down()
  
  nala.left(225)
  nala.forward(7)
  nala.up()
  nala.left(180)
  nala.forward(7)
  nala.right(45)
  nala.down()
  
  nala.right(45)
  nala.forward(7)
  nala.up()
  nala.left(180)
  nala.forward(7)
  nala.right(135)
  nala.goto(0,0)
  
  nala.down()
  
  turtle.update()
  

def drawSups(spans,oneXUnt):
  ''' Developed for my beam analysis proogram '''
  drawSup(spans[0][spanEnds][0], oneXUnt)
  for span in spans:
    drawSup(span[spanEnds][1], oneXUnt)
    