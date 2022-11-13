from pyStl import Vector, Solid, Triangle

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

class Blueprint:
    def __init__(self, blueprint):
        self.rawBlueprint = blueprint
        self.simplifyRawBlueprint()
        self.calcSize()
        self.blockArray = []
        for i in range(self.size[0]):
            self.blockArray.append([])
            for j in range(self.size[1]):
                self.blockArray[i].append([])
                for k in range(self.size[2]):
                    self.blockArray[i][j].append("")
        print("Initialised blueprint thingy")
    def calcSize(self):
        blueprint = self.blueprintObj
        maxPos = Vector(-1000000000, -1000000000, -1000000000)
        minPos = Vector(1000000000, 1000000000, 1000000000)
        for part in self.blueprintObj:
            minPos = minPos.minPerAxis(part["pos"])
            if part["bounds"]:
                maxPos = maxPos.maxPerAxis(part["pos"]+part["bounds"])# Only tells us number of blocks in each direction
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
                if part["bounds"]:
                    part["bounds"] = Vector(part["bounds"]["x"], part["bounds"]["y"], part["bounds"]["z"])
                self.blueprintObj.append(part)

m='''
Each block is a node in a graph. --- No. Graphs will be slow when finding the correct location
for a block.
------
Calculate the dimentions of a 3d bounding box that is large enough to fit the whole object
in it. This is a 3d array which holds the blocks in it. Blocks which are larger than 1x1
can have the center of the block stored in the correct location, and the rest of the block
not need to be stored.
'''
x={"bodies":[{"childs":[{"bounds":{"x":4,"y":1,"z":4},"color":"9B683A","pos":{"x":-7,"y":8,"z":2},"shapeId":"df953d9c-234f-4ac2-af5e-f0490b223e71","xaxis":1,"zaxis":3},{"bounds":{"x":1,"y":3,"z":1},"color":"9B683A","pos":{"x":-5,"y":5,"z":3},"shapeId":"df953d9c-234f-4ac2-af5e-f0490b223e71","xaxis":1,"zaxis":3}]}],"version":4}
x = Blueprint(x)
