# -*- coding: utf-8 -*-
# HP v3/11/22
#from asyncio.windows_events import NULL
import csv, os, re
import ntpath
import nltk

#hppath = r"D:\TK\20062021\20112021\20162021\2016"
#hppath = r"D:\TK\20062021\20112021\20112015\2011"
#hppath = r"D:\TK\20062021\20062010\2006"
#hppath = r"D:\TK\19942005\19942000"
hppath = r"D:\TK\20022005"
houtpath = r"D:\ANR24\HCap\Hculture\bisearch\Pout"
savefilename ='Hculture20022005.txt'
cikfilepath = r"D:\ANR24\HCap\Hculture\bisearch\hciknoheader.csv"
alphabet = "abcdefghijklmnopqrstuvwxyz1234567890$," #the characters that we'll recognize in cleanfile and findword.
### Import the LM stopwords CSV
with open(r'D:\ANR24\HCap\Hculture\bisearch\hpsw724.csv') as f:
    reader = csv.reader(f)
    lmst = list(reader)
lmstopwords = [i[0] for i in lmst] 

cikset = set()
with open(cikfilepath, 'r') as f:  
    ciklist = f.read().splitlines()
    for i in ciklist:
        cikset.add(int(i))

def lociCollect(path):  
    """Parameters: lociPath : String - Contains the path where the CIK files are stored
    Returns: A list of the filenames and the location of files"""   
    all_files = [] 
    for root, dirname, fname in os.walk(path):
        for file in fname:
            cik = re.findall(r"_\d+_", file)
            cik = cik[0][1:-1]
            if(int(cik) in cikset): #adding only the CIK's specified in the file
                filepath = os.path.join(root, file)
                all_files.append(filepath)
    #tkfiles = [s for s in all_files if re.search('_10-K_edgar',s)]
    tkfiles = [s for s in all_files]
    return tkfiles

def delete_stopwords(text):
    text_tokens = nltk.word_tokenize(text)
    tokens_without_sw = [word for word in text_tokens if not word in lmstopwords]
    return " ".join(tokens_without_sw).strip()
    
def cleanfile(file):
    cleantext = '' #The text we'll end up with  
    #wordcount = 0
    with open(file) as text: 
        for line in text:
            for word in line.split(" "):
                #wordcount += 1
                for letter in word.lower():
                    if letter in alphabet:
                        cleantext += letter #add letters to cleantext
                    else:
                        cleantext += " "
                cleantext += " "#because we split by spaces, we need to add a space after each word.
    return cleantext
def delsw(file):
    cleantext = '' #The text we'll end up with  
    #wordcount = 0
    with open(file) as text: 
        for line in text:
            for word in line.split(" "):
                #wordcount += 1
                for letter in word.lower():
                    if letter in alphabet:
                        cleantext += letter #add letters to cleantext
                    else:
                        cleantext += " "
                cleantext += " "#because we split by spaces, we need to add a space after each word.
    delswtext = delete_stopwords(cleantext)
    return delswtext
    
def findword(file, pattern):
    count = 0
    cleanedtext = delsw(file)   
    instances = re.findall(pattern, cleanedtext)
    count += len(instances)
    filename = ntpath.basename(file)
    if count > 0:
        year = int(filename[0:4])
        cik = re.findall(r"_\d+_", filename)
        cik = cik[0][1:-1]
        return [year, filename, int(cik), count]

def makeFileList():
    sflist = lociCollect(hppath) #574 10Ks   
    delete_stopwords("This         sentence is to test how well stocpwords such as and in Python 3.8 work in this file")
    #chkorg0= cleanfile(sflist[0])
    #chk0= delsw(sflist[0])
    return sflist

# To check if all files in hppath are collected correctly
#chkfilelist = lociCollect(hppath)
#chkflagain = makeFileList()