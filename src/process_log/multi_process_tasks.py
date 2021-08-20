from multiprocessing.pool import ThreadPool
import threading
import time
import queue

#TODO: brainstorming idea #1
class customThreadPool():
    def __init__(self, threadList, nameList, workQueue):
        """
        
        """
        self.threadList = threadList
        self.nameList = nameList
        self.workQueue = workQueue
        self.queueLock = threading.lock()
        self.threads = []
        self.threadId = 1
        self.exitFlag = 0
    
    def process_data(self, threadName, q):
        """
        
        """
        while not self.exitFlag:
            self.queueLock.acquire()
            if not self.workQueue.empty():
                data = q.get()
                self.queueLock.release()
                print("%s processing %s " % (threadName, data))
            else:
                self.queueLock.release()
                time.sleep(1)
    
    def setup(self):
        """

        """
        for tName in self.threadList:
            thread = customThread(self.threadId, tName, self.workQueue)
            thread.start()
            self.threads.append(thread)
            self.threadId += 1
        print(threading.enumerate())
    
    def main(self):
        """
        
        """
        self.queueLock.acquire()
        for word in self.nameList:
            self.workQueue.put(word)
        self.queueLock.release()

        while not self.workQueue.empty():
            pass
            
        self.exitFlag = 1

        for t in self.threads:
            t.join()
        
        print(threading.enumerate())
        print("All sub-threads have stopped")



class customThread(threading.Thread):
    def __init__(self, threadId, name, workQueue, *args):
        threading.Thread.__init__(self)
        self.name = name
        self.threadId = threadId
        self.q = workQueue
    
    def run(self):
        pass


#TODO: brainstorming idea number 2
def multiprocess_tasks_basic(callback = None, *zipped_args):
    """


    @type func : callback
    @type List[tuple(func, *func_args)] zipped_
    """

    #TODO: not done, this is a brainstorming idea
    num = None # set to the number of workers we want, default to multiprocessing.cpu_count()
    tp = ThreadPool(num)

    
    for el in zipped_args:

        if len(el) == 1:
           tp.apply_async(el)
        elif len(el) == 2:
            work, args = el
            tp.apply_async(work, args)


    tp.close()
    tp.join()