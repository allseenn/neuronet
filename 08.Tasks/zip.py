#!/usr/bin/python
import os
import time
import zipfile
SIZE_LIMIT = 500_000_000

zip_file = "train.zip"
with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.extractall()
time.sleep(2)
folder = os.sys.argv[1]
files = os.listdir(folder)
print(f"{len(files)} files unzipped to {folder}")
files = os.scandir(folder)
part = 0
sum = 0
zip = dict()
zip_file = zipfile.ZipFile(f'{part}.zip', 'w')
zip_file.write(folder)
for file in files:
    if SIZE_LIMIT > sum:
        sum += file.stat().st_size
        zip_file.write(file.path, f"{folder}/{file.name}")
    else:
        zip_file.write(file.path, f"{folder}/{file.name}")
        zip_file.close()
        print(f"Part {part} has {sum/1024/1024} MB added to {part}.zip")
        part += 1
        sum = 0
        zip_file = zipfile.ZipFile(f'{part}.zip', 'w')
        zip_file.write(folder)

zip_file.close()
print(f"Part {part} has {sum/1024/1024} MB added to {part}.zip")
os.system(f"rm -rf {folder}")
