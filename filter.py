import os
import json
from natsort import natsorted

def updateJsonFile(filename):
    
    jsonFile = open(filename, "r+") # Open the JSON file for reading
    
    data = json.load(jsonFile) # Read the JSON into the buffer
    jsonFile.close() # Close the JSON file
    
    i=0
    for item in data["items"]:
        if item["status"] == "FAILED":
            data["items"].pop(i)
        i+=1

    jsonFile = open(filename, "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()

updateJsonFile("trans.json")
   




    
