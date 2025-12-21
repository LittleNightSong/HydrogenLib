import fnmatch

from modules.hydrogenlib.hycore import listdir, copyfile

if __name__ == '__main__':
    for file in listdir('.'):
        if fnmatch.fnmatch(file, '*.py'):
            copyfile(file, "..\\.git\\hooks\\" + file[:-3])

    print("Install Successful")
