#pylint:disable=W0612
import math
import time
import timeit
import os
import random
import logging
from PIL import Image

RADIAN = math.pi / 180

def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 10, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + u'\u2591' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
       
        
def mapFunc(value, start1, stop1, start2, stop2): #Maps a value from a range ont a nother value from a different range
    return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))


def rotatePoint(p1, p2, a, r=False, y=False):
    if a == 0: return p2
    
    a = a % 359
    x1, y1, z1 = p1
    x2, y2, z2 = p2

    d12 = math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1) + (z2 - z1) * (z2 - z1))

    aP1P2 = math.atan2(z2 - z1, x2 - x1)  # In radians, not degrees
    aP1P3 = aP1P2 - math.radians(a)

    x3 = x1 + d12 * math.cos(aP1P3)
    if not y: y = y2 # same as P1 an P2
    z3 = z1 + d12 * math.sin(aP1P3)
    
    if r:
        x3 = round(x3,r)
        y = round(y,r)
        z3 = round(z3,r)
    
    p3 = (x3, y, z3)
    
    return p3





#print(a1,a2,a3)

#print(getRotationMatrix(a1, a2, a3))
                
   
    
    
def rotatePoint2(p1, p2, a):
    if a == 0: return p2
    
    a = a//2
    
    y1, x1, z1 = p1
    y2, x2, z2 = p2

    d12 = math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1) + (z2 - z1) * (z2 - z1))

    aP1P2 = math.atan2(z2 - z1, x2 - x1)  # In radians, not degrees
    aP1P3 = aP1P2 - math.radians(a)

    y3 = x1 - d12 * math.cos(aP1P3)
    x3 = y2
    z3 = z1 - d12 * math.sin(aP1P3)
    
    p3 = (x3, y3, z3)
    
    return p3



def rotatePoints(p2, points, ax):
    if not ax: return points
    return [rotatePoint(p2, p, ax) for p in points]

def rotatePoints2(p2, points, ay):
    if not ay: return points
    return [rotatePoint2(p2, p, ay) for p in points]

    
def breakUpArray(arr, intv, item="\n"):
    return [el for y in [[el, item] if idx % intv == 2 else el for idx, el in enumerate(arr)] for el in y]
    
def roundPoint(p, r=0):
    return tuple([int(round(x,r)) for x in p])

def roundPoints(points, r=0):
    nPoints = []
    for p in points:
        nPoints.append(roundPoint(p,r))
    return nPoints
    
def changePoint(xyz,x=0,y=0,z=0):
    xo, yo, zo = xyz
    return (xo + x, yo + y, zo + z)

def randomColor():
    r = random.randint(0,255)
    return (r,r,r)
    
def sleep(a=0.1):
    time.sleep(a)

def getDist(p1, p2): #Calculate distance between 2 points (eg: getDist((100,100,100),(140,150,129)))
    x1,y1,z1 = p1
    x2,y2,z2 = p2
    return math.sqrt(pow(x2-x1,2)+pow(y2-y1,2)+pow(z2-z1,2))

def flattenList(arr, rounds=1): #Flattens list round times
    for _ in range(rounds):
        arr = sum(arr, [])
    return arr

def flattenList2(l):
    nL = []
    for el in l:
        if type(el) == list:
            #print(el)
            nL = nL + flattenList2(el)
        else:
            nL = nL + [el]
    
    return nL


def clearScreen():
        try:
            os.system('cls')
        except:
            os.system('clear')
        finally:
            logging.warning("Failed to clear screen!")


def replaceInCoord(xyz,x=False,y=False,z=False):
    xo,yo,zo = xyz
    if x:
        xo = x
    if y:
        yo = y
    if z:
        zo = z
    return (xo, yo, zo)

calcDist = getDist

def lift(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]
  
    
def calcModelMidpoint(triangles):
    p = []
    for triangle in triangles:
        p.append(calcMidpoint(triangle))
            
    return calcMidpoint(p)

def calcMidpoint(points):
    l = len(points)
    #print("length",l)
    assert l != 0
    xyz = 0,0,0
    for p in points:
        x,y,z = addPoints(p,xyz)
        
    return (x/l,y/l,z/l)
    
    
def addPoints(*args):
    x,y,z = 0,0,0
    for p in args:
        x += p[0]
        y += p[1]
        z += p[2]
    return (x,y,z)
  
      
def getRotationPointY(mp, p):
    return (mp[0],p[1],mp[2])  

def getRotationPointX(mp, p):
    return (p[0], mp[1], mp[2])
    
#print(rotatePoint2(getRotationPointX((0,0,0),(0,0,100)),(0,0,100),45))    
    
def turnIntoTriangles(poly):
    
    triangles = []
    
    while len(poly) > 3:
        triangles.append([poly[0], poly.pop(1),poly[2]])
        
    triangles.append(poly)
    
    return triangles