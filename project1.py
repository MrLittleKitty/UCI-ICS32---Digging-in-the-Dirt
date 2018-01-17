from pathlib import *

def digInTheDirt() -> None:

    inputLine = None
    mode = None
    directoryPath = None
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
        break
    if mode == 'D':


def getAllPathsFromDirectory(directory : Path, recursive : bool, paths: [str] = []) -> [str]:
    for file in directory.iterdir():
        if recursive and file.is_dir():
            getAllPathsFromDirectory(file,recursive,paths)
        paths.append(file.abspath())

def error() -> None:
    print('ERROR')

if __name__ == '__main__':
    digInTheDirt()