from tensorflow.keras.preprocessing.image import ImageDataGenerator
from data.config import SplitImageDataset as sid
from data.config import TensorRescale as tr


if __name__ == "__main__":
    # Parameters configured in SplitImageDataset 
    train_dir = sid.train_dir
    test_dir = sid.test_dir
    ############################################
    # Parameters configured in TensorRescale 
    batch_size = tr.batch_size
    epochs = tr.epochs
    IMG_HEIGHT = tr.IMG_HEIGHT
    IMG_WIDTH = tr.IMG_WIDTH
    ########################################
    # ImageDataGenerator
    ## Read images from the disk.
    ## Decode contents of these images and convert it into proper grid format as per their RGB content.
    ## Convert them into floating point tensors.
    ## Rescale the tensors from values between 0 and 255 to values between 0 and 1.
    train_image_generator = ImageDataGenerator(rescale=1./255) # No augmentation
    test_image_generator = ImageDataGenerator(rescale=1./255) # No augmentation
    
    # Generate batches of tensor image data with real-time data augmentation.
    # flow_from_directory: load images from directory, rescale and resize
    train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                           directory=train_dir,
                                                           shuffle=True,
                                                           target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                           class_mode='binary')    
    test_data_gen = test_image_generator.flow_from_directory(batch_size=batch_size,
                                                           directory=test_dir,
                                                           shuffle=True,
                                                           target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                           class_mode='binary') 
