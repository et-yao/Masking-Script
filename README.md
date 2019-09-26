# Masking-Script
Combination of two scripts I wrote for my URAP project that together help speed up the process of masking for photogrammetry automation. It's certainly easier than the manual option. See Readme for running details.


#To Run

Step 1: Run calibration.py with command line argument. Argument should be the image you want to use as calibration base
Step 2: Adjust HSV sliders until the mask looks right (i.e. the left screen should have the object filled in black). It's ok if there's noise.
Step 3: Hit "s" to save the values, the values will be saved to arrays.txt.
Step 4: Run script_test.py with two arguments. First argument is the file header - i.e. "1-213799_s3". Do NOT add the _###.tex. Second argument is the number id of the last file.
Step 5: You should be done.