#!/bin/bash -x

############################################################################################################################################################
#                                                                                                                                                          #
#                                                               Author: Mehdi Zare                                                                         #
#                                                                                                                                                          #
#               Purpose : It converts HISTORY file to the number of images and each image is in xyz format, which are the inputs of Rot-Corr-Time code 	   #
#		Note    : This code assume that your (HISTORY, head.CONFIG, Divide-History.py) in your current directory  				   #
#                                                                                                                                                          #
############################################################################################################################################################
./Divide-History.py << EOF
cont
2500
1
EOF


NumConf=`head -2 HISTORY | tail -1 | awk '{print $4}'`                   # Total number of conformations in HISTORY
lines=`head -2 HISTORY | tail -1 | awk '{print $5}'`                     # Total number of HISTORY's lines
OneConf=$((($lines-2)/$NumConf))                                         # Number of line in one conformation without header
OneConfhead=$(($OneConf+2))						 # Number of line in one conformation with header
OneCONFIG=$(($OneConf-4))   					         # one conformation that we need for CONFIG file(we do not need 4 lines of HISTORY)

j=1
for i in {00001..02500};do  tail -n$OneCONFIG HISTORY.$j > image-$i
cat head.CONFIG image-$i > CONFIG-$i

dlpoly-relocate-config-coordinates -f CONFIG-$i > ali-1
dlpoly-convert-config-to-geometry-xyz -f ali-1 -k 0 -p > image-$i

rm  ali-1 CONFIG-$i

j=$(($j+1))

done

rm HISTORY.*


