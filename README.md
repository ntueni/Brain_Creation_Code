This project was started by Emma Griffiths ca. 2023 and continued by Nicole Tueni (see branches).

The code to create a model is found in the file 'create_model' in the 'personal_scripts' folder. Uncomment sections '####### ATROPHY CODE #######' and '####### TUMOR LESION CODE #######' as necessary. This code will both create a mesh from the MRI images and create the prm files according to the heterogeneity level specified. In creating the prm files the volume average of the mesh is used to create homogenized material properties.

To run a new brain creation code you need the following files: 1. The aparc segmented file from FreeSurfer. Please change the file name to 'aparc_DKTatlas+aseg.mgz' 2. The brain stem segmented file from Freesurfer. Please change the file name to 'brainstemSsLabels.mgz'

You will also need to change the location of the input files 'path_in' in lines 17 and 57 in "create_model". All files will be created in the a folder with their name found in the '/IOput/out/atrophy_files' or '/IOput/out/tumor_files' folder.

## Modifications ##
- Fixed problem with homogenization function
- Possible to get 1R - 2R - 4R - 9R and 17R models with updated material parameters
- run python3 -i -m personal_scripts.create_model in Brain_Creation_Code directory

