#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import numpy as np
#import codecs
from astropy import units as u
from astropy.coordinates import SkyCoord
from subprocess import call, DEVNULL
import random
import os
import glob

Nmaps = 20
show_ans = True
gen_ans = False
clear=True
deep_list='M.csv'

high_w = 0.8
medium_w = 1
low_w = 1

def make_chart(M_Ns,N):
	tex =  r"""\documentclass[11pt,a4paper]{article}
		\usepackage[utf8]{inputenc}
		\usepackage[russian]{babel}
		\usepackage[OT1]{fontenc}
		\usepackage{amsmath}
		\usepackage{amsfonts}
		\usepackage{amssymb}
		\usepackage{graphicx}
		\usepackage[left=1.5cm,right=1.5cm,top=1cm,bottom=1cm]{geometry}
		\begin{document}
		\subsection*{MMMMMMM, MyMmap $$NUMBER$$.... 26.10.2020}
		"""
	tex_part = r"""
		\begin{figure}[h!]
		\begin{minipage}[h!]{0.45\linewidth}
		\center{\includegraphics[width=1\linewidth]{$$F1$$}}
		\end{minipage}
		\hfill
		\begin{minipage}[h!]{0.45\linewidth}
		\center{\includegraphics[width=1\linewidth]{$$F2$$}}
		\end{minipage}
		\end{figure}
		"""
	# print(M_Ns)
	def rand_level():
		rnd = random.random()
		if 0<=rnd<low_w:
			return '40'
		if low_w<=rnd<low_w+medium_w:
			return '33'
		if low_w+medium_w<=rnd<=1:
			return '25'
		print('WARNING')
		return '40'

	for j in range(0,len(M_Ns),2):
		f1name=rand_level()+'/MAP_M'+str(M_Ns[j])
		f2name=rand_level()+'/MAP_M'+str(M_Ns[j+1])
		now_tex_part = tex_part.replace('$$F1$$',f1name)
		now_tex_part = now_tex_part.replace('$$F2$$',f2name)
		tex+=now_tex_part
		if j==4:
			tex+=r"""
			\newpage
			\subsection*{MMMMMMM  .... $$NUMBER$$ }"""

	tex+=r'\end{document}'

	# tex = tex.replace('$$MAP_NAME$$',map_name)
	# tex = tex.replace('$$STAR_TABLE$$',star_table)
	# tex = tex.replace('$$M_LIST$$',m_list)
	tex = tex.replace('$$NUMBER$$',str(N))
	texfname = 'M_Map'+str(N)+'.tex'
	file = open(texfname, 'w')
	file.write(tex)
	file.close()

	call(['pdflatex.exe', texfname],stdout=DEVNULL)#,stderr = DEVNULL )
	print(M_Ns, N)


Mdat = np.loadtxt(deep_list,dtype=str,delimiter=';')
weight_summ = high_w + medium_w + low_w
high_w /= weight_summ
medium_w /= weight_summ
low_w /= weight_summ


if clear:
	rem = np.hstack([glob.glob('./*.pdf'), glob.glob('./*.tex'), glob.glob('./*.log'), glob.glob('./*.aux'), glob.glob('./*.eps'), glob.glob('./*.dvi'), glob.glob('./*.pp3'), glob.glob('./*.dat')])
	for f in rem:
		os.remove(f)

for i in range(Nmaps):
	sequence = np.random.permutation(len(Mdat))[:12]
	MNS=Mdat[sequence,0]
	make_chart(MNS,i)

call('pdfjoin --outfile ./ALLMMMcharts.pdf ./M_Map*pdf', shell=True)


rem = np.hstack([glob.glob('./*.log'), glob.glob('./*.aux'), glob.glob('./*.eps'), glob.glob('./*.dvi'), glob.glob('./*.p3'), glob.glob('./*.dat')])
for f in rem:
	os.remove(f)
