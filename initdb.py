import os
import pyautogui
import socket
from wy.redistools import *
from wy.mongotools import *


def create_redis_bat(curr_path):
    run_path = "%s//%s" % (curr_path,"redis.bat")
    if not os.path.exists(run_path):
        disk = curr_path[:2]
        with open("redis.bat","w",encoding="utf-8") as f:
            f.writelines(disk)
            f.write("\n")
            f.writelines("cd %s//redis" % curr_path)
            f.write("\n")
            f.writelines("redis-server.exe redis.windows.conf")
            f.write("\n")
    return  run_path

def create_mongo_bat(curr_path):
    run_path = "%s//%s" % (curr_path, "mongo.bat")
    if not os.path.exists(run_path):
        disk = curr_path[:2]
        with open("mongo.bat","w",encoding="utf-8") as f:
            f.writelines(disk)
            f.write("\n")
            f.writelines("cd %s//mongo//bin" % curr_path)
            f.write("\n")
            f.writelines("mongod --bind_ip 0.0.0.0 --maxConns 1000 --dbpath  %s\mongo\data\db" % curr_path)
            f.write("\n")
    return run_path
ef create_mongo_client_bat(curr_path):
    run_path = "%s//%s" % (curr_path, "mongo_client.bat")
    if not os.path.exists(run_path):
        disk = curr_path[:2]
        with open("mongo_client.bat","w",encoding="utf-8") as f:
            f.writelines(disk)
            f.write("\n")
            f.writelines("cd %s//mongo//bin" % curr_path)
            f.write("\n")
            f.writelines("mongo.exe")
            f.write("\n")
    return run_path

def run_cmd(cmdstr):
    # _sp = subprocess.Popen(cmdstr,shell=True)
    pyautogui.hotkey('winleft', 'r')
    pyautogui.typewrite(cmdstr, 0.001)
    pyautogui.press("enter")
def isrun_redis(ip):
    try:
        myrc = rc(ip, 6379, "mudman1979", 0).getclient()
        ks = myrc.keys("*")
        if len(ks) >= 0:
            flag = True
            print("redis ok")
        else:
            flag = False
            print("redis no")
    except:
        flag = False
        print("redis no")
    return flag

def isrun_mongo(ip):
    try:
        mc = mongo("mongodb://%s:27017" % ip).getclient("ctg")
        mc["run_ip"].update({"ip":ip},{"ip":ip},upsert=True)
        print("mongo ok")
        flag = True
    except:
        flag = False
        print("mongo no")
    return flag




def run(curr_path):
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    mongo_cmd = create_mongo_bat(curr_path)
    create_mongo_client_bat(curr_path)
    if not isrun_mongo(ip):
        run_cmd(mongo_cmd)
    print("mongo run_at: %s:27017" % ip)


if __name__ == "__main__":
    run(os.getcwd())
