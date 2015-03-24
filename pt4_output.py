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
        #求1秒钟的平均电流做一次list，好处是减少后面不必要的计算
        self.curpersec = [sum(self.curlist5000[i*5000:(i+1)*5000])/5000 for i in range(len(self.curlist5000)/5000)]
        #print self.curlist100

    def pt4getAveCur(self, sec):
        """取得 n 秒后的平均电流
            sec - 从给定的时间之后开始计算该点到文件末尾的平均电流
        """
        return "%.2f" % float(sum(self.curlist100[int(sec)*100:])/(self.curlist100.__len__() - int(sec)*100))

    def pt4getAveHighThan(self, curbase):
        """在电流值高过某个值之后就开始计算平均电流
            curbase - 给定的开始记录的门槛值，取高于门槛值的点到文件末尾部分的电流平均值
        """
        for cur in self.curlist100:
            if cur > int(curbase):
                pos = self.curlist100.index(cur)
                return "%.2f" % float(sum(self.curlist100[pos:])/(self.curlist100.__len__() - pos))
        return -1
    
    def pt4getAveLessThan(self, curbase):
        """在电流值高过某个值之后就开始计算平均电流
            curbase - 给定的开始记录的门槛值，取低于门槛值的点到文件末尾部分的电流平均值
        """
        for cur in self.curlist100:
            if cur < int(curbase):
                pos = self.curlist100.index(cur)
                return "%.2f" % float(sum(self.curlist100[pos:])/(self.curlist100.__len__() - pos))
        return -1
    
    def pt4getSleepCurNoPeak(self, curbase, duration, startpos=0):
        """从某个时间点起，电流低于一定数值，并且一直保持，在一定的时间段内没有跳变的平均电流
            curbase - 电流门槛值，如果startpos没有设置的话，从第一个小于该电流值的开始计算平均值
            duration - 统计区间的时常
            startpos - 强制指定跳过的时间长度，弱该项参数指定后，从指定点之后寻找符合curbase要求的点
        """
        curl = self.curpersec[:]
        length = len(curl)
        sum = curl.pop()
        ave = 0
        if startpos > 0:
            curl = self.curpersec[int(startpos):]
        for i in range(len(curl)):
            sec = curl.pop()
            if sec >= curbase:
                ave = sum/(i+1)
                return ave
            else:
                sum += sec
        ave = sum/(length + 1)
        return ave
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {0} <pt4-file>".format(sys.argv[0]))
        sys.exit(1)
    
    sec = 0
    if len(sys.argv) == 3:
        sec = sys.argv[2]
    result = Pt4Out(sys.argv[1]).pt4getAveLessThan(sec)
    print result
    
