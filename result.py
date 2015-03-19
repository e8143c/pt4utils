#!/usr/bin/env python
# -*- coding:utf-8 -*-
  
import csv
import sys
import os
import time
from pt4_output import Pt4Out

class resurt:	
	def csv(self,sec):
		BASE_DIR = os.path.dirname(__file__)
		print BASE_DIR
		csvfile = file(BASE_DIR+'\\result.csv', 'wb')
		writer = csv.writer(csvfile)
		writer.writerow(['测试case', '平均电流'])
		case_name=['test001Aptest','test002Video','test003Muisc','test005RecordVideo','test006Recorder','test007Camera','test009Reboot','test010Gallery','test011CreateContact','test012SearchContact']
		datadic = []
		print type(datadic)
		for i in range(len(case_name)):
			BASE_DIR = os.path.dirname(__file__)
			xjh = Pt4Out(BASE_DIR+'\\pt4\\'+case_name[i]+'.pt4')
			datadic.append([case_name[i],xjh.pt4getAveLessThan(sec)])
			#print case_name[i],xjh.pt4getAveLessThan(sec)
			writer.writerows(datadic)
		csvfile.close()
if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("add time,like:python xxx.py 10")
		sys.exit(1)
		sec = 0
	if len(sys.argv) == 2:
		sec = sys.argv[1]
	d = resurt()
	d.csv(sec)
