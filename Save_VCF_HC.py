#-*- coding:UTF-8 -*-
from __future__ import division#用于显示浮点数
import sys
import os
p='%s_gatk3.7_HC.vcf'%(sys.argv[1])
q='vcf_%s_filtered/%s_gatk3.7_HC_changed.vcf'%(sys.argv[1],sys.argv[1])
os.system('mkdir vcf_%s_filtered'%(sys.argv[1]))
ratio=float(sys.argv[2])
f=open(p)
L1=[line for line in f.readlines()]
L2=[s for s in L1 if s.startswith('##')]
ret_list=[item for item in L1 if item not in L2]

def gtInCell(r):
    if len(r.strip())>3:
        if r.strip().split(':')[1] == '.' or r.strip().split(':')[2] == '.':
            r=':'.join([r.strip().split(':')[0],'0,0','0','0','0'])
        AD=[int(i) for i in r.strip().split(':')[1].split(',')]
        if AD[0]+AD[1] == 0:
            new_result='./.'
        elif float(AD[0])/(AD[0]+AD[1]) <ratio:
            new_result='1/1'+r[3:]
        elif float(AD[0])/(AD[0]+AD[1]) >=ratio and float(AD[0])/(AD[0]+AD[1])<(1-ratio):
            new_result='0/1'+r[3:]
        elif float(AD[0])/(AD[0]+AD[1]) >=(1-ratio):
            new_result='0/0'+r[3:]
    elif len(r.strip())<=3:
        new_result=r
    return new_result

def GenotypeInRow(i):
    m=ret_list[i].split('\t')
    row_head=m[0:9]
    row_result=m[9:]
    new_row_result=[gtInCell(i) for i in row_result]
    ROW='\t'.join(row_head+new_row_result)
    return ROW

L2.append(ret_list[0])

for i in range(1,len(ret_list)):
    L2.append(GenotypeInRow(i))

result=''.join(L2)
h=open(q,'w')
h.write(result)
h.close()
