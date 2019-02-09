import argparse
import sys
import os
import re
import json
from shutil import copyfile, move
from colorama import init
from colorama import Fore, Style
init()

# CONSTANTS
SIZE_DIRS = [
    "hdpi",
    "ldpi",
    "mdpi",
    "xhdpi",
    "xxhdpi",
    "xxxhdpi"
]
DRAWABLE = 'drawable'
MIPMAP = 'mipmap'

CONFIG_FILE_NAME = 'config.json'
FROM_DIR_KEY = 'from-dir'
TO_DIR_KEY = 'to-dir'

COMMAND_DESCRIPTON = "Collection of tools to manipulate Android drawable files."+"\nAvailable tools: copy, rename and copy-rename." + \
    "\nAll actions will try to run through every drawable directory.\nDirectory paths must lead to the res folder and filenames must include their extension.\nTo rename a file simly use oldName.png>newName.png"

# ARGUMENT PARSER
parser = argparse.ArgumentParser(description=COMMAND_DESCRIPTON)
parser.add_argument('files', metavar='file-name', type=str, nargs='+',
                    help='A drawable file name. Use oldName>newName to rename it aswell.')
parser.add_argument('--from-dir', metavar='dir', type=str, nargs=1,
                    help='Directory to the source android project')
parser.add_argument('--to-dir', metavar='dir', type=str, nargs=1,
                    help='Directory to the target android project')
parser.add_argument('--drawable', action='store_true',
                    help='Use drawable directories')
parser.add_argument('--mipmap', action='store_true',
                    help='Use mipmap directories')
parser.add_argument('--no-copy', action='store_true',
                    help='Don\'t copy, only rename')


# METHODS
def writeDirsToConfig(fromDir: str, toDir: str):
    config = {
        FROM_DIR_KEY: fromDir,
        TO_DIR_KEY: toDir
    }
    with open(CONFIG_FILE_NAME, 'w') as configFile:
        json.dump(config, configFile)


def readFromConfig(key: str):
    try:
        with open(CONFIG_FILE_NAME) as configFile:
            config = json.load(configFile)
            return config[key]
    except Exception:
        return None


def readFromDirFromConfig():
    return readFromConfig(FROM_DIR_KEY)


def readToDirFromConfig():
    return readFromConfig(TO_DIR_KEY)


def color(color: Fore, text: str):
    return color + Style.BRIGHT + text + Style.RESET_ALL


def error(msg: str):
    print(color(Fore.RED, 'Error: '+msg))


def failure(msg: str):
    print('['+color(Fore.RED, 'X')+'] Failure: '+color(Fore.RED, msg))


def success(msg: str):
    print('['+color(Fore.GREEN, '+')+'] Success: '+msg)


def checkFileNameFormat(fileName: str):
    return re.match('[\w]+(\.\w+)+', fileName) is not None


def copyFile(pathA: str, pathB: str, dirname: str, name: str, nameTo: str, noCopy: bool):
    action = '\n>> '
    if noCopy:
        action += 'Renaming '
    else:
        action += 'Copying '
    print(action
          + color(Fore.YELLOW, dirname+'/'+name)
          + " to "
          + color(Fore.YELLOW, dirname+'/'+nameTo)
          )
    try:
        if noCopy:
            move(pathA, pathB)
            success('File renamed')
        else:
            copyfile(pathA, pathB)
            success('File copied')
        return 0
    except Exception as ex:
        failure(str(ex))
        return 1


def copy(dir: str, fromDir: str, toDir: str, name: str, nameTo: str, noCopy: bool):
    errors = 0

    pathA = os.path.join(fromDir, dir, name)
    pathB = os.path.join(toDir, dir, nameTo)
    errors += copyFile(pathA, pathB, dir, name, nameTo, noCopy)

    for sizeDir in SIZE_DIRS:
        dirname = dir+'-'+sizeDir
        pathA = os.path.join(fromDir, dirname, name)
        pathB = os.path.join(toDir, dirname, nameTo)

        errors += copyFile(pathA, pathB, dirname, name, nameTo, noCopy)

    return errors


def run(fromDir: str, toDir: str, noCopy: bool, useDrawable: bool, useMipmap: bool, files: list):
    errors = 0
    for file in files:
        name = file
        match = re.search("(.+)>(.+)", name)
        nameTo = name

        if match is not None:
            name = match.group(1)
            nameTo = match.group(2)

        if not checkFileNameFormat(name) or not checkFileNameFormat(nameTo):
            print()
            failure('Invalid filenames: '+name+'>'+nameTo)
            errors += 1
            continue

        if useDrawable:
            errors += copy(DRAWABLE, fromDir, toDir, name, nameTo, noCopy)
        if useMipmap:
            errors += copy(MIPMAP, fromDir, toDir, name, nameTo, noCopy)

    return errors


def main():
    argsInput = sys.argv
    argsInput.pop(0)
    args = parser.parse_args(argsInput)

    useDrawable = args.drawable
    useMipmap = args.mipmap
    noCopy = args.no_copy

    fromDir = args.from_dir or readFromDirFromConfig()
    toDir = args.to_dir or readFromDirFromConfig()

    if fromDir is None and noCopy:
        error('No backup config found, you must provide a from-dir')
        return
    elif fromDir is None or toDir is None:
        error('No backup config found, you must provide both from-dir and to-dir')
        return

    if type(fromDir) is list:
        fromDir = fromDir[0]
    if type(toDir) is list:
        toDir = toDir[0]

    writeDirsToConfig(fromDir, toDir)

    if noCopy:
        toDir = fromDir

    print('\nfrom-dir: '+color(Fore.CYAN, fromDir))
    print('to-dir: '+color(Fore.CYAN, toDir))
    inp = input('\nContinue with these directories? [Y/n]>')
    if not (inp == "y" or inp == "Y" or inp == ""):
        return

    files = args.files

    errors = run(fromDir, toDir, noCopy, useDrawable, useMipmap, files)

    print()
    if errors < 1:
        print(color(Fore.GREEN, '>> All Done! <<'))
    else:
        print(
            color(Fore.RED, '>> [!] Finished with '+str(errors)+' failures! <<'))


if __name__ == "__main__":
    main()
