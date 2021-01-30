import os
import scipy.io as sio
import numpy as np
import pickle

def save(lst, path):
    with open(path, 'wb') as fp:
        pickle.dump(lst, fp)

def get_mat(feature_dir):
    arr = []
    item = sio.loadmat(feature_dir)
    arr.append(item['feat'])
    return arr

def get_train_test_set():
    data_dir_base = './Conrad Dataset'
    save_dir = './'
    train_dir = './'
    train_file = os.path.join(train_dir,'train.csv')
    cur_line = 0
    subs = []
    templates = []
    lst_train_faces = []
    for line in open(train_file):
        cur_line += 1
        if(cur_line == 1):
            continue
        lst_tmp = line.split(',')
        template_id = lst_tmp[1]
        subject_id = lst_tmp[0]
        fearture_dir = os.path.join(data_dir_base,subject_id,"feature",template_id,template_id,".mat")
        template_id = subject_id + "/" + template_id

        if templates.count(template_id) == 0:
            templates.append(template_id)
            if subs.count(subject_id) == 0:
                subs.append(subject_id)
                lst_train_faces.append([])
            idx = subs.index(subject_id)

            arr = get_mat(fearture_dir)
            if len(lst_train_faces[idx]) == 0:
                lst_train_faces[idx] = arr
            else:
                lst_train_faces[idx] = np.vstack([lst_train_faces[idx], arr])

    save(lst_train_faces, os.path.join(save_dir, 'train_subject.bin'))
    print('#train subject {}'.format(len(lst_train_faces)))



if __name__ == '__main__':
    get_train_test_set()