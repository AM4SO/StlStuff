import os
import json

dirs = os.listdir("Blueprints")

unnamed=0
for path in dirs:
    if "steam_autocloud.vdf" in path:
        continue
    jsonFile = open("Blueprints/"+path + "/description.json", "r")
    jsonObj = json.loads(jsonFile.read())
    jsonFile.close()
    name = jsonObj["name"]
    if name == "":
        name = "unnamed " + str(unnamed)
        unnamed+=1
    os.rename("Blueprints/"+path, "Blueprints/"+name)

