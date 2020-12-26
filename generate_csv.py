import numpy as np 
import os
import csv
import random

datapath = '/home/lss/Desktop/cky/NAN-test/Conrad Dataset'
file_haeader = ["subject","template","feature_path"]
csvTrain = open("train.csv", "w")
writer_train = csv.writer(csvTrain)
csvTest = open("test.csv", "w")
writer_test = csv.writer(csvTest)
persons = os.listdir(datapath)
writer_test.writerow(file_haeader)
writer_train.writerow(file_haeader)
for person in persons:
    person_dir = os.path.join(datapath,person)
    templates = os.listdir(person_dir)
    train_head = 0
    test_head = 0
    train_speak = 0
    test_speak = 0
    for template in templates:
        
        if (template[0:3] == "head"):
            if((random.random()<0.33 and test_head < 1) or train_head == 2):
                test_head =  test_head + 1
                template_dir = os.path.join(person_dir,template,'video')
                frames = os.listdir(template_dir)
                for frame in frames:
                    feature_path = os.path.join(datapath,person,template,frame)
                    tmp = [person,template,feature_path]
                    writer_test.writerow(tmp)
            else:
                train_head = train_head + 1
                template_dir = os.path.join(person_dir,template,'video')
                frames = os.listdir(template_dir)
                for frame in frames:
                    feature_path = os.path.join(datapath,person,template,frame)
                    tmp = [person,template,feature_path]
                    writer_train.writerow(tmp)
        else:
            if((random.random()<0.3 and test_speak < 3) or train_speak == 7):
                test_speak =  test_speak + 1
                template_dir = os.path.join(person_dir,template,'video')
                frames = os.listdir(template_dir)
                for frame in frames:
                    feature_path = os.path.join(datapath,person,template,frame)
                    tmp = [person,template,feature_path]
                    writer_test.writerow(tmp)
            else:
                train_head = train_head + 1
                template_dir = os.path.join(person_dir,template,'video')
                frames = os.listdir(template_dir)
                for frame in frames:
                    feature_path = os.path.join(datapath,person,template,frame)
                    tmp = [person,template,feature_path]
                    writer_train.writerow(tmp)
__