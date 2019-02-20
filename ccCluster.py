#! /usr/bin/env python
from __future__ import print_function

__author__ = "Gianluca Santoni"
__copyright__ = "Copyright 20150-2018"
__credits__ = ["Gianluca Santoni, Alexander Popov"]
__license__ = ""
__version__ = "0.2"
__maintainer__ = "Gianluca Santoni"
__email__ = "gianluca.santoni@esrf.fr"
__status__ = "Beta"




#from PyQt4 import QtGui, QtCore
import matplotlib.pyplot as plt
import sys
sys.path.append('/usr/lib/python2.7/dist-packages/')
#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar



# implement the default mpl key bindings
from scipy.cluster import hierarchy
import collections
import operator


from time import sleep
import os


from resultsTab import resultsTab
from summary import resultsSummary
from clustering import Clustering


# Insert parse  to change the file path from command line

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i","--DISTfile", dest="DISTfile", default=None, help="Distance file from ccCalc module")
parser.add_argument("-o","--outname", dest="outname", default='Dendrogram', help="output dendogram file name")
parser.add_argument("-t", "--threshold", dest="threshold", help="Distance threshold for clustering")
parser.add_argument("-p", "--process",action="store_true", dest="shell", default=False, help="Launch program in shell mode. Need to specify the threshold value")
parser.add_argument("-c", "--count",action="store_true", dest="count", default=False, help="Counts datasets in the biggest cluster and exit")
parser.add_argument("-e", "--estimation",action="store_true", dest="est", default=False, help="Tries to guess an optimal threshold value")
parser.add_argument("-u", dest="cell", default= False , action="store_true" , help='Unit cell based clustering. requires list of input files')
#Minimal for completeness is currently broken
#parser.add_argument("-m", dest="minimal", default= False , action="store_true" , help='Gives minimal threshold for completeness')


#parser.print_help()
args= parser.parse_args()

#Startup message

print("""ccCluster - HCA for protein crystallography 
G. Santoni and A. Popov, 2015
              v .   ._, |_  .,
           `-._\/  .  \ /    |/_
               \\  _\, y | \//
         _\_.___\\, \\/ -.\||
           `7-,--.`._||  / / ,
           /'     `-. `./ / |/_.'
                     |    |//
                     |_    /
                     |-   |
                     |   =|
                     |    |
--------------------/ ,  . \--------._
""")


#this part is commented out to separate ccCluster from ccCalc
# if args.DISTfile is None:
#     if args.HKLlist is None:
#         print('No input specified, calculating Correlation coefficients')
#         print('this might take a while')
#         CalcClass.ccCalc()
#         correlationFile='ccClusterLog.txt'
#     elif args.cell:
#         print("Calculating unit cell distance between specified files")
#         CalcClass.cellList(args.HKLlist)
#         correlationFile='ccClusterLog.txt'
#     else:
#         print("Calculating CC between specified files")
#         CalcClass.ccList(args.HKLlist)
#         correlationFile='ccClusterLog.txt'
# else:
#     correlationFile=args.DISTfile


#Suggest to run ccCalc if no correlation file is provided
if args.DISTfile is None:
    print('no inputs specified, please run ccCalc before')
else:
    correlationFile=args.DISTfile


CC = Clustering(correlationFile)
Tree = CC.avgTree()
etiquets=CC.createLabels()
threshold = CC.thrEstimation()




# #Main part of the program
# #with the different options, we can chose 
# # to process through the shell,
# #count the multiplicity of the highest cluster
# #run the interface

def main():
    if args.threshold:
        threshold = args.threshold
    else:
        threshold= CC.thrEstimation()

    if args.shell:
        CC.checkMultiplicity(threshold)
        CC.merge('ano',threshold)
        CC.flatClusterPrinter(threshold, etiquets, 'ano')        
    elif args.count:
        CC.checkMultiplicity(threshold)
    elif args.est:
        a = CC.thrEstimation()
        print(a)
    # else:
    #     app = QtGui.QApplication(sys.argv)
    #     ex = MainWindow()
    #     ex.show()
    #     sys.exit(app.exec_())      

if __name__== '__main__':
    main()
