from pathlib import *

def error() -> None:
    print('ERROR')

def printList(list: [any]) -> None:
    for value in list:
        print(str(value))

def getAllPathsFromDirectory(directory : Path, recursive : bool, paths: [str] = [], ) -> [Path]:
    directories = []
    for file in directory.iterdir():
        if file.is_dir():
            if recursive:
                directories.append(file)
        else:
            paths.append(file)
    if recursive:
        for file in directories:
            getAllPathsFromDirectory(file,recursive,paths)
    return paths

def filterFiles(mode : str, filter : str or int or None, files : [Path]) -> [Path]:
    if mode == 'A':
        return files
    filteredFiles = []
    for file in files:
        if mode == 'N' and file.stem == filter:
            filteredFiles.append(file)
        elif mode == 'E' and (file.suffix == filter or file.suffix[1:] == filter):
            filteredFiles.append(file)
        elif mode == 'T':
            fileContents = file.read_text()
            if filter in fileContents:
                filteredFiles.append(file)
                continue
        elif mode == '<' and file.stat().st_size < filter:
            filteredFiles.append(file)
        elif mode == '>' and file.stat().st_size > filter:
            filteredFiles.append(file)
    return filteredFiles


def readFirstLine() -> (str,Path):
    while True:
        inputLine = input()
        if len (inputLine) < 3:
            error()
            continue
        mode = inputLine[0:1]
        directoryPath = Path(inputLine[2:])
        if not directoryPath.is_dir() or (mode != 'D' and mode != 'R'):
            error()
            continue
        return (mode,directoryPath)

def readSecondLine() -> (str,any):
    while True:
        inputLine = input()
        mode = inputLine[0:1]
        if mode == 'A' and len(inputLine.strip()) == 1:
            return ('A',None)
        elif mode == 'N' or mode == 'E' or mode == 'T':
            if len(inputLine[2:]) > 0:
                return (mode,inputLine[2:])
        elif mode == '<' or mode =='>':
            if len(inputLine[2:]) > 0 and inputLine[2:].isdigit():
                return (mode,int(inputLine[2:]))
        error()
        continue

def digInTheDirt() -> None:

    mode,path = readFirstLine()
    paths = getAllPathsFromDirectory(path,mode == 'R')
    printList(paths)
    mode,value = readSecondLine()
    interestingFiles = filterFiles(mode,value,paths)
    if len(interestingFiles) != 0:
        printList(interestingFiles)


if __name__ == '__main__':
    digInTheDirt()