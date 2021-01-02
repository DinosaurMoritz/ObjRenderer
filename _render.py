import os
import time 
import math
import logging
import random
import time
import numpy as np
from _resources import *
from _ObjLoader import ObjLoader

class Field:
    def __init__(self, _width, _height, _depth, _background=(-1,-1,-1), _pixel=(255,255,255), _colorGradiant=True):        
        print("Initiating the field!")
       
        self.width = _width
        self.height = _height
        self.depth = _depth
        self.background = _background
        self.pixel = _pixel
        self.colorGradiant = _colorGradiant
      
        t = time.time()
        self.field = [[[self.background for z in range(self.depth)] for y in range(self.height)] for x in range(self.width)] #Create 3d-(actually 4d)-list as coordinate-system
        print("It took ",time.time()-t,"s to create field!")
        
        self.drawnPixels = []
    
    
    def clearField(self):
        self.field = [[[self.background for z in range(self.depth)] for y in range(self.height)] for x in range(self.width)] #Clears the field

    def clear(self):
        clearScreen()
        self.clearField()
        
    def lookupColor(self, p):
        try:
            x,y,z = p
            return self.field[x][y][z]
        except:
            return (0,0,0)
    
    def drawPixel(self, xyz, shade=False): #Draws self.pixel into self.filed at point xyz
        try:
            y, x, z = xyz
            x = round(x)
            y = round(y)
            z = round(z)

            self.drawnPixels.append((xyz, shade, len(self.drawnPixels)))
       
            if shade == False:
                self.field[x][y][z] = self.pixel
            else:
                #s1,s2,s3 = shade
                #shade = (max(s1,0),max(s2,0),max(s3,0))
                
                self.field[x][y][z] = shade
                
        except Exception as e:
                    logging.error((e, xyz), exc_info=True)

    def drawLine(self, p1, p2, draw=True, shade=False): #Bresenham's line drawing algorithm. If not draw the points are returned but not drawn into self.field
       
        p1 = roundPoint(p1)
        p2 = roundPoint(p2)
        
        x1,y1,z1 = p1
        x2,y2,z2 = p2
        ListOfPoints = [] 
        ListOfPoints.append((x1, y1, z1)) 
        dx = abs(x2 - x1) 
        dy = abs(y2 - y1) 
        dz = abs(z2 - z1) 
        if (x2 > x1): 
            xs = 1
        else: 
            xs = -1
        if (y2 > y1): 
            ys = 1
        else: 
            ys = -1
        if (z2 > z1): 
            zs = 1
        else: 
            zs = -1
      
        #X
        if (dx >= dy and dx >= dz):         
            p1 = 2 * dy - dx 
            p2 = 2 * dz - dx 
            while (x1 != x2): 
                x1 += xs 
                if (p1 >= 0): 
                    y1 += ys 
                    p1 -= 2 * dx 
                if (p2 >= 0): 
                    z1 += zs 
                    p2 -= 2 * dx 
                p1 += 2 * dy 
                p2 += 2 * dz 
                ListOfPoints.append((x1, y1, z1)) 
      
        #Y-axis
        elif (dy >= dx and dy >= dz):        
            p1 = 2 * dx - dy 
            p2 = 2 * dz - dy 
            while (y1 != y2): 
                y1 += ys 
                if (p1 >= 0): 
                    x1 += xs 
                    p1 -= 2 * dy 
                if (p2 >= 0): 
                    z1 += zs 
                    p2 -= 2 * dy 
                p1 += 2 * dx 
                p2 += 2 * dz 
                ListOfPoints.append((x1, y1, z1)) 
      
        #Z" 
        else:         
            p1 = 2 * dy - dz 
            p2 = 2 * dx - dz 
            while (z1 != z2): 
                z1 += zs 
                if (p1 >= 0): 
                    y1 += ys 
                    p1 -= 2 * dz 
                if (p2 >= 0): 
                    x1 += xs 
                    p2 -= 2 * dz 
                p1 += 2 * dy 
                p2 += 2 * dx 
                ListOfPoints.append((x1, y1, z1))

        if draw:
            for c in ListOfPoints:
                self.drawPixel(c, shade=shade)
            
        return ListOfPoints


    def drawTriangle(self, p1p2p3, shade=False, draw=True, fill=False):
        p1, p2, p3 = p1p2p3
        
        p1p2 = self.drawLine(p1,p2,draw, shade)
        p2p3 = self.drawLine(p2,p3,draw, shade)
        p3p1 = self.drawLine(p3,p1,draw, shade)

        if fill:
            for p in p1p2:
                self.drawLine(p3,p)
            for p in p2p3:
                self.drawLine(p1,p)
            for p in p3p1:
                self.drawLine(p2,p)
                
        return [p1p2,p2p3,p3p1]
    
    def drawModel(self, name, ax=0, ay=0, factor=1):
        obj = ObjLoader(name, factor)
        print("drawing polygons!")
       
        
        polys = obj.polys
        # print(obj.polys)
        
        
        mp = calcModelMidpoint(polys)
        print("Model midpoint:",roundPoint(mp))
        
        #x,_,z = mp
        
        lenpols = len(polys)
        for npol in range(lenpols):
            #print("a")
            printProgressBar(npol+1,lenpols, prefix="drawing model")
            
            poly = polys[npol]
            
            poly = [rotatePoint(getRotationPointY(mp,p), p, ax) for p in poly]
            poly = [rotatePoint2(getRotationPointX(mp,p), p, ay) for p in poly]
            l = len(poly)
            if l == 3:
                self.drawTriangle(poly, fill=True)
                #print("triangle")
            else:
                triangles = turnIntoTriangles(poly)
                for triangle in triangles:
                    self.drawTriangle(triangle, fill=True)
               
        print(" ",end="\r")       

    

