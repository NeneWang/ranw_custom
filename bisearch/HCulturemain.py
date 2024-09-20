import datetime as dt
import multiprocessing as mp
from datetime import datetime

import dictionary
import HCulturefuncs
import csv
import sys

from multiprocessing import Pool


import nltk
nltk.download('punkt')



# Local directory paths
houtpath = "./Pout"
savefilename = 'Hculture20022005.txt'


def runFile(fileName, q, taskn=1):
    for iword in dictionary.data:
        fileWordFind = HCulturefuncs.findword(fileName, iword)
        if fileWordFind is not None:
            fileWordFind.insert(0, iword)
            line = ",".join(str(x) for x in fileWordFind)
            print(f'\n', datetime.now(),taskn, line)
            q.put(line)
    return


def listener(q):
    with open(houtpath + '/' + savefilename, 'w', newline='') as hpofile:
        hpofile.write("Word, Year, FileName, CIK, WordCount\n")
        while True:
            m = q.get()
            if m == 'kill':
                break
            hpofile.write(str(m) + '\n')
            hpofile.flush()


if __name__ == '__main__':
    print(f'\n\n{dt.datetime.now().strftime("%c")}\nPROGRAM NAME: {sys.argv[0]}\n')
    print(f'\n Number of Processors: ', mp.cpu_count())

    sflist = HCulturefuncs.makeFileList()
    start = dt.datetime.now()

    manager = mp.Manager()
    q = manager.Queue()
    pool = mp.Pool(mp.cpu_count() + 1)

    watcher = pool.apply_async(listener, (q,))

    jobs = []
    taskn =0
    for i in range(len(sflist)):
        taskn+=1
        job = pool.apply_async(runFile, (sflist[i], q, taskn))
        jobs.append(job)

    for job in jobs:
        job.get()
    q.put('kill')
    pool.close()
    pool.join()

    print(f'\n\nRuntime: {(dt.datetime.now() - start)}')
    print(f'\nNormal termination.\n{dt.datetime.now().strftime("%c")}\n')
