#-*- coding:UTF-8 -*-
import os
import sys
a=sys.argv[1]
os.system('date')
os.system('mkdir -p BiadapterCut/untrim')
os.system('cat info.txt | while read line; do cutadapt -g ACGACGTGTCGAGTTCAGGT -G CAGTGAGTCGCCACAGGTCA --untrimmed-output=BiadapterCut/untrim/$line"_"R1.fastq.fq --untrimmed-paired-output=BiadapterCut/untrim/$line"_"R2.fastq.fq -o BiadapterCut/$line"_"R1.fastq.fq -p BiadapterCut/$line"_"R2.fastq.fq sample_%s/$line"_"R1.fastq sample_%s/$line"_"R2.fastq; done'%(a,a))
os.system('rm -rf BiadapterCut/untrim')
os.system('mkdir sam_unsorted_A')
os.system('mkdir bam_sorted_filter_A')
os.system('bwa index -a is reference_%s.fasta'%(a))
os.system('samtools faidx reference_%s.fasta'%(a))
os.system('java -jar /home/sdb/biosoft/picardtools/CreateSequenceDictionary.jar R=reference_%s.fasta O=reference_%s.dict'%(a,a))
os.system('cat info.txt | while read line; do bwa mem -t 18 -R "@RG\\tID:CNC2_S202\\tLB:03\\tSM:$line\\tPL:HISEQ" reference_%s.fasta BiadapterCut/$line"_"R1.fastq.fq  BiadapterCut/$line"_"R2.fastq.fq > sam_unsorted_A/$line.sam; done'%(a))
os.system('''cat info.txt | while read line; do samtools view -@ 16 -h -F 2048 -f 3 sam_unsorted_A/$line.sam | awk '$1~/^@/ || $6!~/.*[HS].*[HS]?/{print $0}'|samtools sort -@ 16 -o bam_sorted_filter_A/$line.bam; done''')
os.system('samtools merge filter_%s.bam bam_sorted_filter_A/*.bam'%(a))
os.system('samtools sort -o filter_sorted_%s.bam filter_%s.bam'%(a,a))
os.system('samtools index filter_sorted_%s.bam'%(a))
os.system('mkdir %s_HC_result'%(a))
os.system('java  -Xmx60G -jar /home/sdb/biosoft/gatk3.7/GenomeAnalysisTK.jar -T HaplotypeCaller --maxNumHaplotypesInPopulation 3 --dontUseSoftClippedBases -dt NONE --max_alternate_alleles 1 --pcr_indel_model CONSERVATIVE -R reference_%s.fasta -I filter_sorted_%s.bam -o %s_HC_result/%s_gatk3.7_HC.vcf' %(a,a,a,a))
os.system('mkdir sam_sorted_filter_A')
os.system('cat info.txt|while read line; do samtools sort -o sam_sorted_filter_A/$line.sam bam_sorted_filter_A/$line.bam; done')
os.system('date')
