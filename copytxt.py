import numpy as np 
import os
import csv
import random

datapath = '/home/lss/Desktop/cky/NAN-test/Conrad Dataset'

for person in persons:
    person_dir = os.path.join(datapath,person,"video")
    person_feature = os.path.join(datapath,person,"feature")
    cmd = 'mkdir ' + person_feature
    os.system(cmd)
    templates = os.listdir(person_dir)
    for template in templates:
        template_dir = os.path.join(person_dir,template)
        feature_dir = os.path.join(person_feature,template)
        cmd = 'mkdir ' + feature_dir
        os.system(cmd)
        frames = os.listdir(template_dir)
        for frame in frames:
            des = os.path.join(feature_dir,frame)
            feature_path = os.path.join(template_dir,frame)
            if(frame[-4:0] == ".txt"):
                cmd = 'mv '+ feature_path + ' ' + des
                os.system(cmd)

            