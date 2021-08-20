import sys
import os
import time
import datetime
import subprocess
import threading
from multiprocessing.pool import ThreadPool
import traceback

SYSTEM_LOG_MESSAGES = '/var/log/system.log'

def tail_f(file):
    """
    
    @rtype subprocess
    """
    try:
        tail_process = subprocess.Popen("tail -f ".format(), shell =True, 
                        stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    except:
        e = sys.exc_info()
        print(repr(e))
        print(traceback.format_exc())
        return None

    print("Type of subprocess popen", type(tail_process))
    return tail_process

if __name__ == "__main__":

    num = None # set to the number of workers we want, default to multiprocessing.cpu_count()
    tp = ThreadPool(num)

    # TODO: some multiprocessing tasks here
    #for el in __:
    #    tp.apply_async(func, (args,))

    tp.close()
    tp.join()
    proc = tail_f(SYSTEM_LOG_MESSAGES)
    while(True):
        try:
            out, err = proc.communicate()
            print("out : ", out)
            print("err : ", err)
        except:
            e = sys.exc_info()
            print(repr(e))
            print(traceback.format_exc())

        finally:
            proc.kill()
