import numpy as np 
import os
import csv
import scipy.io as sio
import random
import codecs

datapath = '/home/lss/Desktop/cky/NAN-test/FDDB_feature'
persons = os.listdir(datapath)

for person in persons:
    
    person_feature = os.path.join(datapath,person)
    
    templates = os.listdir(person_feature)
    for template in templates:
        feature_dir = os.path.join(person_feature,template)
        des_dir = os.path.join(feature_dir,template+".txt")
        #print(des_dir)
        if os.path.exists(des_dir):
            os.remove(des_dir)
            print("delete "+des_dir)
        #print(len(open(des_dir,'rU').readlines()))
        mat_dir = os.path.join(feature_dir,template+".mat")
        if os.path.exists(mat_dir):
            os.remove(mat_dir)
        frames = os.listdir(feature_dir)
        num_frames = len(frames)
        start = random.randint(0,num_frames-65)
        count = 0
        a = 0
        frames.sort(key = lambda x: int(x[:-8]))
        for frame in frames:
            if(count >= start and (a < 65)):
                if a>=65:
                    break
                feature_path = os.path.join(feature_dir,frame)
                #print(feature_path)
                des = open(des_dir,'a')
                with codecs.open(feature_path,'r', encoding='utf-8', errors='ignore') as filein:
                    line = filein.readline()
                    if len(line)>10000:
                        des.write(line)
                        a = a+1
                        #print(frame)
                des.close()
            count += 1
        data = np.loadtxt(des_dir,skiprows=0)
        print(data)
        mdic = {'feat':data}
        sio.savemat(mat_dir,mdic)

