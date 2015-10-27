import logging
import argparse
from time import time, sleep
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(process)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process(line):
    #sleep(0.01)
    if line[0].isupper():
        return line

def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.next()
        return cr
    return start

@coroutine
def write_line(outfile):
    while True:
        lines = yield
        for line in lines:
            if line:
                outfile.write(line)


def main(infile, outfile, run_processes, workers_count=4):
    ts = time()
    if(run_processes):
        logger.info("Fork processes")
        pool = Pool(processes=workers_count)
    else:
        logger.info("Start threads")
        pool = ThreadPool(processes=workers_count)

    writer = write_line(outfile)

    logger.info("Start line processing")
    pool.map_async(process, infile, callback=lambda line: writer.send(line))

    logger.info("Close pool")
    pool.close()

    logger.info("Waiting while workers finished their queue")
    pool.join()

    print('Took: {}s'.format(time() - ts))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'))
    parser.add_argument('outfile', type=argparse.FileType('w'))
    parser.add_argument('-p', '--process', action='store_true', help='fork processes instead of threads')
    parser.add_argument('-c', '--concurent', nargs='?', type=int, const=4, default=4, help='number of threads (processes)')
    args = parser.parse_args()

    main(args.infile, args.outfile, args.process, args.concurent)


