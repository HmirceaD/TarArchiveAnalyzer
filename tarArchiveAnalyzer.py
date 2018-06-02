#!/usr/bin/env python

import os
import sys

def checkIfTar(argument):

    print(argument[-7:])
    print(argument[-4:])

    if argument[-7:] == ".tar.gz" or argument[-4:] == ".tar":
        return True
    else:
        return False

def checkArchive():
    print("E buyn")

def checkArguments():
    nFlag = False
    cFlag = False
    isTar = False

    for argument in sys.argv:
        if argument is "-n":
            nFlag = True
        elif argument is "-c":
            cFlag = True
        isTar = checkIfTar(argument)

    if isTar is True:
        checkArchive()
    else:
        print("You must give a .tar or .tar.gz archive as argument")

def checkPermission():
    if os.geteuid() is not 0:
        checkArguments()
    else:
        print("Only for non root")

if __name__ == "__main__":
    checkPermission()
