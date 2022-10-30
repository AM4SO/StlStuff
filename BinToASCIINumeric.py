import struct
file = open("test.png.stl", "rb")
cont = file.read()
file.close()

class Triangle:
    def __init__(self, byteList):
        self.normal = None
        self.vert1 = None
        self.vert2 = None
        self.vert3 = None
        thing = []
        #print(bytes(byteList[:48]))
        thing = struct.unpack("<12f", bytes(byteList[:48]))
        #for i in range(0,48,2):
        #    thing.append(hex(byteList[i]) + hex(byteList[i+1])[2:])
        self.normal = (thing[0],thing[1],thing[2])
        self.vert1 = (thing[3],thing[4],thing[5])
        self.vert2 = (thing[6],thing[7],thing[8])
        self.vert3 = (thing[9],thing[10],thing[11])
    def __str__(self):
        ret = "normal: " + str(self.normal) + "\n"
        ret += "vertex0" + str(self.vert1) + "\n"
        ret += "vertex1" + str(self.vert2) + "\n"
        ret += "vertex2" + str(self.vert3) + "\n"
        #ret += "ATB: 0x0000"
        return ret

def getTriangle(cont, triNum):
    byteList = []
    start = 80 + triNum * 50
    for i in range(50):
        byteList.append(cont[start+i])
    triangle = Triangle(byteList)
    return triangle

output = ""
for v in cont[0:80]:
    output+=str(v) + " "
print("header: ")
print(output)
for i in range(32):
    triangle = getTriangle(cont, i)
    print(triangle)



    
