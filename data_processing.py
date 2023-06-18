# convert fasta files into usable dataset file
import sys

# -*- coding: utf-8 -*-

import Bio.SeqIO as SeqIO


filename_list=['test_set.fasta', 'target_list.txt', 'data_list.txt',
               'kingdom_list.txt', 'aa_list.txt']

target_list=[]
data_list=[]
kingdom_list=[]

def usage():
    print('Usage: python data_processing.py [fasta_file]')


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

try:
    #read file names if provided

    if len(sys.argv) == 2:
        filename_list[0] = sys.argv[1]
    main()


except IndexError:
    usage()