#!/usr/bin/python

from os import listdir, chdir, remove
from os.path import join, isfile
import re
from pathlib import Path
import filecmp

if __name__ == '__main__':
    downFolder = str(Path.home()) + '/Downloads'
    chdir(downFolder)
    files = [x for x in listdir('.') if isfile(x)]
    
    match = '.*\(.*\d*\)'
    r = re.compile(match)
    suspected = list(filter(r.search, files))
    if suspected:
        count = 0
        for f in suspected:
            if [x for x in files if filecmp.cmp(x, f)]:
                remove(f)
                files.remove(f)
                count += 1
        print(f'{count} Files deleted from downloads')

