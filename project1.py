from pathlib import *

def error() -> None:
    print('ERROR')

def printList(list: [any]) -> None:
    for value in list:
        print(value)

def getAllPathsFromDirectory(directory : Path, recursive : bool, paths: [str] = [], ) -> [str]:
    directories = []
    for file in directory.iterdir():
        if file.is_dir():
            if recursive:
                directories.append(file)
        else:
            paths.append(str(file))
    if recursive:
        for file in directories:
            getAllPathsFromDirectory(file,recursive,paths)
    return paths

def readFirstLine() -> (str,Path):
    while True:
        inputLine = input()
        if len (inputLine) < 3:
            error()
            continue
        mode = inputLine[0:1]
        directoryPath = Path(inputLine[3:])
        if not directoryPath.is_dir() or (mode != 'D' and mode != 'R'):
            error()
            continue
        return (mode,directoryPath)

def readSecondLine() -> (str,any):
    while True:
        inputLine = input()
        mode = inputLine[0:1]
        if mode == 'A' and len(inputLine) == 1:
            return ('A',None)

def digInTheDirt() -> None:

    mode,path = readFirstLine()
    paths = getAllPathsFromDirectory(path,mode == 'R')
    printList(paths)
    mode,value = readSecondLine()

if __name__ == '__main__':
    digInTheDirt()