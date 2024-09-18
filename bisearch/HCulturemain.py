import datetime as dt
import multiprocessing as mp
import dictionary
import HCulturefuncs
import csv
import sys
from multiprocessing import Pool
houtpath = r"D:\ANR24\HCap\Hculture\bisearch\Pout"
savefilename ='Hculture20022005.txt'


def runFile(fileName, q):       
        for iword in dictionary.data:            
            fileWordFind = HCulturefuncs.findword(fileName ,iword) # NonType object
            if fileWordFind != None:
                
                fileWordFind.insert(0,iword)
                line = ",".join(str(x) for x in fileWordFind)
                print(f'\n', line)
                q.put(line)
        return

def listener(q):
    with open(houtpath+'/'+savefilename,'w', newline = '') as hpofile:
        hpofile.write("Word, Year, FileName, CIK, WordCount\n")
        while 1:
            m = q.get()
            if(m == 'kill'):
                break          
            hpofile.write(str(m)+ '\n')
            hpofile.flush()

if __name__ == '__main__':
    
    print(f'\n\n{dt.datetime.now().strftime("%c")}\nPROGRAM NAME: {sys.argv[0]}\n')
    print(f'\n Number of Processors: ', mp.cpu_count())
    
    sflist = HCulturefuncs.makeFileList()
    start = dt.datetime.now()
    
    manager = mp.Manager()
    q = manager.Queue() 
    pool = mp.Pool(mp.cpu_count()+1)

    watcher = pool.apply_async(listener, (q,))

    jobs = []
    for i in range(len(sflist)):
        job = pool.apply_async(runFile, (sflist[i], q))
        jobs.append(job)

    for job in jobs:
        job.get()
    q.put('kill')
    pool.close()
    pool.join()
            
    print(f'\n\nRuntime: {(dt.datetime.now()-start)}')
    print(f'\nNormal termination.\n{dt.datetime.now().strftime("%c")}\n')


