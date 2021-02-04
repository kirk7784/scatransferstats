# count how many tiff files are in each folder
# add up the total file sizes in gb
# update Stats sheet with info
# (optional) simplify dependencies, avoid using json file for creds

import shutil
import pathlib
from pathlib import Path
from shutil import copytree, ignore_patterns

destination = 'C:/Users/k2wang/Desktop/py/myScripts/scaScansStats/destination/for_matt/'

# copy folder and tiff files to destination and ignore cr2 files
for folder in Path().iterdir():
    if folder.is_dir():
        dest = destination + str(folder)
        shutil.copytree(folder, dest, ignore=ignore_patterns('*.cr2'))
        count = 0
        for path in pathlib.Path(dest).iterdir():
            if path.is_file():
                count += 1
                print(count)