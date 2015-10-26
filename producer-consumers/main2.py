import logging
import argparse
from time import time
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool
#import os
#from Queue import Empty
#from threading import Thread
#from multiprocessing import Process, JoinableQueue, Event, Lock, Manager, Pool
#from os import SEEK_SET


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(process)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process(line):
    if line[0].isupper():
        return line


def main(infile, outfile, run_processes, workers_count=4):
    ts = time()
    if(run_processes):
        logger.info("Fork processes")
        pool = Pool(processes=workers_count)
    else:
        logger.info("Start threads")
        pool = ThreadPool(processes=workers_count)

    def write_line(lines):
        for line in lines:
            if line:
                outfile.write(line)

    logger.info("Start line processing")
    pool.map_async(process, infile, callback=write_line)

    logger.info("Close pool")
    pool.close()

    logger.info("Waiting while workers finished their queue")
    pool.join()

    print('Took: {}s'.format(time() - ts))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'))
    parser.add_argument('outfile', type=argparse.FileType('w'))
    #parser.add_argument('outfile')
    parser.add_argument('-p', '--process', action='store_true', help='fork processes instead of threads')
    parser.add_argument('-c', '--concurent', nargs='?', type=int, const=4, default=4, help='number of threads (processes)')
    args = parser.parse_args()

    main(args.infile, args.outfile, args.process, args.concurent)



