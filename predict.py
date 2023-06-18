import os
import torch as torch
import numpy as np
from utils_tools.utils import *

dic = {'NO_SP': 0, 'SP': 1, 'LIPO': 2, 'TAT': 3, 'TATLIPO' : 4, 'PILIN' : 5}
dic2 = {0: 'NO_SP', 1: 'SP', 2: 'LIPO', 3: 'TAT', 4: 'TATLIPO', 5: 'PILIN'}
kingdom_dic = {'EUKARYA':0, 'ARCHAEA':1, 'POSITIVE':2, 'NEGATIVE': 3}

def trans_data(str1, padding_length):
    # 对氨基酸进行编码转换
    a = []
    trans_dic = {'A':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'K':9,'L':10,'M':11,'N':12,'P':13,'Q':14,'R':15,'S':16,'T':17,'V':18,'W':19,'Y':20,'X':0}
    for i in range(len(str1)):
        if (str1[i] in trans_dic.keys()):
            a.append(trans_dic.get(str1[i]))
        else:
            print("Unknown letter:" + str(str1[i]))
            a.append(trans_dic.get('X'))
    while(len(a)<padding_length):
        a.append(0)

    return a

def trans_label(str1):
    # 对标签进行编码转换
    if((str1) in dic.keys()):
        a = dic.get(str1)
    else:
        print(str1)
        raise Exception('Unknown category!')

    return a

def createTestData(data_path='./test_data/data_list.txt',
                    kingdom_path='./test_data/kingdom_list.txt',
                   maxlen=70, test_path="./embedding/test_feature.npy"
                   ):
    # 初始化
    data_list = []
    kingdom_list=[]
    raw_data=[]
    # 加载数据
    with open(data_path, 'r') as data_file:
        for line in data_file:
            str = np.array(trans_data(line.strip('\n')[0:70], maxlen))
            data_list.append(str)

    with open(data_path, 'r') as data_file:
        for line in data_file:
            str = line.strip('\n\t')[0:70]
            raw_data.append(("protein", str))

    features = np.load(test_path)

    with open(kingdom_path, 'r') as kingdom_file:
        for line in kingdom_file:
            if line.strip('\n\t') not in kingdom_dic.keys():
                kingdom_list.append(np.eye(len(kingdom_dic.keys()))[kingdom_dic['NEGATIVE']])#Take seqs without group info as negative
            else:
                kingdom_list.append(np.eye(len(kingdom_dic.keys()))[kingdom_dic[line.strip('\n\t')]])

    count = 0


    data_file.close()
    kingdom_file.close()

    X = np.array(data_list)
    kingdoms= np.array(kingdom_list)

    X = np.concatenate((X,kingdoms, features), axis=1)
    return X

def trans_output(str1):
    # 对标签进行编码转换
    if((str1) in dic2.keys()):
        a = dic2.get(str1)
    else:
        print(str1)
        raise Exception('Unknown category!')

    return a

if __name__ == '__main__':
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    model = torch.load("USPNet_model.pth", map_location=device)

    model_ = model
    if isinstance(model, torch.nn.DataParallel):
        # access the model inside the DataParallel wrapper
        model = model.module
    model = model.to(device)

    filename_list = ["data_list.txt",
                     "kingdom_list.txt",
                     "test_feature.npy",
                     "results.txt",
                     "aa_results.txt",
                     "cleavage_results.txt"
                     ]

    X_test = createTestData(data_path=filename_list[0],
                            kingdom_path=filename_list[1],
                            test_path=filename_list[2])
    output = []
    output_aa = []
    X_test = torch.tensor(X_test)
    test_loader = torch.utils.data.DataLoader(X_test, batch_size=256)
    for i, input in enumerate(test_loader):
        input = input.cuda()
        o1, o_aa = model(input)
        output.extend(o1.cpu().detach().numpy())
        output_aa.extend(o_aa.cpu().detach().numpy())
    output = torch.tensor(np.array(output))
    results = pred(output).cpu().detach().numpy()
    output_aa = torch.argmax(torch.tensor(np.array(output_aa)), dim=2).reshape(-1, 1)
    results_aa = output_aa.cpu().detach().numpy()
    output_aa_ = results_aa.reshape(-1, 70).copy()

    indexes_ = np.where(output_aa_ == 1)
    output_aa_[indexes_] = 100

    indexes_1 = np.where(output_aa_ == 3)
    indexes_2 = np.where(output_aa_ == 0)

    output_aa_[indexes_1] = 1
    output_aa_[indexes_2] = 1

    indexes_0 = np.where(output_aa_ != 1)
    output_aa_[indexes_0] = 0
    indexes_pos = np.where(output_aa_ == 1)

    outf1 = open(filename_list[3], 'w')
    for result in results:
        outf1.write(trans_output(result))
        outf1.write('\n')
    outf1.close()


    outf2 = open(filename_list[4], 'w')
    for result in output_aa_:
        for aa in result:
            outf2.write(str(aa))
        outf2.write('\n')
    outf2.close()
    indexes1= indexes_pos[0].copy().tolist()
    indexes2 = indexes_pos[1].copy().tolist()


    outf3 = open(filename_list[5], 'w')
    count = 0
    data_list = []
    with open(filename_list[0], 'r') as data_file:
        for line in data_file:
            data_list.append(line.strip('\n'))
    data_file.close()
    for result in results:
        if result==0:
            outf3.write('\n')
        else:
            try:
                index = indexes1.index(count)
            except:
                outf3.write(data_list[count])
            else:
                index = indexes1.index(count)
                index2 = indexes2[index]
                sq=data_list[count]
                outf3.write(sq[:index2+1])
            outf3.write('\n')
        count = count + 1
    outf3.close()