#!/usr/bin/python3 

import kang,sys

file_gff = sys.argv[1]
file_in  = sys.argv[2]
file_csv = sys.argv[3]


dicGN2loc = {}
for line in open(file_gff):
	if line[0] == '#':
		continue
	cell = line.strip().split('\t')
	strChr = cell[0]
	intL1 = int(cell[3])
	intL2 = int(cell[4])
	strT = cell[2] 
	strInfo_list = cell[8].split(';')
	dicInfo = dict(zip([x.split('=')[0] for x in strInfo_list],[x.split('=')[1] for x in strInfo_list]))
	if strT == 'mRNA' and dicInfo["longest"] == "1":
		dicGN2loc[dicInfo['Name']] = (strChr,intL1,intL2)
window = 100000
dicChr2LTR = {}
for line in open(file_csv):
	cell = line.strip().split('\t')
	strChr = cell[0].split('_')[0]
	intL1 = int(cell[1])
	intL2 = int(cell[2])
	try:
		dicChr2LTR[(strChr,int(intL1/window))].append(cell)
	except KeyError:
		dicChr2LTR[(strChr,int(intL1/window))] = [cell]
Outfile = open(file_in+'.ltr.nontandem.txt','w')
Outfile_stat = open(file_in+'.ltr.nontandem.stat.txt','w')
dicANNOT2num = {}
dicGenelist = {}
total_genes = 0
for line in open(file_in):
	cell = line.strip().split('\t')
	gene_list = cell[5].split(',')
	for gene in gene_list:
		dicGenelist[gene] = 1

for strGN in dicGN2loc:
	try:
		if dicGenelist[strGN]:
			continue
	except KeyError:
		pass
	total_genes += 1
	strChr,intL1,intL2 = dicGN2loc[strGN]
	start = intL1 - 1000
	end = intL2 + 1000
	try:
		LTR_list = dicChr2LTR[(strChr, int(start/window))]
	except KeyError:
		continue
	for ecell in LTR_list:
		estart = int(ecell[1])
		eend = int(ecell[2])
		if start < estart < end and start < eend < end:
			print(strGN,strChr,intL1,intL2, estart,eend,ecell[-2],ecell[-1],sep='\t',file=Outfile)
			try:
				dicANNOT2num[ecell[-1]] += 1
			except KeyError:
				dicANNOT2num[ecell[-1]] = 1
print(dicANNOT2num,file=Outfile_stat)
print("total_genes",total_genes,file=Outfile_stat)	
