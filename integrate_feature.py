import numpy as np 
import os
import csv
import scipy.io as sio

datapath = '/home/lss/Desktop/cky/NAN-test/Conrad Dataset'
persons = os.listdir(datapath)
for person in persons:
    
    person_feature = os.path.join(datapath,person,"feature")
    
    templates = os.listdir(person_feature)
    for template in templates:
        
        feature_dir = os.path.join(person_feature,template)
        des_dir = os.path.join(feature_dir,template+".txt")
        mat_dir = os.path.join(feature_dir,template+".mat")
        frames = os.listdir(feature_dir)
        for frame in frames:
            des = os.path.join(feature_dir,frame)
            feature_path = os.path.join(feature_dir,frame)
            
            des = open(des_dir,'a')
            with open(feature_path,'r') as filein:
                line = filein.readline()
                des.write(line)
            des.close()
        data = np.loadtxt(des_dir,skiprows=0)
        mdic = {'feat':data}
        sio.savemat(mat_dir,mdic)
    

            

