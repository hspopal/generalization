# Generalization Task

## Script descriptions
* RUN_GENERALIZATION.sh
    * A bash script that allows you to run the generalization scripts like a program
    * Make this file executable, place it on your desktop, and double-click to start the generalization "program"
* init_generalization.py
    * This script runs the initial gui for the program where you can enter the subject ID, the date, and the block order
* generalization.py
    * This script is the meat of the program, where psychopy is used to run the task

## Directory Structure

GENERALIZATION/ <br>
├── Block_1 <br>
│   ├── characters <br>
│   ├── encoding <br>
│   └── individual_items <br>
├── Block_2 <br>
├── scripts <br>
└── subject_data <br>
    └── dev_testing <br>

* Block_1 and Block_2
   * Contains all of the stimuli for each respective block.
   * Inside the "characters" subdirectory is images of each character with the syntax of each file being {character_name}_{category}.png
   * Inside of the "encoding" subdirectory is images of all the scenes for all the characters with the syntax of each file being {category}_encoding_{#}.png
   * The individual_items directory has subdirectories with category names. Then inside each category subdirectory, are pictures of the respective items, which every color iteration in the format {item}_{color}.png

* scripts
This directory is this GitHub repo. 
* subject_data
This directory is where all of the subject data will be outputted. There is also a subdirectory for subject data from development testing (so you can output data while you are testing your stimuli and any coding changes. 
