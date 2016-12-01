#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import os.path
import sys
import glob
import csv
import shutil

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

with open('.\\Result\\Combined_Data.csv','wb') as allcsvfile:
#begin
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
print('Congratulations! The combintion process is successfull!!!')     