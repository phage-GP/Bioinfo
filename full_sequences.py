#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import time


with open('./sample_list.txt','r') as f:
    sample_list = [sample.replace('\n','') for sample in f]

FQ_1 = [ ]
FQ_2 = [ ]

A_list = [ ]                # alignments.vdjca
Clna = []                   # clones.clna
Clns = [ ]                   # full_clones.clns
full_clo = []               # full_clones.txt

Report1 = []                # align raw sequences
Report2 = []                # assemble default CDR3 clonotypes
Report3 = []                # assemble full BCR receptors



MCR = '/home/customer/COVID/mixcr-3.0.13/mixcr.jar'             # MIXCR软件目录
VDJ = '/home/customer/COVID/vdjtools-1.2.1/vdjtools-1.2.1.jar'  # VDJ 软件目录

mixcr_out = '/home/customer/COVID/Severe/mixcr_result/'         # MIXCR结果保存
vdj_out = '/home/customer/COVID/Severe/vdjtools_result/'        # MIXCR结果保存


for sample in sample_list:
    FQ_1.append(sample+'_1.clean.fq.gz')
    FQ_2.append(sample+'_2.clean.fq.gz')
    
    A_list.append(sample+'_alignments.vdjca')
    Clna.append(sample+'_clones.clna')
    Clns.append(sample+'_full_clones.clns')
    full_clo.append(sample+'_full_clones.txt')

    ## 完整序列
    Report1.append(sample+'_report1.txt')
    Report2.append(sample+'_report2.txt')
    Report3.append(sample+'_report3.txt')


## 组装完整的TCR /Ig受体序列
for i in range(len(sample)):
    # align raw sequences
    os.system('java -jar ' + MCR + ' align --species hs -p kAligner2 --report ' +  Report1[i] + ' ' + FQ_1[i] +' '+ FQ_2[i] +' '+ A_list[i])
    print('##'*50)
    # assemble default CDR3 clonotypes (note: --write-alignments is required for further contig assembly)
    os.system('java -jar ' + MCR + ' assemble --write-alignments --report ' + Report2[i] + ' '  + A_list[i] +' '+ Clna[i])
    print('##'*50)
    # assemble full BCR receptors
    os.system('java -jar ' + MCR + ' assembleContigs --report ' + Report3[i] + ' '  + Clna[i] +' '+ Clns[i])
    print('##'*50)
    # export full BCR receptors
    os.system('java -jar ' + MCR + ' exportClones -c IG -p fullImputed ' + Clns[i] +' '+ full_clo[i])
    print('##'*50)
