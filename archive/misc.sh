

# Rename files with underscores instead of spaces
for file in *; do mv "$file" `echo $file | tr ' ' '_'` ; done


mogrify -format png *.psd
for pic in *.psd; do


mogrify -format png *
for f in ./*; do mv "$f" "${f%-0.png}.png" ; done
for f in ./*; do rm "$f" "${f%-0.png}.png" ; done



for f in art chef doctor farm fashion furniture insect music sport vehicle; do 
    #mogrify -format png ${f}/*
    cd ${f}
    for a in ./*; do mv "$a" "${a%.png.png}.png" ; done
    #rm *.png.png
    cd ../
done





mri_label2vol --seg $SUBJECTS_DIR/$subject/mri/aseg.mgz \
              --reg $SUBJECTS_DIR/$subject/mri/transforms/reg.mni152.2mm.dat \
              --o aseg.$subject.mni152.nii