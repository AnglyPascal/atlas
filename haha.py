import csv
import os

transfersArray = []
listOfFiles: list[str] = []
dirName: str = "./data"
for (dirpath, _, filenames) in os.walk(dirName):
    listOfFiles += [os.path.join(dirpath, file) for file in filenames]

    for file in listOfFiles:
        with open(file, encoding="utf-8") as file_name:
            reader = csv.reader(file_name, delimiter=',')
            reader.__next__()
            for row in reader: 
                transfersArray.append(row)

print(len(transfersArray))
