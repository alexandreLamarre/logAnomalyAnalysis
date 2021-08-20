import sys
import os
import time
import datetime
'''
Script to monitor and create logs from
    - Environment variables,
    - Processes 
    - Meminfo
'''


# TODO: option to use a docker volume to persist data in between log collections
PATH_TO_DOCKER_VOLUME = ""

PROC_CACHE = {}
LOG_FILE = "./log_" + str(time.time())


def load_init_proc(startTime):
    """
    Load initially running processes into global dict PROC_CACHE

    @rtype str : log file action string in the format <timestamp> : <message>
    """
    if sys.platform == "darwin":
        cmd = "ps -ae"
        proc_find_process = os.popen(cmd)
        read_proc_find = proc_find_process.read()
        curTime = time.time()
        proc_find_process.close()

        proc_list = str(read_proc_find).strip().split("\n")
        
        for i in range(len(proc_list)):
            proc_list[i] = proc_list[i].split()
            if len(proc_list[i]) >= 4 : 
                key = proc_list[i][3]
                val = " ".join(proc_list[i][0:3]) + " ".join(proc_list[i][4:])
                PROC_CACHE[key] = val
        
        return str(curTime - startTime) + " : Initially loaded processes\n"
        
    elif sys.platform == "linux" or sys.platform == "linux2":
        pass


def load_init_env_var():
    """
    Load initially set environment variables int a dict
    """
    pass

def load_init_mem():
    """
    Load initial meminfo
    """
    pass

def update_proc():
    """
    Update processes in our log using log keywords

    - 'proc_rm' : removed a process
    - 'proc_cr' : create a new process
    - 'proc_up' : updated status of a process 

    @rtype List[tuple], List[tuple], List[tuple] : list of removed processes, list of new processes, list of updated processes
    """
    if sys.platform == "darwin":
        cmd = "ps -ae"
        proc_find_process = os.popen(cmd)
        read_proc_find = proc_find_process.read()
        curTime = time.time()
        proc_find_process.close()


        proc_list = str(read_proc_find).strip().split("\n")

        proc_rm = []
        proc_cr = []
        proc_up = []
        
        temp_dict = dict()

        #TODO: find an efficient way to compare two dictionary differences, maybe python builtin in zip?

        for i in range(len(proc_list)):
            proc_list[i] = proc_list[i].split()
            if len(proc_list[i]) >= 4 : 
                key = proc_list[i][3]
                val = " ".join(proc_list[i][0:3]) + " ".join(proc_list[i][4:])

                if key in PROC_CACHE:
                    if val != PROC_CACHE[key]:
                        proc_up.append((key, val))
                        PROC_CACHE[key] = val
                else:
                    PROC_CACHE[key] = val
                    proc_cr.append((key, val))
                
                temp_dict[key] = val
        
        to_remove = [] #can't remove while iterating inside the dictionary

        for (k,v) in PROC_CACHE.items():
            if k not in temp_dict.keys():
                proc_rm.append((k,v))
                to_remove.append(k)
        
        for k in to_remove:
            PROC_CACHE.pop(k)
        
        return proc_rm, proc_cr, proc_up
        
        
                    

        
        

    elif sys.platform == "linux" or sys.platform == "linux2":
        pass


def update_env_var():
    """
    Update processes in our log using log keywords

    - 'env_rm' : removed a process
    - 'env_cr' : created a new environment variable
    - 'env_up' : updated the value of an environment variable
    """

def update_mem():
    """
    Update meminfo in our log using keywords

    - 'mem_up' : updated status of some meminfo
    """
    pass



if __name__ == "__main__":
    start = time.time() #start all logs at 0, all time measurements will be made relative to start
    log_load_action = load_init_proc(start)    
    try:
        f = open(LOG_FILE, 'w')
    except OSError:
        print("Could not open file", LOG_FILE)
        sys.exit()
    
    f.write(log_load_action)
    for (k,v) in PROC_CACHE.items():
        f.write("\t" + k + " : " + v + "\n")

    while(True):

        proc_rm, proc_cr, proc_up = update_proc()
        curTime = str(time.time() - start)
        for p in proc_rm:
            f.write(curTime + " rm " + p[0] + " : " + p[1] + "\n")
        
        for p in proc_cr:
            f.write(curTime + " cr " + p[0] + " : " + p[1] + "\n")

        for p in proc_up:
            f.write(curTime + " up " + p[0] + " : " + p[1] + "\n")
        
        time.sleep(60)




