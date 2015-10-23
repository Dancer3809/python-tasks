import logging
import os
import argparse
import threading
from time import time
from Queue import Queue
from threading import Thread
from os import SEEK_SET

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ProcessThread(Thread):
    def __init__(self, line_queue, print_queue):
        super(ProcessThread, self).__init__()
        self.lines_queue = line_queue
        self.print_queue = print_queue
        self.stoprequest = threading.Event()

    def run(self):
        while not (self.stoprequest.isSet() and self.lines_queue.empty()):
            # Get the work from the queue
            line = self.lines_queue.get()
            logger.debug('Processing:"{}"'.format(line))
            if line[0].isupper():
                self.print_queue.put(line)
            self.lines_queue.task_done()


def process_lines(lines_queue, print_queue):
    stoprequest = threading.Event()
    while not stoprequest and not lines_queue.empty():
        # Get the work from the queue
        line = lines_queue.get()
        logger.debug('Processing:"{}"'.format(line))
        if line[0].isupper():
            print_queue.put(line)
        lines_queue.task_done()


def write_lines(print_queue, outfile):
    while True:
        line = print_queue.get()
        logger.debug('Writing:"{}"'.format(line))
        outfile.write(line)
        print_queue.task_done()


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


def main(infile, outfile):
    ts = time()

    lines_queue = Queue()
    print_queue = Queue()

    workers = []


    # Create worker threads
    for x in range(4):
        #worker = Thread(target=process_lines, args=(lines_queue, print_queue))
        worker = ProcessThread(lines_queue, print_queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
        workers.append(worker)

    # Spawn threads to write
    writer = Thread(target=write_lines, args=(print_queue, outfile))
    writer.daemon = True
    writer.start()

    # Put the tasks into the queue
    for line in read_lines(infile):
        logger.debug('Queueing:"{}"'.format(line))
        lines_queue.put(line)

    for worker in workers:
        worker.stoprequest.set()

    # Causes the main thread to wait for the queue to finish processing all the tasks
    print_queue.join()
    print('Took: {}s'.format(time() - ts))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'))
    parser.add_argument('outfile', type=argparse.FileType('w'))
    args = parser.parse_args()

    main(args.infile, args.outfile)

