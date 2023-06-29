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
