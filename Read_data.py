import pandas as pd
import csv
import re
import os

from collections import defaultdict
from pathlib import Path

path = r"C:\Users\Srinija Katakam\Downloads\Kickstarter_Video_Text_Files"
os.chdir(path)

def write_text_file():
    results = defaultdict(list)
    for file1 in Path(path).iterdir():
        with open(file1, "r") as file_open:
            results["file_name"].append(file1.name)
            results["text"].append(file_open.read())
    df = pd.DataFrame(results)
    df.to_csv("your_name.csv")


def read_text_file(file_path):
    data = []
    clean_data = []
    clean_data1 = []
    clean_data2 = []
    with open(file_path, 'r') as f:
        data = f.read().splitlines()
        print(len(data))
        for x in data:
            val = x.strip()
            clean_data.append(val)
            clean_data1 = list(filter(None, clean_data))  # Removing extra new line characters
        clean_data1 = clean_data1[:-2]  # Cleaning last two lines of the textfile
        for line in clean_data1:
            line = line.split(':', 1)[-1].strip();  # Removing Speaker name
            sentence = ' '.join(re.split("\s+", line, flags=re.UNICODE))  # Removing white spaces if any
            clean_data2.append(sentence)
        finalstring = "".join(clean_data2)  # Final String of the text file
        print(len(finalstring))
        with open(file_path, 'w+') as file2:
            file2.write(finalstring)
            file2.close();
            print(len(finalstring))
        print("Writing is done",file2.name)

# iterate through all file
for file in os.listdir():
    # Check whether file is in text format or not
    if file.endswith(".txt"):
        file_path = f"{path}\{file}"
        # call read text file function
        read_text_file(file_path)
        #write_text_file()


