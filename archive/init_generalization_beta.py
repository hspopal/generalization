#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 12:30:41 2019

@author: tuk12127
"""

from psychopy import core, gui, data
import os
import subprocess


# Set relevant paths
if os.path.isdir('/Users/tuk12127'):
    project_dir = os.path.expanduser('~/Google_Drive/olson_lab/projects/misc/GENERALIZATION/')
else:
    project_dir = os.path.expanduser('~/Google_Drive/GENERALIZATION/')
os.chdir(project_dir)
os.chdir('./scripts')



#store info about the experiment session
 
expName='Generalization'
expInfo={'Participant':'', 'Session':'001', 'Order':''}
dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)
if dlg.OK==False: core.quit()  #user pressed cancel
expInfo['date']=data.getDateStr()  #add a simple timestamp
expInfo['expName']=expName

run_block_1 = ['python', 'generalization.py', 
               expInfo['Participant'], expInfo['date'],'1']
run_block_2 = ['python', 'generalization.py', 
               expInfo['Participant'], expInfo['date'],'2']

if expInfo['Order'][0] == '1':
    subprocess.Popen(run_block_1).wait()
    subprocess.Popen(run_block_2)
elif expInfo['Order'][0] == '2':
    subprocess.Popen(run_block_2).wait()
    subprocess.Popen(run_block_1)



