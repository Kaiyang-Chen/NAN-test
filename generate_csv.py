import numpy as np 
import os
import csv
import random

datapath = '/home/lss/Desktop/cky/NAN_test/Conrad Dataset'
file_haeader = ["subject","template","feature_path"]
csvTrain = open("train.csv", "w")
writer_train = csv.writer(csvTrain)
csvTest = open("test.csv", "w")
writer_test = csv.writer(csvTest)
persons = os.listdir(datapath)
writer_test.writerow(file_haeader)
writer_train.writerow(file_haeader)
for person in persons:
    templates = os.listdir(person)
    train_head = 0
    test_head = 0
    train_speak = 0
    test_speak = 0
    for template in templates:
        
        if (template[0:3] == "head"):
            if((random.random()<0.33 & test_head < 1) | train_head == 2):
                test_head =  test_head + 1
                frames = os.listdir(template)
                for frame in frames:
                    feature_path = os.path.join(datapath,person,template,frame)
                    tmp = [person,template,feature_path]
                    writer_test.writerow(tmp)
            else:
                train_head = train_head + 1
                frames = os.listdir(template)
                for frame in frames:
                    feature_path = os.path.join(datapath,person,template,frame)
                    tmp = [person,template,feature_path]
                    writer_train.writerow(tmp)
        else:
            if((random.random()<0.3 & test_speak < 3) | train_speak == 7):
                test_speak =  test_speak + 1
                frames = os.listdir(template)
                for frame in frames:
                    feature_path = os.path.join(datapath,person,template,frame)
                    tmp = [person,template,feature_path]
                    writer_test.writerow(tmp)
            else:
                train_head = train_head + 1
                frames = os.listdir(template)
                for frame in frames:
                    feature_path = os.path.join(datapath,person,template,frame)
                    tmp = [person,template,feature_path]
                    writer_train.writerow(tmp)
__