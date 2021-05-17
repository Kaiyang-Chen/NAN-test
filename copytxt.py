import numpy as np 
import os
import csv
import random

datapath = '/home/lss/Desktop/cky/NAN-test/FDDB'
datapath1 = '/home/lss/Desktop/cky/NAN-test/FDDB_feature'

persons = os.listdir(datapath)
for person in persons:
    person_dir = os.path.join(datapath,person)
    person_feature = os.path.join(datapath1,person)
    cmd = 'mkdir ' + person_feature
    #os.system(cmd)
    #templates = os.listdir(person_dir)
    #for template in templates:
    template = "r_3"
    template_dir = os.path.join(person_dir,template)
    feature_dir = os.path.join(person_feature,template)
    if not os.path.exists(feature_dir):
        os.makedirs(feature_dir)
    frames = os.listdir(template_dir)
    for frame in frames:
        des = os.path.join(feature_dir,frame)
            
        feature_path = os.path.join(datapath,person,template,frame)
        #print(frame[-1])
        if(frame[-1] == "t"):
            cmd = 'mv '+ feature_path + ' ' + feature_dir
            print(cmd)
            os.system(cmd)
