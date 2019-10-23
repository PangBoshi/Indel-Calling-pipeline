#-*- coding: utf-8 -*-
import os
import sys
import xlsxwriter
import xlrd
import pysam
#Secondly, all of the depth counting results will be merged in one single excel file, sample by sample.
all_file=os.listdir(os.getcwd())
all_stat=[i for i in all_file if os.path.splitext(i)[1] == ".stat"]
L=[]
for x in range(len(all_stat)):
    f=open(all_stat[x])
    depth=[i for i in f.readlines()]
    new_depth=[]
    for i in range(len(depth)):
        s=depth[i].split(' ')[-2:]
        new_depth.append(s)
    new_depth[0]=[new_depth[0][0].strip()]+['ref_ID\n']
    L.append(new_depth)
x=[]
for i in range(len(L)):
    x.append(len(L[i]))
    idx=x.index(max(x))

max_sample=L[idx]
first_col=[]
for i in range(len(max_sample)):
    s=max_sample[i][-1].strip()
    first_col.append(s)
#Writting depth into excel result file.
#When counting the unfiltered sam file, unmapped reads are marked with '*'.
bookname='%s_before_filter_initial.xlsx'%(sys.argv[1])
workbook=xlsxwriter.Workbook(bookname)
worksheet=workbook.add_worksheet('Sheet1')
worksheet.write(0,0,'reference_ID')
m=len(first_col)-1
for x in range(1,m):
    worksheet.write(x,0,first_col[x+1])
worksheet.write(m,0,'unmapped_reads_number')

#first_sample_depth
def write_matched_depth(x):
    a=len(L[x])
    b=len(first_col)
    if abs(a-b) == 0:
        worksheet.write(0,x+1,L[x][0][0])
        m=len(first_col)-1
        for i in range(1,m):
            worksheet.write(i,x+1,L[x][i+1][0])
        worksheet.write(m,x+1,L[x][1][0])
    elif abs(a-b) > 0:
        worksheet.write(0,x+1,L[x][0][0])
        for s in range(len(L[x])):
            s_id=L[x][s][-1].strip()
            if s_id == '*':
                worksheet.write(b-1,x+1,L[x][1][0])
            else:
                col_num=first_col.index(s_id)
                worksheet.write(col_num-1,x+1,L[x][s][0])
map(write_matched_depth,[i for i in range(len(all_stat))])
p=len(first_col)
worksheet.write(p,0,'successful_mapped_reads')
worksheet.write(p+1,0,'total_reads_number')
total_reads=[]
for i in range(len(all_stat)):
    sam_reads=pysam.AlignmentFile(all_stat[i][:-5])
    reads_num=[x for x in sam_reads.fetch()]
    total_reads.append(len(reads_num))
for x in range(len(total_reads)):
    worksheet.write(p+1,x+1,total_reads[x])
workbook.close()
##
newbook=xlrd.open_workbook(bookname)
sheet_name=newbook.sheet_names()[0]
newsheet=newbook.sheet_by_name(sheet_name)
rows_num=newsheet.nrows
cols_num=newsheet.ncols
rows=newsheet.row_values(p-1)
empty_depth=[]
for i in range(len(rows)):
    if rows[i] == '':
        empty_depth.append(i)
for x in empty_depth:
    rows[x]='0'

book2name='%s_before_filter_mid.xlsx'%(sys.argv[1])
rebook=xlsxwriter.Workbook(book2name)
resheet=rebook.add_worksheet('Sheet1')
for x in range(rows_num):
    for y in range(cols_num):
        cell_value=newsheet.cell_value(x,y)
        resheet.write(x,y,cell_value)
for i in range(len(total_reads)):
    resheet.write(p,i+1,total_reads[i]-int(rows[i+1]))
rebook.close()
os.system('rm -rf %s'%(bookname))

#fill the blank with zero
final_bookname='%s_before_filter.xlsx'%(sys.argv[1])
rebook_1=xlrd.open_workbook(book2name)
resheet_1=rebook_1.sheet_by_index(0)
def changed_colvalues(x):
    s=resheet_1.col_values(x)
    for i in range(1,len(s)):
        if s[i] == '':
            s[i]=0
        else:
            s[i]=float(s[i])
    return s
col_number=resheet_1.ncols
final_name='mapping_%s_before_filter.xlsx'%(sys.argv[1])
final_book=xlsxwriter.Workbook(final_name)
final_sheet=final_book.add_worksheet('Sheet1')
DupSuffix=['reference_ID']+[i.split('.')[0] for i in resheet_1.row_values(0)[1:]]
final_sheet.write_row(0,0,DupSuffix)
final_sheet.write_column(0,0,resheet_1.col_values(0))
for j in range(1,col_number):
    final_sheet.write_column(1,j,changed_colvalues(j)[1:])
final_book.close()
os.system('rm -rf %s' % (book2name))
