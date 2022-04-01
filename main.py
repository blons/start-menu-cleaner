from getpass import getuser
from os import listdir, system, get_terminal_size, walk, rename, remove
from colorama import Fore, Back, Style, init, deinit
# from ctypes import windll
from sys import platform #, executable, argv
from math import floor
from shutil import rmtree


# CLS()
# clear screen, multi platform (because checkos() also uses drawpopup())

def cls():
    if platform == 'win32':
        system('cls')
    else:
        system('clear')


# GETTERMSIZE
# get the size of the terminal
# R: width or height of terminal
# axys: what axys to return

w = 'gettermsize.width'
h = 'gettermsize.height'
def gettermsize(axys):
    width, height = get_terminal_size()
    if axys == 'gettermsize.width':
        return width
    elif axys == 'gettermsize.height':
        return height
    else:
        return width, height


# GETPATHS()
# get start folders
# R: paths

def getpaths():
    path1 = 'C:/ProgramData/Microsoft/Windows/Start Menu/Programs'
    path2 = ''.join(('C:/Users/', getuser(), '/AppData/Roaming/Microsoft/Windows/Start Menu/Programs'))
    return path1, path2


# GETSUBDIR()
# get subdirs of dir
# R: LIST of subdirs
# path: absolute path to maindir
# blacklist: LIST of blacklisted folder names

def getsubdirs(path, blacklist):
    sub_full = listdir(path)
    sub_long = dict()
    for sub in sub_full:
        try:
            listdir(''.join((path, '/', sub)))
            if sub not in blacklist:
                sub_long[sub] = ''.join((path, '/', sub))
        except:
            pass
    del sub_full
    return sub_long


# GETFILE()
# enter local text file, get its contents
# R: LIST of lines within file, lines starting with '##' are ignored
# file: name of local file

def getfile(file):
    items = list()
    with open(file) as txt:
        for line in txt.readlines():
            if line[:2] not in ('##', '\n'):
                items.append(line.strip('\n'))
    return items


# CHECKOS()
# exit program on non nt os
# R: nothing

def checkos():
    if platform != 'win32':
        drawpopup('ERROR', ('This script is windows only', f'Detected {platform} instead of win32'), "style.label.red")
        exit(0)


# DRAWPOPUP()
# draw message as popup
# R: nothing
# title: big bold text to show
# description: TUPLE, less important text to show
# theme: what colour to use for title

def drawpopup(title, description, theme):
    cls()
    height = gettermsize(h)
    space_before = floor(((height - 2) - (2 + len(description))) / 2)
    space_after = height - space_before - 2 - len(description) - 2
    for _ in range(space_before):
        print()
    print(centre(style(title, theme), title))
    print()
    for line in description:
        print(centre(line, line))
    for _ in range(space_after):
        print()
    return input().strip().lower()


# STYLE()
# return string with custom style
# string: the string to format
# style: describe how text is formatted, available in styles_dict

def style(string, style):
    styles_dict = {
        'style.counter': f'{Fore.RED}{Back.WHITE}',
        'style.label.red': f'{Fore.BLACK}{Back.RED}',
        'style.label.green': f'{Fore.BLACK}{Back.GREEN}',
        'style.label.white': f'{Fore.BLACK}{Back.WHITE}',
        'style.label.yellow': f'{Fore.BLACK}{Back.YELLOW}',
        'style.label.cyan': f'{Fore.BLACK}{Back.CYAN}',
        'style.string.red': f'{Fore.RED}',
        'style.string.yellow': f'{Fore.YELLOW}',
        'style.string.magenta': f'{Fore.MAGENTA}',
        'style.string.white': f'{Fore.WHITE}',
        'style.string.cyan': f'{Fore.CYAN}',
        'style.reset': f'{Style.RESET_ALL}'
    }
    return ''.join((styles_dict[style], str(string), styles_dict['style.reset']))


# CENTRE()
# return string centered
# string: the formatted string to format
# unformatted_string: unformatted string, necessary for width calculation

def centre(string, unformatted_string):
    space = ''
    width = gettermsize(w)
    space_before = floor((width - len(unformatted_string)) / 2)
    space = ' ' * space_before
    return  ''.join((space, string))


# GETPATHFILES()
# enter a path, returns every item within it
# R: a DICT that lists every item (incl. subfolders) within a dir, the key is the item name, the value is the path of the item

def getpathfiles(path):
    files = {}
    index = {}
    n = 0
    for (wpath, wdirname, wfile) in walk(path):
        for item in wfile:
            n += 1
            files[item] = '/'.join((wpath.replace('\\', '/'), item))
            index[n] = item
    return files, index


# DIRDISPLAY()
# display function, displays content of directories and adds linebreaks if needed

def dirdisplay(files, folder):
    n = 0
    print(f'{style("FOLDER", "style.label.yellow")} {style(folder, "style.string.yellow")}, containing {style(len(files), "style.counter")} {"item" if len(files) == 1 else "items"}{":" if len(files) >= 2 else ""}')
    for item in files:
        name = ''
        parts = item.split('.')
        for part in range(len(parts) - 1):
            name = '.'.join((name, parts[part]))
        name = name[1:]
        n += 1
        if parts[len(parts) - 1].lower() in ('lnk'):
            temp_main = 'style.string.white'
        elif parts[len(parts) - 1].lower() in ('url', 'html'):
            temp_main = 'style.string.cyan'
        else:
            temp_main = 'style.string.yellow'
        print(f'  {style("ITEM", "style.label.cyan")} {style(n, "style.string.red")} {style(name, temp_main)}{style(f".{parts[len(parts) - 1]}", "style.string.magenta")}')
    n += 1
    while n < gettermsize(h) - 4:
        print()
        n += 1


# TERM()
# main input field

def term(log, n, total):
    space = ''
    opt = '[OPTIONS]: [a]dd, [s]kip, [d]elete, [q]uit'
    cur = f'[CURRENT {n}/{total}]'
    width = gettermsize(w)
    if width < len(opt) + len(cur) + 3:
        space_needed = (width - len(cur))
        space = ' ' * space_needed
        print(style(''.join((space, cur)), 'style.label.white'))
    else:
        space_needed = (width - len(opt) - len(cur))
        space = ' ' * space_needed
        print(style(''.join((opt, space, cur)), 'style.label.white'))
    space_needed = (width - len(log))
    space = ' ' * space_needed
    print(style(''.join((log, space)), 'style.label.green'))
    return input(f'{Fore.GREEN}>> ').strip().lower().split()


# THATSWHATSHESAID()
# block if too smol

def thatswhatshesaid():
    if gettermsize(w) > 45 and gettermsize(h) > 14:
        return False
    return True


# COMMAND()
# get what command was entered

def command(input, files, index, folder, folders):
    if input == []:
        input = ['']
    match input[0]:
        case 's':
            return -1
        case 'a':
            return additem(input, files, index)
        case 'd':
            return delitem(input, files, index, folder, folders)
        case 'q':
            return quitmenu()
        case '':
            return 'No command entered'
        case _:
            return f'No command found: {input[0]}'


# ADDITEM()
# moves item to main dir

def additem(input, files, index):
    if len(input) >= 2:     # if index was provided
        try:
            filewpath = files[index[int(input[1])]]
            filename = index[int(input[1])]
        except:
            return 'Incorrect index (index out of range)'
        try:
            int(input[1])
            try:
                rename(filewpath, '/'.join((cut(filewpath), filename)))
            except:
                return 'Moving file failed (most likely lack of permissions)'
        except:
            return 'Incorrect index (something sus happened, this error should not be possible)'
        return f'Moved {filename} out'
    else:                   # if index wasn't provided
        for file in files:
            try:
                filewpath = files[file]
            except:
                return 'Incorrect index (index out of range)'
            try:
                rename(filewpath, '/'.join((cut(filewpath), file)))
            except:
                return 'Moving file failed (most likely lack of permissions)'
        return f'Moved {len(files)} file(s) out'


# DELITEM()
# deletes item irrecoveribly

def delitem(input, files, index, folder, folders):
    if len(input) >= 2:     # if index was provided
        try:
            filewpath = files[index[int(input[1])]]
            filename = index[int(input[1])]
        except:
            return 'Incorrect index (index out of range)'
        try:
            int(input[1])
            try:
                remove(filewpath)
            except:
                return 'Deleting file failed (most likely lack of permissions)'
        except:
            return 'Incorrect index (something sus happened, this error should not be possible)'
        return f'Deleted {filename}'
    else:                   # if index wasn't provided
        try:
            rmtree(folders[folder])
            return -2
        except:
            return 'Deleting folder failed (most likely lack of permissions)'


# CUT()
# get main path

def cut(path):
    path = path.split('/')
    newpath = ''
    for item in path:
        if item != 'Programs':
            newpath = '/'.join((newpath, item))
        else:
            newpath = '/'.join((newpath, item))
            newpath = newpath[1:]
            return newpath


# QUITMENU()
# the name sums it up pretty well

def quitmenu():
    while True:
        i = drawpopup('WARNING', ('Are you sure you want to quit', '[y]es, [n]o'), "style.label.red")
        if i == 'y':
            cls()
            exit()
        elif i == 'n':
            return ''


# MAINLOOP
# encloses the main mechanics in a loop
# dirs: a DICT that lists every subfolder to check, the key is the folder name, the value is the path of the folder
# Use | dir | for key and | dirs[dir] | for path
# lock: locks while loop until [s]kip is entered
# files: a DICT that lists every item (incl. subfolders) within a dir, the key is the item name, the value is the path of the item
# log: string display at the bottom

def mainloop():
    path1, path2 = getpaths()
    blacklist = getfile('blacklist.txt')
    dir1, dir2 = getsubdirs(path1, blacklist), getsubdirs(path2, blacklist)
    dirs = dir1 | dir2
    n = 0
    total = len(dirs)
    log = 'Enter a command'
    del dir1, dir2, path1, path2, blacklist
    for dir in dirs:
        n += 1
        lock = True
        while lock:
            files, index = getpathfiles(dirs[dir])
            cls()
            while thatswhatshesaid():
                drawpopup('WARNING', ('Window is too small',), "style.label.red")
            dirdisplay(files, dir)
            input = term(log, n, total)
            log = command(input, files, index, dir, dirs)
            if log == -1:
                lock = False
                log = 'Enter a command'
            elif log == -2:
                lock = False
                log = f'Deleted {dir}'


# __MAIN__
# entrypoint

if __name__ == "__main__":
    init()
    checkos()
    # windll.shell32.ShellExecuteW(None, 'runas', executable, ' '.join(argv), None, None)
    drawpopup('WARNING', ('This script requires admin permissions', 'The folders modified are admin protected'), "style.label.red")
    mainloop()
    cls()
    deinit()
