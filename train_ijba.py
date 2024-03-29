import torch
import utils
import os
import model_utils
import pickle
import read_utils
import torch.optim as optim
import numpy as np
import sklearn.metrics.pairwise as skp
import eval_ijba

K = 1 # [optional] to eliminate too small templates while testing
margin = 2.0 # follow the original paper
feat_type = 'resnet34' # casianet or resnet34
set_size = 65 # size of image set
batch_size = 8 # number of subjects per batch
set_per_sub = 3 # number of image set per subject within a batch
pooling_type = 'NAN'
if feat_type == 'casianet':
    feat_dim = 320
else:
    feat_dim = 512

max_iter = 51000
test_iter = 100

save_dir = './model_{}_s{}_{}'.format(feat_type, set_size, pooling_type)
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

logger = utils.config_log(save_dir, 'train_s{}b{}'.format(set_size, batch_size))
meta_dir = './'
logger_result = open(os.path.join(save_dir, 'eval_result.txt'), 'w')
NAN_split_tars = np.zeros((10, 4), dtype=np.float32)
AVE_split_tars = np.zeros((10, 4), dtype=np.float32)

lst_sub_faces = pickle.load(open(os.path.join(meta_dir, 'train_fddb.bin'), 'rb'))
test_sub_faces = pickle.load(open(os.path.join(meta_dir, 'test_subject.bin'), 'rb'))
dataset = read_utils.Dataset(lst_sub_faces, batch_size, set_size)
testset = read_utils.Dataset(test_sub_faces, batch_size, set_size)
net = model_utils.Pooling_Classifier(feat_dim=feat_dim, num_classes=len(lst_sub_faces), pooling_type=pooling_type)
criterion = torch.nn.CrossEntropyLoss()
contrastive_criterion = model_utils.Online_Contrastive_Loss(num_classes=len(lst_sub_faces))
# optimizer_nn = optim.Adam(net.parameters(), weight_decay=5e-5)
optimizer_nn = optim.RMSprop(net.parameters(), lr=0.001, weight_decay=1e-5)

lst_tar = []
for iter in range(max_iter):
    iter += 1
    batch, lst_label, lst_len = dataset.next_batch()
    batch = np.vstack(batch)
    # batch = skp.normalize(batch)
    lst_len = np.array(lst_len)
    lst_label = np.array(lst_label)

    batch = torch.from_numpy(batch).float()
    lst_len = torch.from_numpy(lst_len)
    targets = torch.from_numpy(lst_label).long()

    feats, logits = net(batch, lst_len)
    loss_sf = criterion(logits, targets)
    loss_contrastive = contrastive_criterion(feats, targets)
    loss = 0.0*loss_contrastive + loss_sf
    #print(logits.data)
    _, predicted = torch.max(logits.data, 1)
   # print(targets.data)
    #print(predicted)
    accuracy = (targets.data == predicted).float().mean()
    #print(accuracy)

    optimizer_nn.zero_grad()
    loss.backward()
    if iter > 2:
        optimizer_nn.step()
    #logger.info('iter {} loss {} accuracy {}'.format(iter, loss.data, accuracy.data))
    
    #test every iteration
    if iter % test_iter == 0 or iter == 1:
        lst_test_pair = pickle.load(open(os.path.join(meta_dir, 'lst_test_pair_CD.bin'), 'rb'))
        # cur_pair = 0
        # c_sim = np.zeros(shape=[len(lst_test_pair)], dtype=np.float32)
        # actual_issame = np.zeros(shape=[len(lst_test_pair)], dtype=np.bool)
        c_sim = []
        actual_issame = []
        for pair in lst_test_pair:
            vfea_a = pair[0]
            vfea_b = pair[1]
            if vfea_a.shape[0] < K or vfea_b.shape[0] < K:
                continue

            batch_a = torch.from_numpy(vfea_a).float()
            lst_len = torch.from_numpy(np.array([vfea_a.shape[0]]))
            feats, logits = net(batch_a, lst_len)
            mfeat_a = feats.detach().numpy()

            batch_b = torch.from_numpy(vfea_b).float()
            lst_len = torch.from_numpy(np.array([vfea_b.shape[0]]))
            feats, logits = net(batch_b, lst_len)
            mfeat_b = feats.detach().numpy()

            nfeat_a = eval_ijba.norm_l2(mfeat_a)
            nfeat_b = eval_ijba.norm_l2(mfeat_b)
            cos_d = np.dot(nfeat_b, np.transpose(nfeat_a))
            # c_sim[cur_pair] = cos_d
            issame = pair[2]
            #print(issame)
            # actual_issame[cur_pair] = issame
            c_sim.append(cos_d)
            actual_issame.append(issame)
            # cur_pair += 1
        # end of pair
        c_sim = np.array(c_sim)
        actual_issame = np.array(actual_issame)
        fars, tars, thrs, FA, TA, acc = eval_ijba.cal_far(c_sim, actual_issame)
        lst_tar.append(np.expand_dims(np.array(tars), axis=0))
        np_lst_tar = np.vstack(lst_tar)
        idx_max = np.argmax(np_lst_tar[:, 1])
            # print('# split {} pair {}'.format(idx_split, len(c_sim)))
        logger.info('iter {} loss {} loss_c {} accuracy {}'.format(iter, loss.data, loss_contrastive.data, accuracy.data))
        logger.info('cur tar {}'.format(tars))
        logger.info('max tar {}'.format(np_lst_tar[idx_max, :]))
        logger.info('\n')
    #batch_test, test_label, test_len = testset.next_batch()
    #batch_test = np.vstack(batch_test)
    # batch = skp.normalize(batch)
    #test_len = np.array(test_len)
    #test_label = np.array(test_label)

    #batch_test = torch.from_numpy(batch_test).float()
    #test_len = torch.from_numpy(test_len)
    #targets_test = torch.from_numpy(test_label).long()

    #feats_test, logits_test = net(batch_test, test_len)

    #_, predicted_test = torch.max(logits_test.data, 1)
    #print(targets_test.data)
    #print(predicted_test)
    #accuracy_test = (targets_test.data == predicted_test).float().mean()
    #print(accuracy_test)
    #logger.info('TEST iter {} loss {} accuracy {}'.format(iter, loss.data, accuracy_test.data))
           
    # end of training

    


