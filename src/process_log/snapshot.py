import sys
import os
import time
import datetime
import helpers

'''
Script to monitor and create logs from
    - Environment variables,
    - Processes 
    - Meminfo
'''


# TODO: option to use a docker volume to persist data in between log collections
PATH_TO_DOCKER_VOLUME = ""

PROC_CACHE = {}
ENV_CACHE = {}
MEMINFO_CACHE = {}
LOG_FILE = "./log_" + str(time.time())


def load_init_proc(startTime):
    """
    Load initially running processes into global dict PROC_CACHE

    @type float startTime: the epoch start time of the snapshot script

    @rtype str : log file action string in the format <timestamp> : <message>
    """

    #TODO: separate time running from value into (value, time)
    if sys.platform == "darwin": # Mac OSX
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


def load_init_env_var(startTime):
    """
    Load initially set environment variables int a dict

    @type float startTime : epoch start time of the snapshot script

    @rtype str : log file action string in the format <timestamp> : <message>
    """
    if sys.platform == "darwin": # Mac OSX
        cmd = "printenv"
        env_find_process = os.popen(cmd)
        read_env_find = env_find_process.read()
        curTime = time.time()
        env_find_process.close()

        env_list = str(read_env_find).strip().split("\n")

        for i in range(len(env_list)):
            env_list[i] = env_list[i].split("=", 1)
            ENV_CACHE[env_list[i][0]] = env_list[i][1]
        
        return str(curTime - startTime) + "Initially loaded environment variables\n"
        


    elif sys.platform == "linux" or sys.platform == "linux2":
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
    if sys.platform == "darwin": # Mac OSX
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
                        
                        helpers.debugStringDiff(val, PROC_CACHE[key]) #comment/uncomment to debug string differences
                        
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


    @rtype List[tuple], List[tuple], List[tuple] : list of removed env vars, list of new env vars, list of updated env vars
    """
    if sys.platform == "darwin": # Mac OSX
        cmd = "printenv"
        env_find_process = os.popen(cmd)
        read_env_find = env_find_process.read()
        env_find_process.close()

        env_list = str(read_env_find).strip().split("\n")

        temp_dict = dict()

        env_rm = []
        env_cr = []
        env_up = []

        for i in range(len(env_list)):
            env_list[i] = env_list[i].split("=", 1)
            
            if env_list[i][0] in ENV_CACHE.keys():
                if env_list[i][1] != ENV_CACHE[env_list[i][0]]:
                    env_up.append((env_list[i][0], env_list[i][1]))
            else:
                env_cr.append((env_list[i][0], env_list[i][1]))

            temp_dict[env_list[i][0]] = env_list[i][1]
        
        to_remove = []

        for (k,v) in ENV_CACHE.items():
            if k not in temp_dict.keys():
                env_rm.append((k,v))
                to_remove.append(k)
        
        for k in to_remove:
            ENV_CACHE.pop(k)
        
        return env_rm, env_cr, env_up
            


    elif sys.platform == "linux" or sys.platform == "linux2":
        pass


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
    
    log_load_action = load_init_env_var(start)

    f.write(log_load_action)
    for (k,v) in ENV_CACHE.items():
        f.write("\t" + k + " : " + v + "\n")
    
    while(True):
        cur = time.time()
        curTime = str(time.time() - start)
        proc_rm, proc_cr, proc_up = update_proc()
        
        for p in proc_rm:
            f.write(curTime + " proc_rm " + p[0] + " : " + p[1] + "\n")
        
        for p in proc_cr:
            f.write(curTime + " proc_cr " + p[0] + " : " + p[1] + "\n")

        for p in proc_up:
            f.write(curTime + " proc_up " + p[0] + " : " + p[1] + "\n")
        

        env_rm, env_cr, env_up = update_env_var()

        for e in env_rm:
            f.write(curTime + " env_rm " + p[0] + "=" + p[1] + "\n")
        
        for e in env_cr:
            f.write(curTime + " env_cr " + p[0] + "=" + p[1] + "\n")

        for e in env_up:
            f.write(curTime + " env_up" + p[0] + "=" + p[1] + "\n")

        print("Took {} ms".format(str(time.time() - cur)))
        time.sleep(60)




