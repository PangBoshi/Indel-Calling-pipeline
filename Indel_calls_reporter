#-*- coding:UTF-8 -*-
from __future__ import division#用于显示浮点数
import sys
import os
import re
import xlrd
import xlsxwriter
p=sys.argv[1]
q=sys.argv[2]
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
    s_result_idx=[p for p in range(len(s_result)) if s_result[p] == './.' or s_result[p] == '.' or s_result[p] == './.:.:.:.:.']
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

