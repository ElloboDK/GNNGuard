import imp
import torch
# import sys
# sys.path.insert(0, '/n/scratch2/xz204/Dr37/lib/python3.7/site-packages')
from deeprobust.graph.targeted_attack import Nettack
from deeprobust.graph.utils import *
from deeprobust.graph.data import Dataset
import argparse
from deeprobust.graph.defense import * # GCN, GAT, GIN, JK, GCN_attack,accuracy_1
from tqdm import tqdm
import scipy
import numpy as np
from sklearn.preprocessing import normalize
import pickle


# parser = argparse.ArgumentParser()
# parser.add_argument('--seed', type=int, default=14, help='Random seed.')
# # cora and citeseer are binary, pubmed has not binary features
# parser.add_argument('--dataset', type=str, default='citeseer', choices=['cora', 'cora_ml', 'citeseer', 'polblogs', 'pubmed'], help='dataset')
# parser.add_argument('--ptb_rate', type=float, default=0.05,  help='pertubation rate')
# parser.add_argument('--modelname', type=str, default='GCN',  choices=['GCN', 'GAT','GIN', 'JK'])
# parser.add_argument('--defensemodel', type=str, default='GCNJaccard',  choices=['GCNJaccard', 'RGCN', 'GCNSVD'])
# parser.add_argument('--GNNGuard', type=bool, default=False,  choices=[True, False])
# parser.add_argument('--DPlabel', type=int, default=9,  help='0-10')

# args = parser.parse_args()
# args.cuda = torch.cuda.is_available()
# print('cuda: %s' % args.cuda)

SEED = 14
DATASET = 'citeseer'
GNNGUARD = False
MODELNAME = 'GCN'


device = "cpu"
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("You are running: %s" %device)

np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed(SEED)

data = Dataset(root='./Datasets/', name=DATASET)
adj, features, labels = data.adj, data.features, data.labels

if scipy.sparse.issparse(features)==False:
    features = scipy.sparse.csr_matrix(features)

"""set the number of training/val/testing nodes"""
idx_train, idx_val, idx_test = data.idx_train, data.idx_val, data.idx_test

"""add undirected edges, orgn-arxiv is directed graph, we transfer it to undirected closely following 
https://ogb.stanford.edu/docs/leader_nodeprop/# ogbn-arxiv
"""
adj = adj + adj.T
adj[adj>1] = 1


# Setup Surrogate model
surrogate = GCN_attack(nfeat=features.shape[1], nclass=labels.max().item()+1, n_edge=adj.nonzero()[0].shape[0],
                nhid=16, dropout=0, with_relu=False, with_bias=False, device=device, )
surrogate = surrogate.to(device)
surrogate.fit(features, adj, labels, idx_train, train_iters=201)  # change this train_iters to 201: train_iters=201

# Setup Attack Model
target_node = 1104

model = Nettack(surrogate, nnodes=adj.shape[0], attack_structure=True, attack_features=False, device=device)
model = model.to(device)

def main():
    degrees = adj.sum(0).A1
    # How many perturbations to perform. Default: Degree of the node
    n_perturbations = int(degrees[target_node])
    # n_perturbations = 10

    print("n_perturbations: %s" %n_perturbations)

    # indirect attack/ influencer attack
    model.attack(features, adj, labels, target_node, n_perturbations, direct=True)
    modified_adj = model.modified_adj
    modified_features = model.modified_features

    # print(modified_adj)
    # print(modified_features)

    print('=== testing GNN on original(clean) graph ===')
    test(adj, features, target_node,  attention=GNNGUARD)

    print('=== testing GCN on perturbed graph ===')
    test(modified_adj, modified_features, target_node,attention=GNNGUARD)


def test(adj, features, target_node, attention=True):
    ''
    """test on GCN """
    """model_name could be 'GCN', 'GAT', 'GIN','JK'  """
    # for orgn-arxiv: nhid =256, layers =3, epoch =500

    gcn = globals()[MODELNAME](nfeat=features.shape[1], nhid=256, nclass=labels.max().item() + 1, dropout=0.5,
              device=device)
    gcn = gcn.to(device)
    gcn.fit(features, adj, labels, idx_train, idx_val=idx_val,
            idx_test=idx_test,
            attention=attention, verbose=True, train_iters=81)
    gcn.eval()
    _, output = gcn.test(idx_test=idx_test)

    probs = torch.exp(output[[target_node]])[0]
    print('probs: {}'.format(probs.detach().cpu().numpy()))
    acc_test = accuracy(output[idx_test], labels[idx_test])

    print("Test set results:",
          "accuracy= {:.4f}".format(acc_test.item()))
    return acc_test.item()


def multi_test():
    cnt = 0
    degrees = adj.sum(0).A1
    node_list = select_nodes(num_target=10)
    print(node_list)

    num = len(node_list)
    print('=== Attacking %s nodes respectively ===' % num)
    num_tar = 0
    for target_node in tqdm(node_list):
        n_perturbations = int(degrees[target_node])
        if n_perturbations <1:  # at least one perturbation
            continue

        model = Nettack(surrogate, nnodes=adj.shape[0], attack_structure=True, attack_features=False, device=device)
        model = model.to(device)
        model.attack(features, adj, labels, target_node, n_perturbations, direct=True, verbose=False)
        modified_adj = model.modified_adj
        modified_features = model.modified_features
        acc = single_test(modified_adj, modified_features, target_node)
        if acc == 0:
            cnt += 1
        num_tar += 1
        print('classification rate : %s' % (1-cnt/num_tar), '# of targets:', num_tar)

"""Set attention"""
attention = GNNGUARD

def single_test(adj, features, target_node):
    'ALL the baselines'

    # """defense models"""
    # classifier = globals()[args.defensemodel](nnodes=adj.shape[0], nfeat=features.shape[1], nhid=16,
    #                                           nclass=labels.max().item() + 1, dropout=0.5, device=device)

    # ''' test on GCN (poisoning attack), model could be GCN, GAT, GIN'''
    classifier = globals()[MODELNAME](nfeat=features.shape[1], nhid=16, nclass=labels.max().item() + 1, dropout=0.5, device=device)
    classifier = classifier.to(device)
    classifier.fit(features, adj, labels, idx_train,
                   idx_val=idx_val,
                   idx_test=idx_test,
                   verbose=False, attention=attention) #model_name=model_name
    classifier.eval()
    acc_overall, output =  classifier.test(idx_test, ) #model_name=model_name

    probs = torch.exp(output[[target_node]])
    acc_test, pred_y, true_y = accuracy_1(output[[target_node]], labels[target_node])
    print('target:{}, pred:{}, label: {}'.format(target_node, pred_y.item(), true_y.item()))
    print('Pred probs', probs.data)
    return acc_test.item()

"""=======Basic Functions============="""
def select_nodes(num_target = 10):
    '''
    selecting nodes as reported in nettack paper:
    (i) the 10 nodes with highest margin of classification, i.e. they are clearly correctly classified,
    (ii) the 10 nodes with lowest margin (but still correctly classified) and
    (iii) 20 more nodes randomly
    '''
    gcn = globals()[MODELNAME](nfeat=features.shape[1],
              nhid=16,
              nclass=labels.max().item() + 1,
              dropout=0.5, device=device)
    gcn = gcn.to(device)
    gcn.fit(features, adj, labels, idx_train, idx_test, verbose=True)
    gcn.eval()
    output = gcn.predict()
    degrees = adj.sum(0).A1

    margin_dict = {}
    for idx in tqdm(idx_test):
        margin = classification_margin(output[idx], labels[idx])
        acc, _, _ = accuracy_1(output[[idx]], labels[idx])
        if acc==0 or int(degrees[idx])<1: # only keep the correctly classified nodes
            continue
        """check the outliers:"""
        neighbours = list(adj.todense()[idx].nonzero()[1])
        y = [labels[i] for i in neighbours]
        node_y = labels[idx]
        aa = node_y==y
        outlier_score = 1- aa.sum()/len(aa)
        if outlier_score >=0.5:
            continue

        margin_dict[idx] = margin
    sorted_margins = sorted(margin_dict.items(), key=lambda x:x[1], reverse=True)
    high = [x for x, y in sorted_margins[: num_target]]
    low = [x for x, y in sorted_margins[-num_target: ]]
    other = [x for x, y in sorted_margins[num_target: -num_target]]
    other = np.random.choice(other, 2*num_target, replace=False).tolist()

    return other + high + low


if __name__ == '__main__':
    main()
    # multi_test()
