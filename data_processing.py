# convert fasta files into usable dataset file
import sys

# -*- coding: utf-8 -*-

import Bio.SeqIO as SeqIO
from utils_tools.Msa_Create_Embedding import *


filename_list=['test_set.fasta', 'target_list.txt', 'data_list.txt',
               'kingdom_list.txt', 'aa_list.txt']
msa_dir = None

target_list=[]
data_list=[]
kingdom_list=[]

def usage():
    print('Usage: python data_processing.py [fasta_file] or python data_processing.py [fasta_file] [msa_dir/]')
    print('msa_dir: directory of msa files, if not provided, msa embedding will not be created')
    print('MSA files in the directory should be names as 1.a3m, 2.a3m, 3.a3m, ..., in numerical order')
    print('The order of msa files should be the same as sequences in fasta file')

def main():

    outf1= open(filename_list[1], 'w')
    outf2 = open(filename_list[2], 'w')
    outf3 = open(filename_list[3], 'w')
    outf4 = open(filename_list[4], 'w')

    count=0

    data_list = []
    aa_list=[]
    target_list = []
    kingdom_list = []
    for record in SeqIO.parse(filename_list[0], "fasta"):

        half_len = int(len(record) / 2)

        sequence = str(record.seq[:half_len])
        ann_sequence = str(record.seq[half_len : int(len(record))])


        feature_parts = record.id.split("|")
        (uniprot_id, kingdom, sp_type) = feature_parts

        data_list.append((sequence))
        aa_list.append((ann_sequence))
        kingdom_list.append(kingdom)
        target_list.append(sp_type)

    print("Sum:")
    print(len(data_list))
    print(len(aa_list))
    print(len(kingdom_list))
    print(len(target_list))

    for target in target_list:
        outf1.write(target)
        outf1.write('\n')

    for data in data_list:
        outf2.write(data)
        outf2.write('\n')

    for kingdom in kingdom_list:
        outf3.write(kingdom)
        outf3.write('\n')

    for aa in aa_list:
        outf4.write(aa)
        outf4.write('\n')

    outf1.close()
    outf2.close()
    outf3.close()
    outf4.close()

    #create msa embedding
    if msa_dir is not None:
        createDatasetEmbedding(msa_dir, "test_feature.npy")


try:
    #read file names if provided

    if len(sys.argv) == 2:
        filename_list[0] = sys.argv[1]
    elif len(sys.argv) == 3:
        msa_dir = sys.argv[2]
    elif len(sys.argv) > 3:
        usage()
        sys.exit(1)
    main()


except IndexError:
    usage()