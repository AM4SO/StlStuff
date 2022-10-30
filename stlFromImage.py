### using the greyscale of an image as a hight map, create a 3d model. 
import cv2
import numpy as np
import sys
import os
from argparse import ArgumentParser
from pyStl import Solid, Triangle, Vector

actualWidth = 60
INVERSE_COLOR = False
maxHeightAboveBase = 10
minThickness = 0.5

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filePath", help="image file to load")
parser.add_argument("-m", "--minThickness", dest="minThickness", help="base level thickness of STL in mm")
parser.add_argument("-M", "--maxThickness", dest="maxThickness", help="Amount in mm the largest color is above the base level")
parser.add_argument("-I", "--inverseColor", dest="reverseColor", help="'True' if lighter colors should be lower")

args = parser.parse_args()
filePath = "test.png"
if args.filePath and os.path.exists(args.filePath):
    filePath = args.filePath
if args.minThickness:
    minThickness = float(args.minThickness)
if args.maxThickness:
    maxHeightAboveBase = float(args.maxThickness)
if args.reverseColor and args.reverseColor.lower() == "true":
    INVERSE_COLOR = True

outputPath = filePath

img = cv2.imread(filePath)
grayscaleImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgShape = grayscaleImg.shape
if INVERSE_COLOR:
    grayscaleImg = np.ones(imgShape) * 255 - grayscaleImg
minVal = np.min(grayscaleImg)
grayscaleImg = grayscaleImg - np.ones(imgShape)*(minVal+0.01)
grayscaleImg = grayscaleImg * (maxHeightAboveBase / 255)    ## put image in range of 0 to maxHeightAboveBase

width = imgShape[0]
length = imgShape[1]

grayscaleImg += np.ones(imgShape) * minThickness

solid = Solid(outputPath)

for x in range(width-1):
    if x%100 == 0:
        print(str(x*(length-1)) + " / " + str((width-1)*(length-1)))
    xCoord = Vector.right * x
    for y in range(length-1):
        yCoord = Vector.back * y
        for height in (0,):
            z = Vector.up*height
            normal = Vector.zero-Vector.up
            reverse = False
            if height == minThickness:
                normal = Vector.up#normal
                reverse = True
            solid.addTriangle(normal, xCoord+yCoord+z, z+yCoord+Vector.back+xCoord, z+xCoord+Vector.right+yCoord, reverse)
            solid.addTriangle(normal, z+xCoord+yCoord+Vector.back, z+xCoord+yCoord+Vector.right,z+ Vector.right*(x+1) + Vector.back*(y+1), not reverse)
        if x!=0:
            continue
        otherEnd = Vector.right * (width-1)
        solid.addTriangle(-Vector.right, yCoord, yCoord + Vector.back, yCoord + Vector.up*minThickness, True)
        solid.addTriangle(-Vector.right, yCoord+Vector.back, yCoord+Vector.up*minThickness, yCoord+Vector.back+Vector.up*minThickness, not True)
        solid.addTriangle(Vector.right, yCoord + otherEnd, otherEnd + yCoord + Vector.back, otherEnd+ yCoord + Vector.up*minThickness, not True)
        solid.addTriangle(Vector.right, yCoord+Vector.back + otherEnd, otherEnd + yCoord+Vector.up*minThickness, otherEnd + yCoord+Vector.back+Vector.up*minThickness, True)
            
    solid.addTriangle(Vector.zero-Vector.back, xCoord, xCoord+Vector.right, xCoord+Vector.up*minThickness)
    solid.addTriangle(Vector.zero-Vector.back, xCoord+Vector.right, xCoord + Vector.up*minThickness, xCoord+Vector.right + Vector.up*minThickness, True)
    otherEnd = Vector.back * (length-1)
    solid.addTriangle(Vector.back, xCoord + otherEnd, otherEnd + xCoord+Vector.right, otherEnd + xCoord+Vector.up*minThickness, True)
    solid.addTriangle(Vector.back, otherEnd+xCoord+Vector.right, otherEnd+xCoord + Vector.up*minThickness, otherEnd + xCoord+Vector.right + Vector.up*minThickness, False)

for x in range(width-1):
    if x %100 == 0:
        print(str(round(x*100/(width-1))) + "%")
    for y in range(length-1):
        height = grayscaleImg[x,y]
        thisVert = Vector(x,y, height)
        l = Vector(x+1, y, grayscaleImg[x+1,y])
        b = Vector(x, y+1, grayscaleImg[x,y+1])
        bl = Vector(x+1, y+1, grayscaleImg[x+1,y+1])
        thisToL, thisToB = l - thisVert, b - thisVert
        normal = Vector.zero
        solid.addTriangle(normal, thisVert, l, b)
        solid.addTriangle(normal, l, b, bl, True)
        if x == 0 or x==width-2:## add triangles from walls. If x == 0, we are against the left wall
            t = 0 * (x==0) + 1*(x==width-2)
            normal = Vector.right
            bottom = Vector(x,y, minThickness)
            bottomRight = Vector(x,y+1, minThickness)
            topRight = Vector(x,y+1, grayscaleImg[x+t,y+1])# add 1 to x to make sure looking at the outermost one for height
            this = Vector(x,y, grayscaleImg[x+t, y])
            if x == width-2:
                bottom += Vector.right
                bottomRight += Vector.right
                topRight += Vector.right
                this += Vector.right
            solid.addTriangle(normal, bottom, bottomRight, this, x!=(width-2))
            solid.addTriangle(normal, bottomRight, this, topRight, x==(width-2))
        if y == 0 or y==length-2:
            t = 0 * (y==0) + 1*(y==length-2)
            normal = Vector.back
            bottom = Vector(x,y, minThickness)
            bottomBack = Vector(x+1,y, minThickness)
            topBack = Vector(x+1,y, grayscaleImg[x+1,y+t])
            this = Vector(x,y, grayscaleImg[x, y+t])
            if y == length-2:
                bottom += Vector.back
                bottomBack += Vector.back
                topBack += Vector.back
                this += Vector.back
            solid.addTriangle(normal, bottom, bottomBack, this, (y!=0))
            solid.addTriangle(normal, bottomBack, this, topBack, (y==0))


#solid.scalex(actualWidth / width)
#solid.scaley(actualWidth / width)
solid.save()
