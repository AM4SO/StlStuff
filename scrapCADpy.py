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
