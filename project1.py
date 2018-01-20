# Eric Wolfe. UCI ID#: 76946154. eawolfe@uci.edu
from pathlib import *


def error() -> None:
    """Prints the word ERROR to the standard output"""
    print('ERROR')


def print_list(list: [any]) -> None:
    """
    Prints every element from the given list to the standard output
    Each element is printed on its own line
    """
    for value in list:
        print(str(value))


def get_all_paths_from_directory(directory: Path, recursive: bool, paths: [str] = [], ) -> [Path]:
    """
    Gets a list of file paths for all files in the given directory (and its subdirectories if recursive is true)
    :param directory: The starting directory to get file paths from
    :param recursive: Whether files in subdirectories should be included
    :param paths: The list that file paths will be added to
    :return: A list of file paths from the given directory (and subdirectories if recursive is true)
    """
    directories = []
    for file in directory.iterdir():
        # If the file is a subdirectory and we are processing subdirectories, add it to the list for later processing
        if file.is_dir():
            if recursive:
                directories.append(file)
        else: # If the file is just a normal file then add it to the paths list
            paths.append(file)
    # If we are processing subdirectories then go through all the subdirectories and process them
    if recursive:
        for file in directories:
            get_all_paths_from_directory(file, recursive, paths)
    return paths


def filter_files(mode: str, filter: str or int or None, files: [Path]) -> [Path]:
    """
    Removes files from the given list according to the given mode and filter criteria
    :param mode: The mode that will be used to filter the files ('A', 'N', 'E', 'T', '<', '>')
    :param filter: the filter criteria that the files will be evaluated against
    :param files: The list of files to be filtered
    :return: A list of files that passed the filter according to the given mode and filter criteria
    """
    # If the mode is 'A' then all files pass the filter so we just return the given list of files
    if mode == 'A':
        return files
    filteredFiles = []
    for file in files:
        # 'N' means the files name must match the filter
        if mode == 'N' and file.name == filter:
            filteredFiles.append(file)
        elif mode == 'E' and (file.suffix == filter or file.suffix[1:] == filter):
            filteredFiles.append(file)  # 'E' means the files extension must match the filter
        elif mode == '<' and file.stat().st_size < filter:  # '<' means the files size must be less than the filter
            filteredFiles.append(file)
        elif mode == '>' and file.stat().st_size > filter:  # '> means the files size must be greater than the filter
            filteredFiles.append(file)
        elif mode == 'T':  # 'T' means the file must contain text that matches the filter
            try:
                fileContents = file.read_text()
                if filter in fileContents:
                    filteredFiles.append(file)
                    continue
            except UnicodeDecodeError:  # If the file isn't a text file and we try to read it as one it throws an error
                continue
    return filteredFiles


def take_action(action: str, files: [Path]) -> None:
    """
    Takes a specific action on all of the given files
    :param action: The action that will be taken on all the files
    :param files: The files that the given action will be taken on
    """
    for file in files:
        if action == 'T':  # 'T' means we Touch the file (aka change its modified date to the current time)
            file.touch(exist_ok=True)
        elif action == 'F':  # 'F' means we print out the first line of the file (or 'NOT TEXT') if its not a text file
            try:
                with file.open() as openFile:
                    print(openFile.readline(), end='')
            except UnicodeDecodeError:  # Non text files will throw this exception so we catch it and print 'NOT TEXT'
                print("NOT TEXT")
        elif action == 'D':  # 'D' means we copy the file and append '.dup' to the copy
            newFile = file.parent / Path(file.name + '.dup')
            newFile.write_bytes(file.read_bytes())


def read_first_line() -> (str, Path):
    """
    Reads the first line of input which is a search mode and then a path to a directory
    :return: A tuple containing the search mode ('D' or 'R') and a valid directory path
    """
    while True:
        inputLine = input()
        mode = inputLine[0:1]
        directoryPath = Path(inputLine[2:])
        if not directoryPath.is_dir() or (mode != 'D' and mode != 'R'):
            error()
            continue
        return (mode, directoryPath)


def read_second_line() -> (str, any):
    """
    Reads the second line of input which is a filter mode and then a filter criteria
    :return: A tuple containing the filter mode ('A', 'N', 'E', 'T', '<', '>') and the filter criteria
    """
    while True:
        inputLine = input()
        mode = inputLine[0:1]
        if mode == 'A' and len(inputLine.strip()) == 1:
            return ('A', None)
        elif mode == 'N' or mode == 'E' or mode == 'T':
            if len(inputLine[2:]) > 0:
                return (mode, inputLine[2:])
        elif mode == '<' or mode == '>':
            if len(inputLine[2:]) > 0 and inputLine[2:].isdigit():
                return (mode, int(inputLine[2:]))
        error()


def read_third_line() -> str:
    """
    Reads the third line of input which is an action that should be taken on all the interesting files
    :return: A string ('F', 'F', 'T') that is the action which should be taken on all the interesting files
    """
    while True:
        inputLine = input()
        mode = inputLine[0:1]
        if (mode == 'F' or mode == 'D' or mode == 'T') and len(inputLine.strip()) == 1:
            return mode
        error()


def dig_in_the_dirt() -> None:
    """
    The main function that runs the program
    This function reads the three lines of input, handles acting on that input, and handles printing out the file paths
    """

    # Read the first line of input and then search for files according to it
    mode, path = read_first_line()
    paths = get_all_paths_from_directory(path, mode == 'R')
    print_list(paths)

    # Read the second line of input and then filter out files according to it
    mode, value = read_second_line()
    interestingFiles = filter_files(mode, value, paths)
    if len(interestingFiles) == 0:
        return
    print_list(interestingFiles)

    # Read the third line of input and then take action on the files according to it
    mode = read_third_line()
    take_action(mode, interestingFiles)


# Handles starting the program when it is run as opposed to when it is imported
if __name__ == '__main__':
    dig_in_the_dirt()
