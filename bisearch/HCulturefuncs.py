# -*- coding: utf-8 -*-
# HP v3/11/22
import csv, os, re
import ntpath
import nltk

# Ensure necessary NLTK resources are available
# nltk.download('punkt')

# File paths updated for local directories
savefilename = 'Hculture20022005.txt'
alphabet = "abcdefghijklmnopqrstuvwxyz1234567890$,"  # characters to recognize in cleanfile and findword.

hppath = "./TK/20022005"
houtpath = "./Pout"
cikfilepath = "./hciknoheader.csv"

# Import the LM stopwords CSV
with open('./hpsw724.csv', encoding='utf-8') as f:
    reader = csv.reader(f)
    lmst = list(reader)
lmstopwords = [i[0] for i in lmst]

cikset = set()
with open(cikfilepath, 'r', encoding='utf-8') as f:

    ciklist = f.read().splitlines()
    for i in ciklist:
        cikset.add(int(i))


def lociCollect(path):
    """Parameters: lociPath : String - Contains the path where the CIK files are stored
    Returns: A list of the filenames and the location of files"""
    all_files = []
    for root, dirname, fname in os.walk(path):
        for file in fname:
            # print(file, fname)
            try:
                cik = re.findall(r"_\d+_", file)
                cik = cik[0][1:-1]
                if int(cik) in cikset:  # adding only the CIK's specified in the file
                    filepath = os.path.join(root, file)
                    all_files.append(filepath)
            except IndexError:
                print(f"Error processing file: {file}, skipping...")
    return all_files

def lociCollectNatural(path):
    """Parameters: lociPath : String - Contains the path where the CIK files are stored
    Returns: A list of the filenames and the location of files"""
    all_files = []
    for root, dirs, files in os.walk(path):  # Iterate through all directories and files
        for file in files:
            try:
                # Modify regex to match numbers after "data_" part of the filename
                cik = re.findall(r"data_(\d+)", file)  # Match the CIK number after 'data_'
                if cik:  # Check if CIK is found
                    cik = cik[0]  # Get the first match
                    print(cik)
                    if int(cik) in cikset:  # Only add files with CIK in the set
                        filepath = os.path.join(root, file)
                        all_files.append(filepath)
            except IndexError:
                print(f"Error processing file: {file}, skipping...")
    return all_files


def delete_stopwords(text):
    text_tokens = nltk.word_tokenize(text)
    tokens_without_sw = [word for word in text_tokens if word not in lmstopwords]
    return " ".join(tokens_without_sw).strip()


def cleanfile(file):
    cleantext = ''  # The text we'll end up with
    try:
        with open(file, 'r', encoding='utf-8') as text:
            content = text.read().lower()  # Process whole file at once
            for letter in content:
                if letter in alphabet:
                    cleantext += letter  # add letters to cleantext
                else:
                    cleantext += " "  # non-alphabet characters replaced with space
    except FileNotFoundError:
        print(f"File {file} not found.")
    return cleantext


def delsw(file):
    try:
        cleantext = cleanfile(file)
        delswtext = delete_stopwords(cleantext)
    except FileNotFoundError:
        print(f"File {file} not found.")
        delswtext = ""
    return delswtext


def findword(file, pattern):
    count = 0
    try:
        cleanedtext = delsw(file)
        instances = re.findall(pattern, cleanedtext)
        count += len(instances)
        filename = ntpath.basename(file)
        if count > 0:
            year = int(filename[0:4])
            cik = re.findall(r"_\d+_", filename)
            cik = cik[0][1:-1]
            return [year, filename, int(cik), count]
    except FileNotFoundError:
        print(f"File {file} not found.")
    return None


def makeFileList():
    sflist = lociCollect(hppath)  # Collect files from the specified path
    # sflist = lociCollectNatural(hppath)
    delete_stopwords("This sentence is to test how well stopwords such as and in Python 3.8 work in this file")
    return sflist

