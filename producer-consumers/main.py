import logging
import os
import argparse
from time import time
from Queue import Empty
from threading import Thread
from multiprocessing import Process, JoinableQueue, Event, Lock, Manager
from os import SEEK_SET

import struct, fcntl

logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(process)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TIMEOUT = 0.05 # Used to set timeout for Queue get method

class Worker(object):
    def __init__(self, worker, line_queue, lock, outfile):
        self.process = worker()
        self.process.__init__()

        self.lines_queue = line_queue
        self.lock = lock
        #self.outfile = open(outfile, 'w')
        self.outfile = outfile

        self.stoprequest = Event()
        self.process.run = self.run

    def print_line(self, line):
        self.lock.acquire(True)
        logger.debug('Writing:"{}"'.format(line))
        self.outfile.write(line)
        self.lock.release()


    def run(self):
        while not self.stoprequest.is_set():
            try:
                line = self.lines_queue.get(True, TIMEOUT)
                logger.debug('Processing:"{}"'.format(line))
                if line[0].isupper():
                    self.print_line(line)
                    #self.print_queue.put(line)
                self.lines_queue.task_done()
            except Empty:
                continue


#class WriteThread(Thread):
    #def __init__(self, print_queue, outfile):
        #super(WriteThread, self).__init__()
        #self.print_queue = print_queue
        #self.outfile = outfile
        #self.stoprequest = Event()

    #def run(self):
        #while not self.stoprequest.isSet():
            #try:
                #line = self.print_queue.get(True, 0.05)
                #logger.debug('Writing:"{}"'.format(line))
                #self.outfile.write(line)
                #self.print_queue.task_done()
            #except Empty:
                #continue


def read_lines(infile):
    buff = ""
    char = infile.read(1)
    while char:
        char = infile.read(1)
        buff = buff + char

        # Return buffer if we've found the new line
        if char == "\n" and buff:
            yield buff
            buff = ""


def main(infile, outfile, run_processes, workers_count=4):
    ts = time()
    lines_queue = JoinableQueue()
    manager = Manager()
    lock = manager.Lock()
    print lock
    workers = []


    # Create worker threads
    for x in range(workers_count):
        if run_processes:
            logger.info("Forking process")
            worker = Worker(Process, lines_queue, lock, outfile)
        else:
            logger.info("Running thread")
            worker = Worker(Thread, lines_queue, lock, outfile)
        worker.process.start()
        workers.append(worker)

    # Spawn threads to write
    #logger.info("Running writer thread")
    #writer = WriteThread(print_queue, outfile)
    #writer.start()

    logger.info("Start reading lines")
    # Put the tasks into the queue
    for line in read_lines(infile):
        logger.debug('Queueing:"{}"'.format(line))
        lines_queue.put(line)

    # Wait while all workers finished their queue
    logger.info("Waiting while workers finished their queue")
    lines_queue.join()

    # Send stop event to all workers
    for worker in workers:
        worker.stoprequest.set()

    # Wait for all workers
    logger.info("Waiting workers")
    for worker in workers:
        worker.process.join()

    # Wait while all print_queue will be processed
    #logger.info("Waiting print queue")
    #print_queue.join()
    ## Stop writer
    #writer.stoprequest.set()
    ## Wait for writer
    #writer.join()

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


