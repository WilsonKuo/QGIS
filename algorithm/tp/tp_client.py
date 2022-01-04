#!/bin/python3.6
from multiprocessing.managers import SyncManager
import sys, time

class MyManager(SyncManager):
    pass

MyManager.register("syncdict")

if __name__ == "__main__":
    manager = MyManager(("127.0.0.1", 5000), authkey=b'abc')
    manager.connect()
    syncdict = manager.syncdict()
    for key, value in syncdict.items():
        print(key, value)