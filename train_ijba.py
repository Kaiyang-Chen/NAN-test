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
set_size = 8 # size of image set
batch_size = 128 # number of subjects per batch
set_per_sub = 3 # number of image set per subject within a batch
pooling_type = 'NAN'
if feat_type == 'casianet':
    feat_dim = 320
else:
    feat_dim = 512

max_iter = 510
test_iter = 100

save_dir = './model_{}_s{}_{}'.format(feat_type, set_size, pooling_type)
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

logger = utils.config_log(save_dir, 'train_s{}b{}'.format(set_size, batch_size))
meta_dir = './'
logger_result = open(os.path.join(save_dir, 'eval_result.txt'), 'w')
NAN_split_tars = np.zeros((10, 4), dtype=np.float32)
AVE_split_tars = np.zeros((10, 4), dtype=np.float32)

lst_sub_faces = pickle.load(open(os.path.join(meta_dir, 'train_subject.bin'.format(idx_split)), 'rb'))
dataset = read_utils.Dataset(lst_sub_faces, batch_size, set_size)
net = model_utils.Pooling_Classifier(feat_dim=feat_dim, num_classes=len(lst_sub_faces), pooling_type=pooling_type)
criterion = torch.nn.CrossEntropyLoss()
contrastive_criterion = model_utils.Online_Contrastive_Loss(num_classes=len(lst_sub_faces))
# optimizer_nn = optim.Adam(net.parameters(), weight_decay=5e-5)
optimizer_nn = optim.RMSprop(net.parameters(), lr=0.001, weight_decay=1e-5)

lst_tar = []
for iter in range(max_iter):
    iter += 1
    batch, lst_label, lst_len = dataset.next_pair_batch(set_per_sub)
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
    loss = loss_contrastive + 0.0*loss_sf
    _, predicted = torch.max(logits.data, 1)
    accuracy = (targets.data == predicted).float().mean()

    optimizer_nn.zero_grad()
    loss.backward()
    if iter > 2:
        optimizer_nn.step()

           
    # end of training
np_lst_tar = np.vstack(lst_tar)
idx_max = np.argmax(np_lst_tar[:, 1])
    


