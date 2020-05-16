import os
from data.images.image_preprocessing.crop import crop_image_pil


def remove_files(directory, file_list):
    """
    Given a path to a directory and a list of files,
    remove them from directory.
    """
    count = 0
    for file in file_list:
        try:
            os.remove(os.path.join(directory,file))   
            count +=1
        except:
            print(f"Unable to remove image {file}")
    print(f"{count} files removed.")


def faulty_images_list():
    return [
        "Acer_campestre/Acer_campestre_2236810424.jpg", # not a plant
        "Acer_campestre/Acer_campestre_2236813636.jpg", # not a plant

        "Alnus_glutinosa/Alnus_glutinosa_2446322730.jpg", # not a plant
        "Alnus_glutinosa_2515848856.jpg", # wrong species

        "Buxus_sempervirens/Buxus_sempervirens_2513370351.jpg", # not a plant

        "Carpinus_betulus/Carpinus_betulus_1701389889.jpg", # wrong species

        "Cornus_sanguinea/Cornus_sanguinea_2513371631.jpg", # not a plant
        "Cornus_sanguinea/Cornus_sanguinea_2513371720.jpg", # not a plant
        "Cornus_sanguinea/Cornus_sanguinea_2513374477.jpg", # not a plant

        "Corylus_avellana/Corylus_avellana_2236812926.jpg", # not a plant
        "Corylus_avellana/Corylus_avellana_2446322403.jpg", # not a plant

        "Crataegus_monogyna/Crataegus_monogyna_2236812276.jpg", # not a plant

        "Fraxinus_excelsior/Fraxinus_excelsior_2457123235.jpg", # not a plant
        "Fraxinus_excelsior/Fraxinus_excelsior_2236813420.jpg", # not a plant
        "Fraxinus_excelsior/Fraxinus_excelsior_2457113234.jpg", # not a plant
        "Fraxinus_excelsior/Fraxinus_excelsior_2457124237.jpg", # not a plant
        "Fraxinus_excelsior/Fraxinus_excelsior_2515551394.jpg", # no leaves or fruits

        "Ilex_aquifolium/Ilex_aquifolium_2513365947.jpg", # not a plant
        "Ilex_aquifolium/Ilex_aquifolium_2513367739.jpg", # not a plant
        "Ilex_aquifolium/Ilex_aquifolium_2513367739.jpg", # not a plant
        "Ilex_aquifolium/Ilex_aquifolium_2513368768.jpg", # not a plant

        "Pinus_sylvestris/Pinus_sylvestris_1949283642.jpg", # not a plant  

        "Populus_tremula/Populus_tremula_1055575024.jpg", # wrong species

        "Prunus_avium/Prunus_avium_2513392312.jpg", # not a plant
        "Prunus_avium/Prunus_avium_2513393273.jpg", # not a plant       
        "Prunus_avium/Prunus_avium_2513393461.jpg", # not a plant 
        "Prunus_avium/Prunus_avium_2513445275.jpg", # not a plant
        "Prunus_avium/Prunus_avium_2513447478.jpg", # not a plant


        "Quercus_robur/Quercus_robur_2236812883.jpg", # not a plant       
        "Quercus_robur/Quercus_robur_2236813162.jpg", # not a plant 
        "Quercus_robur/Quercus_robur_1935989152.jpg", # covered by label

        "Salix_caprea/Salix_caprea_2236813594.jpg", # not a plant       
        "Salix_caprea/Salix_caprea_2236813594.jpg", # wrong cropping 

        "Salix_viminalis/Salix_viminalis_2236813677.jpg", # not a plant       
        "Salix_viminalis/Salix_viminalis_2236814213.jpg", # not a plant 

        "Taxus_baccata/Taxus_baccata_574678811.jpg", # not a herbarium sheet   

        "Tilia_x_europaea/Tilia_x_europaea_2236814175.jpg", # not a plant   
        "Tilia_x_europaea/Tilia_x_europaea_2457118221.jpg", # wrong cropping  

        "Ulmus_procera/Ulmus_procera_2236814366.jpg" # not a plant 
    ]

if __name__ == "__main__":

    # SOURCE DIR
    base_path = "data/images/image_preprocessing/"
    directory = "cropped_images"
    source_dir = os.path.join(base_path, directory)

    # DESTINATION DIR (keep in the last saved images)
    base_path = "data/images/image_preprocessing/"
    directory = "cropped_images"
    destination_dir = os.path.join(base_path, directory)

    # List of faulty images
    faulty_images = faulty_images_list()
    print(f"{len(faulty_images)} faulty images")

    # Remove faulty images
    remove_files(source_dir,faulty_images)


    # # Recrop some images
    # crop_image_pil(os.path.join(base_path, "resized_images", "Betula_pubescens"),
    #                os.path.join(destination_dir, "Betula_pubescens"),
    #                 , 
    #                 crop_coords)
