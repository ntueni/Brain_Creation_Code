import sys
import os

#define project root (main folder which contains the subfolders _pycache_, common, ... IOput, mesh, personalscripts etc. and the python files _init_, ArrayProcessor, brain_creation, BrainHexMesh etc.)
project_root = r"C:\Users\pumab\Documents\Brain_Creation_Code-17-region-model_2"
os.chdir(project_root)
# Add project root to the search path in order to find all modules
sys.path.append(project_root)
print("Project Root:", project_root)

# Module Import
import brain_creation
from config.Config import ConfigFile
import writers.HeterogeneityConverter as heterogConverter
from readers.Readers import Reader
from personal_scripts.create_prms import CreateAtrophyPRM, CreateTumorPRM

from ucd_processing import process_UCD_extension 
from ucd_processing import process_UCD_column_remove
from ucd_processing import convert_to_vtk

# Model type options: basic_fullcsf, basic_partilacsf, basic_nocsf, atrophy, lesion

####### ATROPHY CODE #######
# Absoluter Pfad zu den Eingabe- und Ausgabeordnern sowie zur Konfigurationsdatei und dem Template
path_to_oasis   = os.path.join(project_root, "IOput", "in")
print("Path in:", path_to_oasis)
file_name_in    = "aparc_DKTatlas+aseg.mgz"
path_to_out     = os.path.join(project_root, "IOput", "out", "atrophy_files")
print("Path to Out:", path_to_out)
config_file_path = os.path.join(project_root, "IOput", "model_config.ini")
template_prm_path = os.path.join(project_root, "personal_scripts", "atrophy_template_folder", "atrophy_template_V2.prm")

filenames = ["rampp"] #change name of the output folder here
for name in filenames:
    path_in = path_to_oasis
    path_out = "/".join([path_to_out, name])
    file_name_out = name
    
    config = ConfigFile(path_in, file_name_in, path_out, file_name_out,
                        configFilePath="./IOput/model_config.ini", model_type='atrophy')
    mesh = brain_creation.run(config)
    mesh.write(path_out, file_name_out, ['vtk','ucd'])
    # UNCOMMENT THE FOUR LINES BELOW AND COMMENT OUT LINES 21-24 inkl. IF YOU HAVE AN INPUT FIL ETO READ AND DON'T WANT TO CREATE A NEW MESH
    # reader = Reader('vtk')
    # reader.openReader(file_name_out + "_VTK", path_out)
    # mesh = reader.getMesh()
    # reader.closeReader()

    conditioning = 'preconditioned'
    poissons = '0,49'
    for heterogeneity_model in [heterogConverter.Heterogeneity.ONER, heterogConverter.Heterogeneity.TWOR, heterogConverter.Heterogeneity.FOURR,
                                heterogConverter.Heterogeneity.NINER]:
    # for heterogeneity_model in [hc.Heterogeneity.NINETEENR]:

        atrophy_creator = CreateAtrophyPRM("./personal_scripts/atrophy_template_folder/atrophy_template_V2.prm")
        atrophy_creator.create_materials(mesh, conditioning, poissons, heterogeneity_model)
        atrophy_creator.write_materials()
        atrophy_creator.complete_prm(path_out, file_name_out, "{}_atrophy_{}R".format(file_name_out, heterogeneity_model.value))
        output_prm = "/".join([path_out, "{}_atrophy_{}R".format(file_name_out, heterogeneity_model.value)])
        atrophy_creator.write_prm(output_prm)
        atrophy_creator.close_prm()

    # change add and remove columns for the final output files
    input_file_extension = os.path.join(path_out, "rampp_UCD.inp")
    output_file_extension = os.path.join(path_out, "rampp_UCD1.inp")
    process_UCD_extension(input_file_extension, output_file_extension)

    
    input_file_column = os.path.join(path_out, "rampp_UCD.inp")
    output_file_column = os.path.join(path_out, "rampp_UCD_orig.inp")
    process_UCD_column_remove(input_file_column, output_file_column)

    input_file_column = os.path.join(path_out, "rampp_UCD1.inp")
    output_file_column = os.path.join(path_out, "rampp_UCD_FA.inp")
    process_UCD_column_remove(input_file_column, output_file_column)

    input_file = os.path.join(path_out, "rampp_UCD_FA.inp")
    output_file = os.path.join(path_out, "rampp_VTK_FA.vtk")
    convert_to_vtk(input_file, output_file)

    print("COMPLETE")
    print("Files written to",path_out)

# ####################################################################################################################
# # ####### TUMOR LESION CODE #######
# path_to_files_in = "C:/Users/grife/OneDrive/Documents/PostDoc/BrainModels/OASIS/OASIS-1/oasis_cs_freesurfer_disc1.tar/oasis_cs_freesurfer_disc1/disc1"
# file_name_in = "aparc_DKTatlas+aseg.mgz"
# path_to_out = "../IOput/out/tumor_files"
# # filenames = ["Silvia_brain"]
# filenames = ["OAS1_0002_MR1", "OAS1_0004_MR1", "OAS1_0005_MR1", "OAS1_0006_MR1", "OAS1_0007_MR1", "OAS1_0009_MR1"]
# for name in filenames:
#     path_in = "/".join([path_to_oasis, name, "mri"])
#     path_out = "/".join([path_to_out, name])
#     file_name_out = name
#
#     config = ConfigFile(path_in, file_name_in, path_out, file_name_out,
#                         configFilePath="../IOput/model_config.ini", model_type='lesion')
#     mesh = brain_creation.run(config)
#     mesh.write(path_out, file_name_out, ['vtk', 'ucd'])
#     # UNCOMMENT THE FOUR LINES BELOW AND COMMENT OUT LINES 61-64 inkl. IF YOU HAVE AN INPUT FIL ETO READ AND DON'T WANT TO CREATE A NEW MESH 
#     # reader = Reader('vtk')
#     # reader.openReader(file_name_out + "_VTK", path_out)
#     # mesh = reader.getMesh()
#     # reader.closeReader()
#
#     conditioning = 'preconditioned'
#     poissons = '0,49'
#     for heterogeneity_model in [heterogConverter.Heterogeneity.ONER, heterogConverter.Heterogeneity.TWOR, heterogConverter.Heterogeneity.FOURR,
#                                 heterogConverter.Heterogeneity.NINER]:
#         # heterogeneity_model = hc.Heterogeneity.ONER
#
#         tumor_creator = CreateTumorPRM("./tumor_template_folder/tumor_growth_template.prm")
#         tumor_creator.create_materials(mesh, conditioning, poissons, heterogeneity_model)
#         tumor_creator.write_materials()
#         tumor_creator.complete_prm(path_out, file_name_out, "{}_tumor_{}R".format(file_name_out, heterogeneity_model.value))
#         output_prm = "/".join([path_out, "{}_tumor_{}R".format(file_name_out, heterogeneity_model.value)])
#         tumor_creator.write_prm(output_prm)
#         tumor_creator.close_prm()
#
#     print("COMPLETE")
#     print("Files written to", path_out)
