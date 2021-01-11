#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 14:57:44 2018

@author: tuk12127
"""

from psychopy import core, visual, event#, sound
#from psychopy.tools.filetools import fromFile, toFile
import random
import os
import pandas as pd
from PIL import Image
import numpy as np

project_dir = os.path.expanduser('~/Google_Drive/olson_lab/projects/misc/GENERALIZATION')
os.chdir(project_dir)
char_dir = 'Finalized_stimuli/characters/'
scene_dir = 'Finalized_stimuli/encoding/'
item_dir = 'Finalized_stimuli/individual_items/'

scene_images = [i for i in os.listdir('./Finalized_Stimuli/encoding/') if i.endswith('.psd')]
stimulus_key = pd.read_csv('Finalized_Stimuli/stimulus_key.csv')
stimulus_key['Stim'] = stimulus_key['Item'] + '_' + stimulus_key['Color']
character_list = stimulus_key['Character'].unique().tolist()
random.shuffle(character_list)
fixation = 'Finalized_Stimuli/fixation_cross.png'
subject_stim = pd.DataFrame(columns=['Part','Character','Scene','Item','Color','Lure_1','Lure_2','Answer'])
item_size = 200, 200




### Encoding

subject_items = []
count = 0
# Create randomized orders for all scenes and items
for character in character_list:
    encoding_character_order = random.sample(range(1,5),4)
    item_list = stimulus_key[stimulus_key['Character']==character]['Item'].unique().tolist()
    random.shuffle(item_list)
    encoding_items = item_list[:4]
    foil_items = item_list[4:]
    
    for i in range(4):
        color_list = stimulus_key[stimulus_key['Item']==encoding_items[i]]['Stim'].tolist()
        random.shuffle(color_list)
        subject_stim.loc[count,'Part'] = 'encoding'
        subject_stim.loc[count,'Character'] = character
        subject_stim.loc[count,'Scene'] = character+'_encoding_'+str(encoding_character_order[i])
        subject_stim.loc[count,'Item'] = encoding_items[i]
        subject_stim.loc[count,'Color'] = color_list[0]
        count = count + 1
        


subject_stim = subject_stim.sample(frac=1).reset_index(drop=True)


# create window
win = visual.Window([1000,600], allowGUI=True, monitor='testMonitor', 
                    units='norm', color="Gray")

r = open('text_instructions.txt', 'r')
instr = r.read().splitlines()
r.close()
    
temp_instr = visual.TextStim(win, instr[0], color='black', pos=[0,0])
temp_instr.draw()
win.update()
core.wait(2)
win.flip()

# Introduce characters
char_intro_order = ['doraemon', 'gaturro', 'krtek', 'moomin', 'unico', 'henry', 
                    'tama', 'tabaluga', 'luntik']
n = 1
for char in char_intro_order:
    temp_instr = visual.TextStim(win, instr[n], color='black', pos=[0,0.5])
    char_stim = Image.open(char_dir + 
                           [i for i in os.listdir(char_dir)
                           if i.startswith(char)][0])
    char_stim.thumbnail(item_size, Image.ANTIALIAS)
    char_stim = visual.ImageStim(win, char_stim, pos=[0,-0.5])
    temp_instr.draw()
    char_stim.draw()
    win.update()
    core.wait(3)
    win.flip()
    n = n + 1
    
# Example of encoding
temp_instr = visual.TextStim(win, instr[11], color='black', pos=[0,0])
temp_instr.draw()
win.update()
core.wait(1)
win.flip()

temp_instr = visual.TextStim(win, instr[12], color='black', pos=[0,0.7])
temp_instr.draw()
scene_stim = scene_dir+'example.png'
item_stim = Image.open(item_dir+'books.png')
item_stim.thumbnail(item_size, Image.ANTIALIAS)
scene_pres = visual.ImageStim(win, scene_stim, pos=[-0.5,0])
item_pres = visual.ImageStim(win, item_stim, pos=[0.5,0])
scene_pres.draw()
item_pres.draw()
win.update()
core.wait(1)
win.flip()


# Start encoding
temp_instr = visual.TextStim(win, instr[13], color='black', pos=[0,0])
temp_instr.draw()
win.update()
core.wait(1)
win.flip()


#encoding_music = sound.Sound('encoding_sound.wav')
#encoding_music.play()

for n in range(len(subject_stim)):
    if event.getKeys(['escape']):
        win.close()  # assumes your visual Window is named win; seems optional
        core.quit()
    scene_stim = scene_dir+subject_stim['Scene'].iloc[n]+'.png'
    item_stim = Image.open(item_dir+
                           subject_stim['Scene'].iloc[n].split('_')[0]+'/'+
                           subject_stim['Color'].iloc[n]+'.png')
    item_stim.thumbnail(item_size, Image.ANTIALIAS)
    scene_pres = visual.ImageStim(win, scene_stim, pos=[-0.35,0])
    item_pres = visual.ImageStim(win, item_stim, pos=[0.5,0])
    scene_pres.draw()
    item_pres.draw()
    win.update()
    core.wait(0.5)
    win.flip()
    fix_pres = scene_pres = visual.ImageStim(win, fixation, pos=[0,0])
    fix_pres.draw()
    win.update()
    win.flip()

#encoding_music.stop()







### Generalization

# Generalization instructions
temp_instr = visual.TextStim(win, instr[14], color='black', pos=[0,0])
temp_instr.draw()
win.update()
core.wait(1)
win.flip()

random.shuffle(character_list)

# Pick items to be used as b/w category lures
gen_lure_items = pd.DataFrame(columns=['Lure_1','Lure_2'], index=character_list)
items_already_used = subject_stim['Item'].tolist()
for character in character_list:
    gen_lure_items.loc[character] = random.sample([x for x in stimulus_key[stimulus_key['Character']==character]['Item'].unique() 
                           if x not in items_already_used],2)
    items_already_used = subject_stim['Item'].tolist() + gen_lure_items['Lure_1'].tolist() + gen_lure_items['Lure_2'].tolist()

def shuffle(df, n=1, axis=0):     
    df = df.copy()
    for _ in range(n):
        df.apply(np.random.shuffle, axis=axis)
    return df

gen_char_pairs = pd.DataFrame(columns=['Lure_1','Lure_2'], index=character_list)
gen_char_pairs['Lure_1'] = character_list
gen_char_pairs['Lure_2'] = character_list

reshuffle = 1
while reshuffle == 1:
    gen_char_pairs = shuffle(gen_char_pairs)
    for n in range(len(gen_char_pairs)):
        if gen_char_pairs.index[n] == gen_char_pairs['Lure_1'][n] or gen_char_pairs.index[n] == gen_char_pairs['Lure_2'][n]:
            gen_char_pairs = shuffle(gen_char_pairs)
            reshuffle = 1
            break
        elif n == 9:
            reshuffle = 0
        

# create window
#win = visual.Window([1000,600], allowGUI=True, monitor='testMonitor', 
#                    units='norm', color="Gray")
mouse = event.Mouse(win=win)


used_cats = []
lure1_char_used = []
lure2_char_used = []
for character in character_list:
    if event.getKeys(['escape']):
        win.close()  # assumes your visual Window is named win; seems optional
        core.quit()
    # done use subject_stim['Item'].tolist()
    items_already_pres = subject_stim['Item'].tolist() + subject_stim['Lure_1'].tolist() + subject_stim['Lure_2'].tolist()
    
    # Get two random category lures
    lure1_char = gen_char_pairs.loc[character][0]
    lure2_char = gen_char_pairs.loc[character][1]
    lure1 = gen_lure_items.loc[lure1_char,'Lure_1']
    lure2 = gen_lure_items.loc[lure2_char,'Lure_2']
    target = random.choice([x for x in stimulus_key[stimulus_key['Character']==character]['Item'].unique() 
                           if x not in items_already_used])
    #target = random.choice(stimulus_key[stimulus_key['Item']==target]['Stim'].tolist())
    subject_stim.loc[count,'Part'] = 'generalization'
    subject_stim.loc[count,'Character'] = character
    subject_stim.loc[count,'Item'] = target
    subject_stim.loc[count,'Lure_1'] = lure1
    subject_stim.loc[count,'Lure_2'] = lure2
    
    lure1 = random.choice(stimulus_key[stimulus_key['Item']==lure1]['Stim'].tolist())
    lure2 = random.choice(stimulus_key[stimulus_key['Item']==lure2]['Stim'].tolist())
    target = random.choice(stimulus_key[stimulus_key['Item']==target]['Stim'].tolist())
    
    # Present stimuli
    char_stim = Image.open('Finalized_Stimuli/characters/'+
                           [i for i in os.listdir(char_dir)
                           if i.endswith(character+'.png')][0])
    lure1_stim = Image.open(item_dir + lure1_char + '/' + 
                           [i for i in os.listdir(item_dir+lure1_char+'/')
                           if i.startswith(lure1+'.png')][0])
    lure2_stim = Image.open(item_dir + lure2_char + '/' + 
                           [i for i in os.listdir(item_dir+lure2_char+'/')
                           if i.startswith(lure2+'.png')][0])
    target_stim = Image.open(item_dir+character+'/'+ 
                           [i for i in os.listdir(item_dir+character+'/')
                           if i.startswith(target+'.png')][0])
    char_stim.thumbnail(item_size, Image.ANTIALIAS)
    lure1_stim.thumbnail(item_size, Image.ANTIALIAS)
    lure2_stim.thumbnail(item_size, Image.ANTIALIAS)
    target_stim.thumbnail(item_size, Image.ANTIALIAS)
    stim_pos = [[-0.5,-0.6], [0,-0.6], [0.5,-0.6]]
    random.shuffle(stim_pos)
    char_pres = visual.ImageStim(win, char_stim, pos=[0,0.5])
    lure1_pres = visual.ImageStim(win, lure1_stim, pos=stim_pos[0])
    lure2_pres = visual.ImageStim(win, lure2_stim, pos=stim_pos[1])
    target_pres = visual.ImageStim(win, target_stim, pos=stim_pos[2])
    char_pres.draw()
    lure1_pres.draw()
    lure2_pres.draw()
    target_pres.draw()
    win.update()
    
    while True:
        if mouse.isPressedIn(target_pres):
            subject_stim.loc[count,'Answer'] = target
            break
        elif mouse.isPressedIn(lure1_pres):
            subject_stim.loc[count,'Answer'] = lure1
            break
        elif mouse.isPressedIn(lure2_pres):
            subject_stim.loc[count,'Answer'] = lure2
            break

    win.update()
    win.flip()
    fix_pres = scene_pres = visual.ImageStim(win, fixation, pos=[0,0])
    fix_pres.draw()
    win.update()
    core.wait(0.5)
    win.flip()
    count = count + 1
    subject_stim.to_csv('subject_data/test_data.csv')




#win.close()
#core.quit()







### Binding and Pattern Separation

# Binding and pattern separation instructions
for n in range(14,17):
    temp_instr = visual.TextStim(win, instr[n], color='black', pos=[0,0])
    temp_instr.draw()
    win.update()
    core.wait(1)
    win.flip()

win = visual.Window([1000,600], allowGUI=True, monitor='testMonitor', 
                    units='norm', color="Gray")
mouse = event.Mouse(win=win)
encoding_pres_items = subject_stim[subject_stim['Part']=='encoding']

feedback_correct = 'That’s right.'
feedback_incorrect = 'Actually, you saw that friend with this object circled in black.'

random.shuffle(character_list)
for character in character_list:
    if event.getKeys(['escape']):
        win.close()  # assumes your visual Window is named win; seems optional
        core.quit()
    # done use subject_stim['Item'].tolist()
    
    items_already_pres = subject_stim['Item'].tolist() + subject_stim['Lure_1'].tolist() + subject_stim['Lure_2'].tolist()
    
    # Get two random category lures
    binding_lures = random.sample([x for x in stimulus_key[stimulus_key['Character']==character]['Item'].unique() 
                           if x not in items_already_pres],2)
    # Get lure items that were not presented during encoding and set random color
    lure1 = binding_lures[0]
    lure2 = binding_lures[1]
    target = random.choice(encoding_pres_items[encoding_pres_items['Character']==character]['Item'].unique())
    subject_stim.loc[count,'Part'] = 'binding'
    subject_stim.loc[count,'Character'] = character
    subject_stim.loc[count,'Item'] = target
    subject_stim.loc[count,'Lure_1'] = lure1
    subject_stim.loc[count,'Lure_2'] = lure2
    
    
    # Present stimuli
    char_stim = Image.open('Finalized_Stimuli/characters/'+
                           [i for i in os.listdir(char_dir)
                           if i.endswith(character+'.png')][0])
    lure1_stim = Image.open(item_dir+character+'/'+ 
                           [i for i in os.listdir(item_dir+character+'/')
                           if i.startswith(lure1+'_white.png')][0])
    lure2_stim = Image.open(item_dir+character+'/'+ 
                           [i for i in os.listdir(item_dir+character+'/')
                           if i.startswith(lure2+'_white.png')][0])
    target_stim = Image.open(item_dir+character+'/'+ 
                           [i for i in os.listdir(item_dir+character+'/')
                           if i.startswith(target+'_white.png')][0])
    char_stim.thumbnail(item_size, Image.ANTIALIAS)
    lure1_stim.thumbnail(item_size, Image.ANTIALIAS)
    lure2_stim.thumbnail(item_size, Image.ANTIALIAS)
    target_stim.thumbnail(item_size, Image.ANTIALIAS)
    stim_pos = [[-0.5,-0.6], [0,-0.6], [0.5,-0.6]]
    random.shuffle(stim_pos)
    char_pres = visual.ImageStim(win, char_stim, pos=[0,0.5])
    lure1_pres = visual.ImageStim(win, lure1_stim, pos=stim_pos[0])
    lure2_pres = visual.ImageStim(win, lure2_stim, pos=stim_pos[1])
    target_pres = visual.ImageStim(win, target_stim, pos=stim_pos[2])
    char_pres.draw()
    lure1_pres.draw()
    lure2_pres.draw()
    target_pres.draw()
    win.update()
    
    
    while True:
        if mouse.isPressedIn(target_pres):
            subject_stim.loc[count,'Answer'] = target
            temp_instr = visual.TextStim(win, feedback_correct,
                                         color='black', pos=[0,0])
            feedback_circle = visual.Circle(win, radius=0.25, pos=target_pres.pos)
            feedback_circle.lineColor='black'
            feedback_circle.lineWidth=7
            char_pres.draw()
            lure1_pres.draw()
            lure2_pres.draw()
            target_pres.draw()
            temp_instr.draw()
            feedback_circle.draw()
            win.flip()
            core.wait(1)
            break
        elif mouse.isPressedIn(lure1_pres):
            subject_stim.loc[count,'Answer'] = lure1
            temp_instr = visual.TextStim(win, feedback_incorrect,
                                         color='black', pos=[0,0])
            feedback_circle = visual.Circle(win, radius=0.25, pos=target_pres.pos)
            feedback_circle.lineColor='black'
            feedback_circle.lineWidth=7
            char_pres.draw()
            lure1_pres.draw()
            lure2_pres.draw()
            target_pres.draw()
            temp_instr.draw()
            feedback_circle.draw()
            win.flip()
            core.wait(1)
            break
        elif mouse.isPressedIn(lure2_pres):
            subject_stim.loc[count,'Answer'] = lure2
            temp_instr = visual.TextStim(win, feedback_incorrect,
                                         color='black', pos=[0,0])
            feedback_circle = visual.Circle(win, radius=0.25, pos=target_pres.pos)
            feedback_circle.lineColor='black'
            feedback_circle.lineWidth=7
            char_pres.draw()
            lure1_pres.draw()
            lure2_pres.draw()
            target_pres.draw()
            temp_instr.draw()
            feedback_circle.draw()
            win.flip()
            core.wait(1)
            break
    win.update()
    win.flip()
    fix_pres = scene_pres = visual.ImageStim(win, fixation, pos=[0,0])
    fix_pres.draw()
    win.update()
    core.wait(0.5)
    win.flip()
    count = count + 1
    
    
    
    # Pattern Separation
    target_ps = encoding_pres_items[encoding_pres_items['Item']==target]['Color'].iloc[0]
    lures_ps = random.sample([x for x in stimulus_key[stimulus_key['Item']==target]['Stim'] 
                           if x not in target_ps],2)
    lure1_ps = lures_ps[0]
    lure2_ps = lures_ps[1]
    subject_stim.loc[count,'Part'] = 'pattern_separation'
    subject_stim.loc[count,'Character'] = character
    subject_stim.loc[count,'Item'] = target_ps
    subject_stim.loc[count,'Lure_1'] = lure1_ps
    subject_stim.loc[count,'Lure_2'] = lure2_ps
    
    
    lure1_ps_stim = Image.open(item_dir+character+'/'+ 
                           [i for i in os.listdir(item_dir+character+'/')
                           if i.startswith(lure1_ps+'.png')][0])
    lure2_ps_stim = Image.open(item_dir+character+'/'+ 
                           [i for i in os.listdir(item_dir+character+'/')
                           if i.startswith(lure2_ps+'.png')][0])
    target_ps_stim = Image.open(item_dir+character+'/'+ 
                           [i for i in os.listdir(item_dir+character+'/')
                           if i.startswith(target_ps+'.png')][0])
    lure1_ps_stim.thumbnail(item_size, Image.ANTIALIAS)
    lure2_ps_stim.thumbnail(item_size, Image.ANTIALIAS)
    target_ps_stim.thumbnail(item_size, Image.ANTIALIAS)
    stim_pos = [[-0.5,-0.6], [0,-0.6], [0.5,-0.6]]
    random.shuffle(stim_pos)
    char_pres = visual.ImageStim(win, char_stim, pos=[0,0.5])
    lure1_ps_pres = visual.ImageStim(win, lure1_ps_stim, pos=stim_pos[0])
    lure2_ps_pres = visual.ImageStim(win, lure2_ps_stim, pos=stim_pos[1])
    target_ps_pres = visual.ImageStim(win, target_ps_stim, pos=stim_pos[2])
    char_pres.draw()
    lure1_ps_pres.draw()
    lure2_ps_pres.draw()
    target_ps_pres.draw()
    win.update()
    

    while True:
        if mouse.isPressedIn(target_ps_pres):
            subject_stim.loc[count,'Answer'] = target_ps
            break
        elif mouse.isPressedIn(lure1_ps_pres):
            subject_stim.loc[count,'Answer'] = lure1_ps
            break
        elif mouse.isPressedIn(lure2_ps_pres):
            subject_stim.loc[count,'Answer'] = lure2_ps
            break
    win.update()
    win.flip()
    count = count + 1
    fix_pres = scene_pres = visual.ImageStim(win, fixation, pos=[0,0])
    fix_pres.draw()
    win.update()
    core.wait(0.5)
    win.flip()
    subject_stim.to_csv('subject_data/test_data.csv')




win.close()
core.quit()




