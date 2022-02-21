from PyQt5.QtCore import QThread, QMutex
import time

def test():
    print(1)

class WorkThread(QThread):
    def __int__(self):
        # 初始化函数
        super(WorkThread, self).__init__()
        print(dir(self))
        self.qmutex = QMutex()
        print(self.qmutex)
    def setfunc(self, function):
        self.function = function
    def run(self):
        #print(dir(self))
        #self.qmutex.lock()
        while True:
            print(self.function)
            pass
        #self.qmutex.unlock()
        

if __name__ == "__main__":
    workthread = WorkThread()
    workthread.setfunc(test)
    workthread.start()

