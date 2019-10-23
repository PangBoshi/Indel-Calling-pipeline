#-*- coding:UTF-8 -*-
from __future__ import division#用于显示浮点数
import sys
import os
import re
import xlrd
import xlsxwriter
p=sys.argv[1]
o=sys.argv[2]
q=sys.argv[3]
#外部参数1：input.vcf，外部参数2：output_depth.xlsx
f=open(p)#此处修改输入文件路径
L1=[line for line in f.readlines()]# L1[52]是第一个突变信息
L2=[s for s in L1 if s.startswith('##')]
if __name__ == '__main__':
    ret_list=[item for item in L1 if item not in L2]#生成L1和L2的差集 ret_list[1]等于L1[52]

col_0=['Chrom']+[ret_list[i].split('\t')[0] for i in range(1,len(ret_list))]
col_1=['POS']+[ret_list[i].split('\t')[1] for i in range(1,len(ret_list))]
col_2=['REF']+[ret_list[i].split('\t')[3] for i in range(1,len(ret_list))]
col_3=['ALT']+[ret_list[i].split('\t')[4] for i in range(1,len(ret_list))]
col_4=['FILTER']+[ret_list[i].split('\t')[6] for i in range(1,len(ret_list))]
result_genotype=[]
result_depth=[]
empty_result='-:0,0:0:0:0'
for i in range(9,len(ret_list[0].split('\t'))):
    sample_name=ret_list[0].split('\t')[i]
    s_result=[sample_name]+[ret_list[j].split('\t')[i].strip() for j in range(1,len(ret_list))]
    s_result_idx=[p for p in range(len(s_result)) if s_result[p] == './.' or s_result[p] == '.']
    for x in s_result_idx:
        s_result[x]=empty_result
    s_genotype=[s_result[0]]+[s_result[i].split(':')[0] for i in range(1,len(s_result))]
    s_depth=[s_result[0]]+[int(s_result[i].split(':')[2]) for i in range(1,len(s_result))]
    result_genotype.append(s_genotype)
    result_depth.append(s_depth)

gt_book=xlsxwriter.Workbook('%s_HC.vcf_genotype.xlsx'%(q))
gt_sheet=gt_book.add_worksheet('Sheet1')
gt_sheet.write_column(0,0,col_0)
gt_sheet.write_column(0,1,col_1)
gt_sheet.write_column(0,2,col_2)
gt_sheet.write_column(0,3,col_3)
gt_sheet.write_column(0,4,col_4)
for y in range(len(result_genotype)):
    gt_sheet.write_column(0,y+5,result_genotype[y])

dp_book=xlsxwriter.Workbook('%s_HC.vcf_depth.xlsx'%(q))
dp_sheet=dp_book.add_worksheet('Sheet1')
dp_sheet.write_column(0,0,col_0)
dp_sheet.write_column(0,1,col_1)
dp_sheet.write_column(0,2,col_2)
dp_sheet.write_column(0,3,col_3)
dp_sheet.write_column(0,4,col_4)
for z in range(len(result_depth)):
    dp_sheet.write_column(0,z+5,result_depth[z])

gt_book.close()
dp_book.close()

depth_file=xlrd.open_workbook('%s_HC.vcf_depth.xlsx'%(q))
genotype_file=xlrd.open_workbook('%s_HC.vcf_genotype.xlsx'%(q))
depth_data=depth_file.sheet_by_name('Sheet1')
genotype_data=genotype_file.sheet_by_name('Sheet1')
cols_num=depth_data.ncols
rows_num=depth_data.nrows
#判断位点去留
filtered_variant=[]
for x in range(1,rows_num):
    variant_depth=[int(i) for i in depth_data.row_values(x)[5:]]
    if max(variant_depth) >= 30:
        filtered_variant.append(depth_data.row_values(x))

#判断样本去留
def sample_quality(x):
    depth_value=[int(i) for i in depth_data.row_values(x)[5:]]
    low_depth_position=[]
    n=0
    while n < len(depth_value):
        if depth_value[n] < 15:
            low_depth_position.append(n)
        n=n+1
    changed_genotype=genotype_data.row_values(x)
    for m in range(len(low_depth_position)):
        changed_genotype[low_depth_position[m]+5]='.'
    for i in range(len(changed_genotype)):
        if changed_genotype[i]=='0/0':
            changed_genotype[i]='%s'%(changed_genotype[2])
        elif changed_genotype[i]=='0/1':
            changed_genotype[i]='%s/%s'%(changed_genotype[2],changed_genotype[3].split(',')[0])
        elif changed_genotype[i]=='1/0':
            changed_genotype[i]='%s/%s'%(changed_genotype[2],changed_genotype[3].split(',')[0])
        elif changed_genotype[i]=='0/2':
            changed_genotype[i]='%s/%s'%(changed_genotype[2],changed_genotype[3].split(',')[1])
        elif changed_genotype[i]=='2/0':
            changed_genotype[i]='%s/%s'%(changed_genotype[2],changed_genotype[3].split(',')[1])
        elif changed_genotype[i]=='1/1':
            changed_genotype[i]='%s'%(changed_genotype[3].split(',')[0])
        elif changed_genotype[i]=='1/2':
            changed_genotype[i]='%s/%s'%(changed_genotype[3].split(',')[0],changed_genotype[3].split(',')[1])
        elif changed_genotype[i]=='2/1':
            changed_genotype[i]='%s/%s'%(changed_genotype[3].split(',')[0],changed_genotype[3].split(',')[1])
        elif changed_genotype[i]=='2/2':
            changed_genotype[i]='%s'%(changed_genotype[3].split(',')[1])
        elif changed_genotype[i]=='0/3':
            changed_genotype[i]='%s/%s'%(changed_genotype[2],changed_genotype[3].split(',')[2])
        elif changed_genotype[i]=='3/0':
            changed_genotype[i]='%s/%s'%(changed_genotype[2],changed_genotype[3].split(',')[2])
        elif changed_genotype[i]=='3/3':
            changed_genotype[i]='%s'%(changed_genotype[3].split(',')[2])
        elif changed_genotype[i]=='1/3':
            changed_genotype[i]='%s/%s'%(changed_genotype[3].split(',')[0],changed_genotype[3].split(',')[2])
        elif changed_genotype[i]=='3/1':
            changed_genotype[i]='%s/%s'%(changed_genotype[3].split(',')[0],changed_genotype[3].split(',')[2])
        elif changed_genotype[i]=='2/3':
            changed_genotype[i]='%s/%s'%(changed_genotype[3].split(',')[1],changed_genotype[3].split(',')[2])
        elif changed_genotype[i]=='3/2':
            changed_genotype[i]='%s/%s'%(changed_genotype[3].split(',')[1],changed_genotype[3].split(',')[2])
    return changed_genotype

savebook=xlsxwriter.Workbook('%s_genotype_filtered.xlsx'%(q))
savesheet=savebook.add_worksheet('Sheet1')
savesheet.write_row(0,0,depth_data.row_values(0))
for x in range(1,rows_num):
    savesheet.write_row(x,0,sample_quality(x))
savebook.close()

depth_file=xlrd.open_workbook('%s_HC.vcf_depth.xlsx'%(q))
genotype_file=xlrd.open_workbook('%s_HC.vcf_genotype.xlsx'%(q))
depth_data=depth_file.sheet_by_name('Sheet1')
genotype_data=genotype_file.sheet_by_name('Sheet1')
cols_num=depth_data.ncols
rows_num=depth_data.nrows
#判断位点去留
filtered_variant=[]
for x in range(1,rows_num):
    variant_depth=[int(i) for i in depth_data.row_values(x)[5:]]
    if max(variant_depth) >= 30:
        filtered_variant.append(depth_data.row_values(x))

#判断样本去留
def sample_quality(x):
    depth_value=[int(i) for i in depth_data.row_values(x)[5:]]
    low_depth_position=[]
    n=0
    while n < len(depth_value):
        if depth_value[n] < 1:
            low_depth_position.append(n)
        n=n+1
    changed_genotype=genotype_data.row_values(x)
    for m in range(len(low_depth_position)):
        changed_genotype[low_depth_position[m]+5]='.'
    for i in range(len(changed_genotype)):
        if changed_genotype[i]=='0/0':
            changed_genotype[i]='%s'%(changed_genotype[2])
        elif changed_genotype[i]=='0/1':
            changed_genotype[i]='%s/%s'%(changed_genotype[2],changed_genotype[3].split(',')[0])
        elif changed_genotype[i]=='1/0':
            changed_genotype[i]='%s/%s'%(changed_genotype[2],changed_genotype[3].split(',')[0])
        elif changed_genotype[i]=='0/2':
            changed_genotype[i]='%s/%s'%(changed_genotype[2],changed_genotype[3].split(',')[1])
        elif changed_genotype[i]=='2/0':
            changed_genotype[i]='%s/%s'%(changed_genotype[2],changed_genotype[3].split(',')[1])
        elif changed_genotype[i]=='1/1':
            changed_genotype[i]='%s'%(changed_genotype[3].split(',')[0])
        elif changed_genotype[i]=='1/2':
            changed_genotype[i]='%s/%s'%(changed_genotype[3].split(',')[0],changed_genotype[3].split(',')[1])
        elif changed_genotype[i]=='2/1':
            changed_genotype[i]='%s/%s'%(changed_genotype[3].split(',')[0],changed_genotype[3].split(',')[1])
        elif changed_genotype[i]=='2/2':
            changed_genotype[i]='%s'%(changed_genotype[3].split(',')[1])
        elif changed_genotype[i]=='0/3':
            changed_genotype[i]='%s/%s'%(changed_genotype[2],changed_genotype[3].split(',')[2])
        elif changed_genotype[i]=='3/0':
            changed_genotype[i]='%s/%s'%(changed_genotype[2],changed_genotype[3].split(',')[2])
        elif changed_genotype[i]=='3/3':
            changed_genotype[i]='%s'%(changed_genotype[3].split(',')[2])
        elif changed_genotype[i]=='1/3':
            changed_genotype[i]='%s/%s'%(changed_genotype[3].split(',')[0],changed_genotype[3].split(',')[2])
        elif changed_genotype[i]=='3/1':
            changed_genotype[i]='%s/%s'%(changed_genotype[3].split(',')[0],changed_genotype[3].split(',')[2])
        elif changed_genotype[i]=='2/3':
            changed_genotype[i]='%s/%s'%(changed_genotype[3].split(',')[1],changed_genotype[3].split(',')[2])
        elif changed_genotype[i]=='3/2':
            changed_genotype[i]='%s/%s'%(changed_genotype[3].split(',')[1],changed_genotype[3].split(',')[2])
    return changed_genotype

savebook=xlsxwriter.Workbook('%s_genotype_unfiltered.xlsx'%(q))
savesheet=savebook.add_worksheet('Sheet1')
savesheet.write_row(0,0,depth_data.row_values(0))
for x in range(1,rows_num):
    savesheet.write_row(x,0,sample_quality(x))
savebook.close()

print 'Extracted depth is in : %s_HC.vcf_depth.xlsx'%(q)
print 'Extracted genotype is in : %s_HC.vcf_genotype.xlsx'%(q)
print 'Unfiltered genotype is in : %s_genotype_unfiltered.xlsx'%(q)
print 'Filtered genotype is in : %s_genotype_filtered.xlsx'%(q)

gt=xlrd.open_workbook('%s_genotype_filtered.xlsx'%(q))
info=xlrd.open_workbook(o)
gt_data=gt.sheet_by_index(0)
info_data=info.sheet_by_index(0)
row_num=gt_data.nrows
col_0=['Amplicon_Name']+gt_data.col_values(0)[1:]
col_1=gt_data.col_values(1)
col_2=['Location']
col_3=['Chrom']
col_4=['Strand']
col_5=gt_data.col_values(2)
col_6=gt_data.col_values(3)
col_7=['REF_2']
col_8=['ALT_2']
col_9=['MAF']
#计算 MAF
for x in range(1,row_num):
    genotype=gt_data.row_values(x)[5:]
    ref=gt_data.row_values(x)[2]
    alt_num=len(gt_data.row_values(x)[3].split(','))
    if alt_num == 1:
        alt=gt_data.row_values(x)[3].split(',')[0]
        hete=ref+'/'+alt
        total_allel=genotype.count(ref)*2+genotype.count(alt)*2+genotype.count(hete)*2
        alt_allel=genotype.count(alt)*2+genotype.count(hete)
        if alt_allel == 0:
            MAF_value = 0
        else:
            MAF_value=(alt_allel*1.0)/total_allel
    elif alt_num == 2:
        alt_1=gt_data.row_values(x)[3].split(',')[0]
        alt_2=gt_data.row_values(x)[3].split(',')[1]
        hete_1=ref+'/'+alt_1
        hete_2=ref+'/'+alt_2
        total_allel=genotype.count(ref)*2+genotype.count(alt_1)*2+genotype.count(alt_2)*2+genotype.count(hete_1)*2+genotype.count(hete_2)*2
        alt_allel=genotype.count(alt_1)*2+genotype.count(hete_1)+genotype.count(alt_2)*2+genotype.count(hete_2)
        if alt_allel == 0:
            MAF_value = 0
        else:
            MAF_value=(alt_allel*1.0)/total_allel
    elif alt_num == 3:
        alt_1=gt_data.row_values(x)[3].split(',')[0]
        alt_2=gt_data.row_values(x)[3].split(',')[1]
        alt_3=gt_data.row_values(x)[3].split(',')[2]
        hete_1=ref+'/'+alt_1
        hete_2=ref+'/'+alt_2
        hete_3=ref+'/'+alt_3
        total_allel=genotype.count(ref)*2+genotype.count(alt_1)*2++genotype.count(alt_2)*2+genotype.count(alt_3)*2+genotype.count(hete_1)*2+genotype.count(hete_2)*2+genotype.count(hete_3)*2
        alt_allel=genotype.count(alt_1)*2+genotype.count(hete_1)+genotype.count(alt_2)*2+genotype.count(hete_2)+genotype.count(alt_3)*2+genotype.count(hete_3)
        if alt_allel == 0:
            MAF_value = 0
        else:
            MAF_value=(alt_allel*1.0)/total_allel
    col_9.append(MAF_value)

#计算 location
info_header=info_data.row_values(0)
insert_match=re.compile('/*amp_start/*',re.I)
for i in range(len(info_header)):
    if insert_match.match(info_header[i]):
        insert_start=info_data.col_values(i)
chrom_match=re.compile('/*chrom/*',re.I)
for i in range(len(info_header)):
    if chrom_match.match(info_header[i]):
        chroms=info_data.col_values(i)
strand_match=re.compile('/*strand/*',re.I)
for i in range(len(info_header)):
    if strand_match.match(info_header[i]):
        strand_mark=info_data.col_values(i)

interval_maf_table_name='%s_MAF_result.xlsx' % (q)
book=xlsxwriter.Workbook(interval_maf_table_name)
sheet=book.add_worksheet('Sheet1')

if __name__ == '__main__':
    CHROM_To_write=[chroms[idx] for idx in [info_data.col_values(0).index(i) for i in gt_data.col_values(0)[1:]]]
    STRAND_To_write=[strand_mark[idx] for idx in [info_data.col_values(0).index(i) for i in gt_data.col_values(0)[1:]]]
    ChPo=[gt_data.col_values(0)[i]+'|'+gt_data.col_values(1)[i] for i in range(1,gt_data.nrows)]
    Position=[int(insert_start[info_data.col_values(0).index(ChPo[i].split('|')[0])])+int(ChPo[i].split('|')[1])-1 for i in range(len(ChPo))]
    col_2=col_2+Position
    col_3=col_3+CHROM_To_write
    col_4=col_4+STRAND_To_write
    col_7=col_7+gt_data.col_values(2)[1:]
    col_8=col_8+gt_data.col_values(3)[1:]

def DNA_reverse(seq):
    seq=seq.upper()
    seq=seq.replace('A','t')
    seq=seq.replace('T','a')
    seq=seq.replace('C','g')
    seq=seq.replace('G','c')
    seq=seq.upper()[::-1]
    return seq

L_header=[info_data.col_values(0)[i]+':'+str(int(info_data.col_values(6)[i])-int(info_data.col_values(5)[i])+1) for i in range(1,info_data.nrows)]
id_in_L_header=[i.split(':')[0] for i in L_header]
length_in_L_header=[i.split(':')[1] for i in L_header]
for i in range(1,gt_data.nrows):
    s=col_4[i]
    if s == '-':
        id_idx=id_in_L_header.index(gt_data.col_values(0)[i])
        seq_length=length_in_L_header[id_idx]
        head_position=col_2[i]-int(col_1[i])+int(seq_length)
        reverse_streand_position=head_position-int(col_1[i])+1
        col_7[i]=DNA_reverse(col_7[i])
        col_8[i]=','.join(DNA_reverse(col_8[i]).split(',')[::-1])
        base_length=len(col_7[i])
        col_2[i]=reverse_streand_position
    else:
        pass
sheet.write_column(0,0,col_0)
sheet.write_column(0,1,col_1)
sheet.write_column(0,2,col_2)
sheet.write_column(0,3,col_3)
sheet.write_column(0,4,col_4)
sheet.write_column(0,5,col_5)
sheet.write_column(0,6,col_6)
sheet.write_column(0,7,col_7)
sheet.write_column(0,8,col_8)
sheet.write_column(0,9,col_9)
book.close()

print 'MAF result in : %s_MAF_result.xlsx'%(sys.argv[3])
