#coding=utf-8
import sys
from pt4_filereader import Pt4FileReader

class Pt4Out(file):
    def __init__(self, file):
        """power monitor的固定采样频率是5000Hz，测试中为了避免不必要的数据运算，采用100Hz的频率进行计算"""
        self.curlist5000 = []
        for smpl in Pt4FileReader.readAsVector(file):
            #print smpl[2].mainCurrent
            self.curlist5000.append(smpl[2].mainCurrent)
        self.curlist100 = [self.curlist5000[i] for i in range(len(self.curlist5000)) if i%50 == 0]
        print self.curlist100

    def pt4getAveCur(self, sec):
        """取得 n 秒后的平均电流"""
        sublist = self.curlist100[100*sec:]
        return sum(sublist)/len(sublist)
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {0} <pt4-file>".format(sys.argv[0]))
        sys.exit(1)
    
    sec = 0
    if len(sys.argv) == 3:
        sec = sys.argv[2]
    result = Pt4Out(sys.argv[1]).pt4getAveCur(sec)
    print result
    
