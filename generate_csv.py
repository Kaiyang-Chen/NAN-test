import numpy as np 
import os
import csv
import random

datapath_train = '/home/lss/Desktop/cky/NAN-test/FDDB_feature'
file_haeader = ["subject","template","feature_path"]
csvTrain = open("train_fddb.csv", "w")
writer_train = csv.writer(csvTrain)
persons = os.listdir(datapath_train)
writer_train.writerow(file_haeader)
for person in persons:
    feature_dir = os.path.join(datapath_train,person)
    templates = os.listdir(feature_dir)
    # train_head = 0
    # test_head = 0
    # train_speak = 0
    # test_speak = 0
    for template in templates:
        template_dir = os.path.join(feature_dir,template)
        frames = os.listdir(template_dir)
        tmp = [person,template,template_dir]
        writer_train.writerow(tmp)
datapath_test = '/home/lss/Desktop/cky/NAN-test/Conrad Dataset'
file_haeader = ["subject","template","feature_path"]
csvTest = open("test_CD.csv", "w")
writer_test = csv.writer(csvTest)
persons = os.listdir(datapath_test)
writer_test.writerow(file_haeader)
num_objects = len(persons)
count = 0
for person in persons:
    feature_dir = os.path.join(datapath_test,persons[count],'feature')
    templates = os.listdir(feature_dir)
    for i in range(5):
        idx_diff = random.randint(0,len(persons)-1)
        if(idx_diff == count):
            idx_diff = (idx_diff+3)%len(persons)
        diff_path = feature_dir = os.path.join(datapath_test,persons[idx_diff],'feature')
        diff_tem = os.listdir(diff_path)
        idx_a = random.randint(0,len(templates)-1)
        diff_dir = os.path.join(datapath_test,persons[idx_diff],'feature',diff_tem[(idx_a+1)%len(diff_tem)],diff_tem[(idx_a+1)%len(diff_tem)]+'.mat')
        if not os.path.exists(diff_dir):
            print(diff_dir)
            print("ddd")

        template_dir_a = os.path.join(datapath_test,persons[count],'feature',templates[idx_a],templates[idx_a]+'.mat')
        if not os.path.exists(template_dir_a):
            print(templates)
            print(template_dir_a) 
            print(persons[count])
            print(count)
            print(os.listdir(os.path.join(datapath_test,persons[count],'feature',persons[count],'feature')))     
            print("aaa")  
        idx_b = random.randint(0,len(templates)-1)
        if(idx_a == idx_b):
            idx_b = (idx_b+3)%len(templates)
        template_dir_b = os.path.join(datapath_test,persons[count],'feature',templates[idx_b],templates[idx_b]+'.mat')
        if not os.path.exists(template_dir_b):
            print(template_dir_b)
            print("bbb")
        is_same = True
        tmp = [template_dir_a,template_dir_b,is_same]
        writer_test.writerow(tmp)
        is_same = False
        tmp = [template_dir_a,diff_dir,is_same]
        writer_test.writerow(tmp)
    count += 1
        # if (template[0:3] == "head"):
        #     if((random.random()<0.33 and test_head < 1) or train_head == 2):
        #         test_head =  test_head + 1
        #         template_dir = os.path.join(feature_dir,template)
        #         frames = os.listdir(template_dir)
        #         for frame in frames:
        #             feature_path = os.path.join(template_dir,frame)
        #             tmp = [person,template,feature_path]
        #             writer_test.writerow(tmp)
        #     else:
        #         train_head = train_head + 1
        #         template_dir = os.path.join(feature_dir,template)
        #         frames = os.listdir(template_dir)
        #         for frame in frames:
        #             feature_path = os.path.join(template_dir,frame)
        #             tmp = [person,template,feature_path]
        #             writer_train.writerow(tmp)
        # else:
        #     if((random.random()<0.3 and test_speak < 3) or train_speak == 7):
        #         test_speak =  test_speak + 1
        #         template_dir = os.path.join(feature_dir,template)
        #         frames = os.listdir(template_dir)
        #         for frame in frames:
        #             feature_path = os.path.join(template_dir,frame)
        #             tmp = [person,template,feature_path]
        #             writer_test.writerow(tmp)
        #     else:
        #         train_head = train_head + 1
        #         template_dir = os.path.join(feature_dir,template)
        #         frames = os.listdir(template_dir)
        #         for frame in frames:
        #             feature_path = os.path.join(template_dir,frame)
        #             tmp = [person,template,feature_path]
        #             writer_train.writerow(tmp)
