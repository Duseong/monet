#! /naqfc/noscrub/Barry.Baker/anaconda2/bin/python


###for aitken replace the first line with /data/aqf/barryb/anaconda2/bin/python for the line above

import verify
from glob import glob
import matplotlib.pyplot as plt
import sys

print "Name of Script: ", sys.argv[0]
print "ACONC FILE: ", sys.argv[1]
print "GRIDCRO2D FILE: ", sys.argv[2]
print "LABEL: ", sys.argv[3]
print "AIRNOW Username: ", sys.argv[4]
print "AIRNOW Password: ", sys.argv[5]
print "OUTPUT FILENAME: ", sys.argv[6]

files = glob(sys.argv[1])
grid = sys.argv[2]

va = verify.verify_airnow(concpath=files,gridcro=grid,datapath='.',user=sys.argv[4],passw=sys.argv[5],combine=True,neighbors=9)

for i in va.df.Region.dropna().unique():
  

va.compare_param(param='PM2.5',timeseries=True,label=sys.argv[3])
plt.savefig('pm25_' + sys.argv[6],dpi=100)
plt.close()

va.compare_param(param='OZONE',timeseries=True,label=sys.argv[3])
plt.savefig('o3_' + sys.argv[6],dpi=100)
plt.close()
