#!/usr/bin/python
# -*- coding: utf-8 -*-
import hypercoll

BE = 'Belgium'
EL = 'Greece'
LT = 'Lithuania'
PT = 'Portugal'
BG = 'Bulgaria'
ES = 'Spain'
LU = 'Luxembourg'
RO = 'Romania'
CZ = 'Czechia'
FR = 'France'
HU = 'Hungary'
SI = 'Slovenia'
DK = 'Denmark'
HR = 'Croatia'
MT = 'Malta'
SK = 'Slovakia'
DE = 'Germany'
IT = 'Italy'
NL = 'Netherlands'
FI = 'Finland'
EE = 'Estonia'
CY = 'Cyprus'
AT = 'Austria'
SE = 'Sweden'
IE = 'Ireland'
LV = 'Latvia'
PL = 'Poland'
UK = 'UK'
NO = 'Norway'
CH = 'Switzerland'
LI = 'Liechtenstein'
IS = 'Iceland'
MK = 'Macedonia'
AL = 'Albania'
RS = 'Serbia'

# 2017 - Larger scale cooperation projects (Cat 2) - Selected Applications
# https://eacea.ec.europa.eu/sites/eacea-site/files/2._coop2_selected_applications_incl._partners_0.pdf

p1 = [ES,NO,DK,PL,DE,AT]
p2 = [PT,IT,MK,PL,HR,UK,FR,LT] 
p3 = [IT,ES,RO,PT,BE]
p4 = [ES,DK,DE,SE,UK,LT]
p5 = [PT,ES,IT,NO,IE,UK]
p6 = [FR,PL,PT,NL,MT,AT]
p7 = [DK,IT,SI,FR,BE,EL,SE,PT,UK,FR,UK,DE]
p8 = [SK,NO,DE,AT,FR,UK,NL,HR]
p9 = [IT,UK,BE,CZ,ES,DE,FR,UK,PL,IT,RO,AT]
p10 = [PT,SI,LU,AT,PL,ES,SE,UK]
p11 = [IT,AL,SE,FR,EL,PL,BE]
p12 = [PT,LV,DK,MK,BE,FR,UK]
p13 = list(set([FR,NO,FI,IT,ES,EL,HR,HU,SE,BE,LV,CZ,FR,UK,ES,PL,NL,DE,PL,FR,BE,UK,IE]))
p14 = [HR,FR,ES,UK,IE,SI,LT,FI]
p15 = [SK,BG,NL,EL,HR,RS]

projects = [p10,p11,p13,p15]
import collections
countires = collections.deque(set([c for p in projects for c in p]))
countires =list(sorted(countires))
print(countires)

print(len(countires))
hc = hypercoll.HyperColl(countires)

color1 = [57./255,91./255,142./255]
oldcolor1 = [1./255,16./255,40./255]
oldcolor2 = [10./255,26./255,70./255]

color = oldcolor2
hc.hypercoll(projects,250,0.0,.6,
	background_color=color,font_size=9,hspace=5,
	fill=True,background_disk=True,background_circle=False,labels=True,font_face = "Open Sans")

EU = "EU"
EFTA = "EFTA"
EUC = "EU candidate"

hc.sectors(251,260,{'Italy':EU, 'Luxembourg':EU, 'France':EU, 'Slovakia':EU, 
	'Ireland':EU, 'Norway':EFTA, 'Slovenia':EU, 'Germany':EU, 'Belgium':EU, 'Spain':EU, 
	'Netherlands':EU, 'Poland':EU, 'Finland':EU, 'Sweden':EU, 'Latvia':EU, 'Croatia':EU, 
	'Bulgaria':EU, 'Portugal':EU, 'Czechia':EU, 'Serbia':EUC, 'UK':EU, 
	'Austria':EU, 'Greece':EU, 'Hungary':EU,AL:EUC},
	labels=None,
	background_color={EU:[0,51./255,153./255],EFTA:[255./255,204./255,0/255],EUC:[.6,201./255,24./255]},boundy_width=1,
)
hc.sectors(260,270,{'Italy':EU, 'Luxembourg':EU, 'France':EU, 'Slovakia':EU, 
	'Ireland':EU, 'Norway':EFTA, 'Slovenia':EU, 'Germany':EU, 'Belgium':EU, 'Spain':EU, 
	'Netherlands':EU, 'Poland':EU, 'Finland':EU, 'Sweden':EU, 'Latvia':EU, 'Croatia':EU, 
	'Bulgaria':EU, 'Portugal':EU, 'Czechia':EU, 'Serbia':EUC, 'UK':EU, 
	'Austria':EU, 'Greece':EU, 'Hungary':EU,AL:EUC},
	background_color=[1,1,1],
	foreground_color=[0,0,0],
	labels={EU:'',EFTA:'EFTA',EUC:'EU candidate'},
	font_size=8
)
