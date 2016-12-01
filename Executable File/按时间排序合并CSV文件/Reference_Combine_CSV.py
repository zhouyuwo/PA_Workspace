#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import os.path
import sys
import glob
import csv
import shutil
import numpy 
import time

start = time.clock()

txtfilenames=[] 
path = '.\\'

if os.path.exists('.\\Result'):
	shutil.rmtree('.\\Result')
	os.makedirs('.\\Result')
else:
	os.makedirs('.\\Result')

for dirpath,dirnames,filenames in os.walk(path): 
	filenames = filter(lambda filename:filename[-4:]=='.csv',filenames) 
	filenames = map(lambda filename:os.path.join(dirpath,filename),filenames) 
	txtfilenames.extend(filenames)

#由于csv中有非数字数据，因此不能使用numpy进行处理	
with open('.\\Result\\temp.csv','wb') as allcsvfile:
	writer = csv.writer(allcsvfile)
	for filename in txtfilenames:
		#begin
		try:
			with open(filename,'rb') as csvfile:
			#begn
				reader = csv.reader(csvfile)
				column = [row[1] for row in reader]
				writer.writerow(column)
			#end
		except Exception,e:  
			print Exception,":",e
		#end
	csvfile.close()
	allcsvfile.close()
	
data_matrix = numpy.loadtxt(open(".\\Result\\temp.csv","rb"),delimiter=",",skiprows=0) 
zip_data_matrix= zip(*data_matrix)
numpy.savetxt('.\\Result\\Combined_Data.csv', zip_data_matrix, delimiter = ',') 
numpy.save('.\\Result\\Combined_Data_CW.npy',zip_data_matrix)
os.remove(".\\Result\\temp.csv")

end = time.clock()
print('*********** Congratulations! The combintion process is successfull!!! **********')
print('**************************** Runtime: %fs ********************************') % (end - start)