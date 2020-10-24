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
deep_list='M.csv'

def make_chart(alpha0,delta0,M_N):

	pp3 = '''
	filename output Map_M$$M_N$$.tex
	filename stars starsH.dat
	filename nebulae nebulaeM.dat
	filename milky_way milkyway.dat

	switch pdf_output on
	switch colored_stars off
	switch milky_way on
	switch labels off
	switch ecliptic off
	switch boundaries off
	switch nebulae on
	set grad_per_cm $$SCALE$$
	set box_width 20
	set box_height 20
	color stars 0 0 0
	color nebulae 0 0 0
	color background 1 1 1
	color grid 0.5 0.5 0.5
	color ecliptic 0.3 0.3 0.3
	color constellation_lines 0.7 0.7 0.7
	color labels 0 0 0
	color boundaries 0 0 0
	color highlighted_boundaries 0 0 0
	color milky_way 0.5 0.5 0.5
	set faintest_star_magnitude $$M_MAX$$
	set faintest_star_disk_magnitude $$M_DISK$$
	set minimal_star_radius $$S_RADIUS$$
	set star_scaling $$S_SCALE$$

	set center_rectascension $$RA$$
	set center_declination $$DEC$$
	'''

	scale=2			#light
	M_MAX=6
	M_DISK=5
	star_scale=1.22
	star_r = 0.035

	# scale=1.65		#medium
	# M_MAX=7.5
	# M_DISK=6.5
	# star_scale=1.15
	# star_r = 0.03

	# scale=1.25		#high
	# M_MAX=8.5
	# M_DISK=7.5
	# star_scale=0.9
	# star_r = 0.03

	pp3=pp3.replace('$$SCALE$$', str(scale) )
	pp3=pp3.replace('$$M_MAX$$', str(M_MAX) )
	pp3=pp3.replace('$$M_DISK$$', str(M_DISK) )
	pp3=pp3.replace('$$S_RADIUS$$', str(star_r) )
	pp3=pp3.replace('$$S_SCALE$$', str(star_scale) )


	pp3=pp3.replace('$$M_N$$',str(M_N))
	pp3=pp3.replace('$$RA$$',str(alpha0/15.))
	pp3=pp3.replace('$$DEC$$',str(delta0))

	pp3fname = './map_M'+str(M_N)+'.pp3'
	file = open(pp3fname, 'w')
	file.write(pp3)
	file.close()

	call(['./pp3-1.3.3_9m/pp3', pp3fname],stdout=DEVNULL,stderr = DEVNULL)
	# call(['pdflatex.exe', 'Chart'+str(N)+'.tex'],stdout=DEVNULL)#,stderr = DEVNULL )
	print(M_N)

Mdat = np.loadtxt(deep_list,dtype=str,delimiter=';')

for i in range(len(Mdat)):
	Ms= Mdat[:,0].astype(int)
	alphaM = Mdat[:,1].astype(float)
	deltaM = Mdat[:,2].astype(float)

	make_chart(alphaM[i], deltaM[i], Ms[i])
