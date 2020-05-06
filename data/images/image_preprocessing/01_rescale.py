from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
from data.config import SplitImageDataset as sid
from data.config import ImageGenerator as ig


if __name__ == "__main__":
    # Parameters configured in SplitImageDataset 
    train_dir = sid.train_dir
    val_dir = sid.val_dir
    test_dir = sid.test_dir
    ############################################
    # Parameters configured in ImageGenerator 
    color_mode= ig.color_mode
    img_height = ig.img_height
    img_width = ig.img_width  
    class_mode= ig.class_mode
    batch_size = ig.batch_size
    epochs = ig.epochs                                   
    shuffle = ig.shuffle                                                             
    seed = ig.seed
    # Parameters for test dataset 
    test_batch_size = 1

    ########################################
    # ImageDataGenerator
    ## Read images from the disk.
    ## Decode contents of these images and convert it into proper grid format as per their RGB content.
    ## Convert them into floating point tensors.
    ## Rescale the tensors from values between 0 and 255 to values between 0 and 1.
    train_image_generator = ImageDataGenerator(rescale=1./255) # No augmentation
    val_image_generator = ImageDataGenerator(rescale=1./255) # No augmentation
    test_image_generator = ImageDataGenerator(rescale=1./255)
    
    # Generate batches of tensor image data with real-time data augmentation.
    # flow_from_directory: load images from directory, rescale and resize
    train_data_gen = train_image_generator.flow_from_directory(directory = train_dir,
                                                               target_size =(img_height, img_width),
                                                               color_mode = color_mode,
                                                               batch_size = batch_size,                                                       
                                                               shuffle = shuffle,
                                                               class_mode = class_mode,
                                                               seed=seed
                                                               ) 
    val_data_gen = val_image_generator.flow_from_directory(directory = val_dir,
                                                               target_size =(img_height, img_width),
                                                               color_mode = color_mode,
                                                               batch_size = batch_size,                                                       
                                                               shuffle = shuffle,
                                                               class_mode = class_mode,
                                                               seed=seed
                                                               )  
    test_data_gen = test_image_generator.flow_from_directory(directory = test_dir,
                                                            target_size =(img_height, img_width),
                                                            color_mode = color_mode,
                                                            batch_size = test_batch_size,                                                       
                                                            shuffle = False,
                                                            class_mode = None,
                                                            seed=seed
                                                            )  


