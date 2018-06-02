#!/usr/bin/env python

import re
import tarfile
import os
import sys

def checkIfTar(argument):

    if argument[-7:] == ".tar.gz" or argument[-4:] == ".tar":
        return True
    else:
        return False

def parseTarArchive(nFlag, cFlag, fileToParse):
    #Parse the tar archive and read the lines also check
    #if there are any more tar archives within

    tar = tarfile.open(fileToParse)

    if cFlag is True:
        print("Number of files in " + fileToParse +  " is: " + str(len(tar.getmembers())))

    for member in tar.getmembers():

        #check if there are tar files within and if there are
        #make a recursive call

        if checkIfTar(member.name) is True:
            parseTarArchive(nFlag, cFlag, member.name)
        #do the same for subdirectories
        elif os.path.isdir(member.name) is True:
            parseDirectory(nFlag, cFlag, member.name)

        f = tar.extractfile(member)

        content = f.read()

        if nFlag is True:
            if bool(re.search("much Open, such Stack", content)) is True:
                print("A file inside " + fileToParse + " that contains 'much Open, such Stack:'" + member.name)


    tar.close()


def parseDirectory(nFlag, cFlag, directoryToParse):

    filesInsideDir = os.listdir(directoryToParse)

    os.chdir(directoryToParse)

    for fi in filesInsideDir:
        if checkIfTar(fi) is True:
            parseTarArchive(nFlag, cFlag, fi)
        elif os.path.isdir(fi) is True:
            parseDirectory(nFlag, cFlag, fi)

def checkArguments():
    nFlag = False
    cFlag = False
    isTar = False
    isDirectory = False

    index = -1
    parsePosition = -1

    for argument in sys.argv:

        index += 1

        if argument == "-n":
            nFlag = True
        elif argument == "-c":
            cFlag = True
        elif os.path.isdir(argument) is True:
            isDirectory = True
            parsePosition = index

        isTar = checkIfTar(argument)

        if isTar is True:
            parsePosition = index

    if isTar is True:
        parseTarArchive(nFlag, cFlag, sys.argv[parsePosition])
    elif isDirectory is True:
        parseDirectory(nFlag, cFlag, sys.argv[parsePosition])
    else:
        print("You must include a directory or a tar archive to parse")

def checkPermission():
    if os.geteuid() is not 0:
        checkArguments()
    else:
        print("Only for non root")

if __name__ == "__main__":
    checkPermission()
