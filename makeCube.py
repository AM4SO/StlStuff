from pyStl import Solid, Triangle, Vector
import math

cube = Solid("cubeThing")

cube.addTriangle(Vector.up, Vector.zero,Vector.right*50,Vector.back*50, True)
cube.addTriangle(Vector.up, Vector.right*50, (Vector.right+Vector.back) * 50, Vector.back*50, True)
cube.addTriangle(Vector.up, Vector.up*50,(Vector.up + Vector.right)*50,(Vector.up+Vector.back)*50)
cube.addTriangle(Vector.up, (Vector.right+Vector.up)*50, (Vector.right+Vector.back+Vector.up) * 50, (Vector.back+Vector.up)*50)

cube.addTriangle(Vector.right, Vector.zero, Vector.up*50, Vector.back * 50)
cube.addTriangle(Vector.right, Vector.up*50, (Vector.back+Vector.up) * 50, Vector.back * 50)
cube.addTriangle(Vector.right, (Vector.right + Vector.up) * 50, (Vector.right + Vector.back + Vector.up) * 50, (Vector.right + Vector.back)*50, True)
cube.addTriangle(Vector.right, Vector.right * 50, (Vector.right + Vector.up) * 50, (Vector.right + Vector.back) * 50, True)

cube.addTriangle(Vector.back, Vector.zero, Vector.up*50, Vector.right * 50, True)
cube.addTriangle(Vector.back, Vector.up*50, (Vector.right+Vector.up) * 50, Vector.right * 50, True)
cube.addTriangle(Vector.back, Vector.back * 50, (Vector.up + Vector.back) * 50, (Vector.right+Vector.back)*50)
cube.addTriangle(Vector.back, (Vector.up+Vector.back)*50, (Vector.right+Vector.up+Vector.back)*50, (Vector.right+Vector.back) * 50)
cube.saveAscii()
