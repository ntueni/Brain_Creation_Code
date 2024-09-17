import brain_creation
from config.Config import ConfigFile
import writers.HeterogeneityConverter as heterogConverter
from readers.Readers import Reader
from personal_scripts.create_prms import CreateAtrophyPRM, CreateTumorPRM

# Model type options: basic_fullcsf, basic_partilacsf, basic_nocsf, atrophy, lesion

####### ATROPHY CODE #######
# CHANGE ACCORDING TO PERSONAL DRIVES
path_to_oasis = " path to data directory "
file_name_in = "aparc_DKTatlas+aseg.mgz"
path_to_out = "../IOput/out/atrophy_files"
filenames = ["OAS1_0002_MR1", "OAS1_0004_MR1", "OAS1_0005_MR1", "OAS1_0006_MR1", "OAS1_0007_MR1","OAS1_0009_MR1"]
for name in filenames:
    path_in = "/".join([path_to_oasis, name, "mri"])
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
