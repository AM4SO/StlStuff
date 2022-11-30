from pyStl import Vector, Solid, Triangle
from argparse import ArgumentParser
import os
import json

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filePath", help="scrap mechanic model JSON file")
parser.add_argument("-n", "--name", dest="modelName", help="Name of model (will be used in when saving the generated STL)")
args = parser.parse_args()
path = ""
modelName = "testThing"

if args.filePath and os.path.exists(args.filePath):
    path = args.filePath
if args.modelName:
    modelName = args.modelName

rludbf = (Vector.right, -Vector.right, Vector.up, -Vector.up, Vector.back, -Vector.back)

class Face:
    def __init__(self, normal, bl, br, tr, tl, blockPos=None):
        self.triangles = []
        self.normal = normal
        if blockPos:
            rightVec, upVec = None, None
            x = normal.positive()
            if x == Vector.right:
                rightVec = Vector.back
                upVec = Vector.up
            elif x == Vector.up:
                rightVec = Vector.right
                upVec = Vector.back
            elif x == Vector.back:
                rightVec = Vector.right
                upVec = Vector.up
            bl = -rightVec*0.5 -upVec*0.5
            br = bl+rightVec
            tl = bl+upVec
            tr = tl+rightVec
        rev = normal != Vector.right and normal != Vector.up and normal != Vector.back
        self.triangles.append(Triangle(bl,br,tl, rev))
        self.triangles.append(Triangle(tl, br, tr, rev))

class Block:
    left, right, back, front, top, bottom = None, None, None, None, None, None
    def __init__(self, position):
        self.position = position
        
        left = Face(-Vector.right, blockPos=position)

def print3d(arr):
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            print(arr[i][j])
        print("")

class Blueprint:
    blueprintObj = None
    solid, name = None, None
    def __init__(self, blueprint, name):
        self.rawBlueprint = blueprint
        self.name = name
        self.simplifyRawBlueprint()
        self.calcSize()
        self.blockArray = []
        for i in range(self.size[0]):
            self.blockArray.append([])
            for j in range(self.size[1]):
                self.blockArray[i].append([])
                for k in range(self.size[2]):
                    self.blockArray[i][j].append("0")
        print("Initialised blueprint thingy")
        for part in self.blueprintObj:
            position = part["pos"] - self.minPos
             bounds = Vector(1,1,1)
            if part.get("bounds"):
                bounds = part["bounds"]
            else: ## Correct orientation: xaxis: 2, zaxis:1
                xaxis = part["xaxis"]
                zaxis = part["zaxis"]
                part["bounds"] = Vector(1,1,1) # Assume cube for now
                #translate = Vector.zero -- No translate: Use rotate
                part["bounds"] = part["bounds"].rotatex(xaxis - 2).rotatez(zaxis - 1)
                #if not (xaxis == 2 and zaxis == 1):
                    
            endPos = position + bounds - Vector.ones
                position += translate
            for x in range(bounds.x):
                for y in range(bounds.y):
                    for z in range(bounds.z):
                        self.blockArray[position.x+x][position.y+y][position.z+z] = "1"#part["shapeId"]
        print3d(self.blockArray)
        self.createModel()
        self.solid.save()
    
    def createModel(self):
        self.solid = Solid(self.name)
        blockArray = self.blockArray
        for x in range(len(blockArray)):
            for y in range(len(blockArray[x])):
                for z in range(len(blockArray[x][y])):
                    block = blockArray[x][y][z]
                    if block == "0":
                        continue
                    l = x==0 or blockArray[x-1][y][z] == "0"
                    r = x==len(blockArray)-1 or blockArray[x+1][y][z] == "0"
                    d = z==0 or blockArray[x][y][z-1] == "0"
                    u = z==len(blockArray[x][y])-1 or blockArray[x][y][z+1] == "0"
                    f = y==0 or blockArray[x][y-1][z] == "0"
                    b = y==len(blockArray[x])-1 or blockArray[x][y+1][z] == "0"
                    self.solid.createCube(Vector(x,y,z),1, includelrdufb=(l,r,d,u,f,b))
        
    def calcSize(self):
        blueprint = self.blueprintObj
        maxPos = Vector(-1000000000, -1000000000, -1000000000)
        minPos = Vector(1000000000, 1000000000, 1000000000)
        for part in self.blueprintObj:
            minPos = minPos.minPerAxis(part["pos"])
            bounds = Vector.ones
            if part.get("bounds"):
                bounds = part["bounds"]
            maxPos = maxPos.maxPerAxis(part["pos"]+bounds)# Only tells us number of blocks in each direction
        self.minPos = minPos
        self.maxPos = maxPos - Vector.ones ## -1 to get coords instead of blocks in each direction
        self.objBounds = maxPos - minPos ## tells us array size
        self.size = self.objBounds
    def simplifyRawBlueprint(self):
        blueprint = self.rawBlueprint
        ## Merge bodies into single array
        self.blueprintObj = []
        for body in blueprint["bodies"]:
            for part in body["childs"]:
                part["pos"] = Vector(part["pos"]["x"], part["pos"]["y"], part["pos"]["z"])
                if part.get("bounds"):
                    part["bounds"] = Vector(part["bounds"]["x"], part["bounds"]["y"], part["bounds"]["z"])
                self.blueprintObj.append(part)

m='''
------
Calculate the dimentions of a 3d bounding box that is large enough to fit the whole object
in it. This is a 3d array which holds the blocks in it. Blocks which are larger than 1x1
can have the center of the block stored in the correct location, and the rest of the block
not need to be stored.
'''
file = open(path)
x = file.read()
file.close()
x = json.loads(x)
#x={"bodies":[{"childs":[{"bounds":{"x":4,"y":1,"z":4},"color":"9B683A","pos":{"x":-7,"y":8,"z":2},"shapeId":"df953d9c-234f-4ac2-af5e-f0490b223e71","xaxis":1,"zaxis":3},{"bounds":{"x":1,"y":3,"z":1},"color":"9B683A","pos":{"x":-5,"y":5,"z":3},"shapeId":"df953d9c-234f-4ac2-af5e-f0490b223e71","xaxis":1,"zaxis":3}]}],"version":4}
x = Blueprint(x, modelName)
