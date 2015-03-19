#coding=utf-8
import sys,copy
from pt4_filereader import Pt4FileReader

class Pt4Out(file):
    def __init__(self, file):
        """power monitor的固定采样频率是5000Hz，测试中为了避免不必要的数据运算，采用100Hz的频率进行计算"""
        self.curlist5000 = []
        for smpl in Pt4FileReader.readAsVector(file):
            #print smpl[2].mainCurrent
            self.curlist5000.append(smpl[2].mainCurrent)
        self.curlist100 = [self.curlist5000[i] for i in range(len(self.curlist5000)) if i%50 == 0]
        #print self.curlist100

    def pt4getAveCur(self, sec):
        """取得 n 秒后的平均电流
            sec - 从给定的时间之后开始计算该点到文件末尾的平均电流
        """
        return "%.2f" % sum(self.curlist100[int(sec)*100:])/(self.curlist100.__len__() - int(sec)*100)
    
    def pt4getAveHighThan(self, curbase):
        """在电流值高过某个值之后就开始计算平均电流
            curbase - 给定的开始记录的门槛值，取高于门槛值的点到文件末尾部分的电流平均值
        """
        for cur in self.curlist100:
            if cur > int(curbase):
                pos = self.curlist100.index(cur)
                return "%.2f" % sum(self.curlist100[pos:])/(self.curlist100.__len__() - pos)
        return -1
    
    def pt4getAveLessThan(self, curbase):
        """在电流值高过某个值之后就开始计算平均电流
            curbase - 给定的开始记录的门槛值，取低于门槛值的点到文件末尾部分的电流平均值
        """
        for cur in self.curlist100:
            if cur < int(curbase):
                pos = self.curlist100.index(cur)
                return "%.2f" % (sum(self.curlist100[pos:])/(self.curlist100.__len__() - pos))
        return -1
    
    def pt4getSleepCurNoPeak(self, curbase, duration, startpos=0):
        return -1
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {0} <pt4-file>".format(sys.argv[0]))
        sys.exit(1)
    
    sec = 0
    if len(sys.argv) == 3:
        sec = sys.argv[2]
    result = Pt4Out(sys.argv[1]).pt4getAveLessThan(sec)
    print result
    
