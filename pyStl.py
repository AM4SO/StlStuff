import math
import struct
class Solid:
    def __init__(self, name):
        self.name = name
        self.triangles = []
        self.numTriangles = 0
    def saveAscii(self):
        output = ""
        output += "solid " + self.name
        for tri in self.triangles:
            output+= "\nfacet normal " + str(tri.normal)
            output += "\nouter loop"
            for vert in (tri.vert1, tri.vert2, tri.vert3):
                output += "\nvertex " + str(vert)
            output += "\nendloop\nendfacet"
        output += "\nendsolid " + self.name
        file = open(self.name + ".stl", "w+")
        file.write(output)
        file.close()
    def save(self):
        fileName = self.name + ".stl"
        self.saveAs(fileName)
    def saveAs(self, fileName):
        #file = open(fileName,"wb+")
        #out= b""
        #out += struct.pack("<80xi", self.numTriangles)
        #for tri in self.triangles:
        #    trianglesBin = tri.getNumericBinary()
        #    out += struct.pack("<12fh", *trianglesBin[:12], trianglesBin[12])
        #file.write(out)
        #file.close()
        #                              ^#Works^
        file = open(fileName, "wb+")
        file.write(bytes(0))
        file.close()
        with open(fileName, "ab+") as file:
            file.write(struct.pack("<80xi", self.numTriangles))
            for tri in self.triangles:
                trianglesBin = tri.getNumericBinary()
                file.write(struct.pack("<12fh", *trianglesBin[:12], trianglesBin[12]))
        ############                  ^Doesn't work^ --- Now works?!
        
    def addTriangle(self, normal, v1,v2,v3,reverse=False):
        self.triangles.append(Triangle(normal,v1,v2,v3,reverse))
        self.numTriangles+=1
    def removeTriangle(self, index=-1):
        self.triangles.pop(index)
        self.numTriangles -= 1
    def scalex(self, scale):
        for tri in self.triangles:
            tri.scalex(scale)
    def scaley(self, scale):
        for tri in self.triangles:
            tri.scaley(scale)
    def scalez(self, scale):
        for tri in self.triangles:
            tri.scalez(scale)
    def scale(self, scale):
        self.scalex(scale)
        self.scaley(scale)
        self.scalez(scale)
        return true

class Triangle:
    def __init__(self, normal, v1,v2,v3, reverse=False):
        self.normal = normal
        self.vert1 = v1
        self.vert2 = v2
        self.vert3 = v3
        if reverse:
            self.vert1, self.vert3 = self.vert3, self.vert1
        self.atb = 0
    def getNumericBinary(self):
        ret = []
        for vector in (self.normal.positive(),self.vert1, self.vert2, self.vert3):
            for v in vector:
                ret.append(v)
        ret.append(self.atb)
        return ret
    def __str__(self):
        ret = "normal: " + str(self.normal) + "\n"
        ret += "vertex0" + str(self.vert1) + "\n"
        ret += "vertex1" + str(self.vert2) + "\n"
        ret += "vertex2" + str(self.vert3) + "\n"
        #ret += "ATB: 0x0000"
        return ret
    def scalex(self, scale):
        for v in (self.vert1, self.vert2, self.vert3):
            v.x *= scale
    def scaley(self, scale):
        for v in (self.vert1, self.vert2, self.vert3):
            v.y *= scale
    def scalez(self, scale):
        for v in (self.vert1, self.vert2, self.vert3):
            v.z *= scale
class Vector:
    up,right,back,zero = None,None,None,None

    x,y,z = None,None,None
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def __add__(self, other):
        return Vector(self.x+other[0], self.y+other[1], self.z+other[2])
    def __iadd__(self, other):
        return self + other
    def __sub__(self, other):
        return Vector(self.x-other[0], self.y-other[1], self.z-other[2])
    def __isub__(self, other):
        return self + other
    def __mul__(self, scal):
        return Vector(self.x*scal, self.y*scal, self.z*scal)
    def __imul__(self, scal):
        return self.__mul__(scal)
    def __abs__(self):
        return (self.x**2+self.y**2+self.z**2)**0.5
    def __getitem__(self, index):
        return self.x * (index==0) + self.y*(index==1) + self.z * (index==2)
    def __str__(self):
        #return "("+str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"
        return str(self.x) + " " + str(self.y) + " " + str(self.z)
    def __iter__(self):
        return iter((self.x,self.y,self.z))
    def cross(self, other):
        x = self.y*other.z - self.z*other.y
        y = self.z*other.x - self.x*other.z
        z = self.x*other.y - self.y*other.x
        return Vector(x, y, z)
    def asUnit(self):
        return self * (1/abs(self))
    def positive(self):
        return Vector(abs(self.x),abs(self.y),abs(self.z))
    def __neg__(self):
        return Vector.zero - self
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    def maxPerAxis(self, other):
        return Vector(max(self.x, other.x), max(self.y,other.y), max(self.z, other.z))
    def minPerAxis(self, other):
        return Vector(min(self.x, other.x), min(self.y,other.y), min(self.z, other.z))
Vector.up = Vector(0,0,1)
Vector.right = Vector(1,0,0)
Vector.back = Vector(0,1,0)
Vector.zero = Vector(0,0,0)
Vector.ones = Vector(1,1,1)
