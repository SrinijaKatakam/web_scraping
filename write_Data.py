import pandas as pd
import csv
import re
import os

from collections import defaultdict
from pathlib import Path

path = r"C:\Users\Srinija Katakam\Downloads\Kickstarter_Video_Text_Files"
os.chdir(path)


results = defaultdict(list)
def write_text_file(file_path,file):
    data = []

    with open(file_path, 'r') as f:
        data = f.read().splitlines()
        print(len(data))
        for x in data:
            print("LEngth of x", len(x))
            results["file_name"].append(file)
            results["text"].append(x)
            print(results)
    df = pd.DataFrame(results)
    print("DataaaaFrameee",df)
    df.to_csv("sri.csv",  header=True, index=False,  encoding='ansi')

# iterate through all file
for file in os.listdir():
    # Check whether file is in text format or not
    if file.endswith(".txt"):
        print("1")
        file_path = f"{path}\{file}"
        # call read text file function
        write_text_file(file_path,file)
        #write_text_file()


