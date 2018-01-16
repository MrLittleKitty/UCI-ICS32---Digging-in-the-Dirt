def digInTheDirt() -> None:

    inputLine = None
    while (True):
        inputLine = input()
        if len (inputLine) < 3:
            error()
            continue
        firstArgument = inputLine[0:1]

def error() -> None:
    print('ERROR')

if __name__ == '__main__':
    digInTheDirt()