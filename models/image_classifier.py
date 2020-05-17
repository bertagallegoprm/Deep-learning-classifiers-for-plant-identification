import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
import os
import matplotlib.pyplot as plt
from models.config import SplitImageDataset as sid
from models.config import ImageGenerator as ig


def plotImages(images_arr):
    fig, axes = plt.subplots(1, 5, figsize=(20,20))
    axes = axes.flatten()
    for img, ax in zip( images_arr, axes):
        ax.imshow(img)
        ax.axis('off')
    plt.tight_layout()
    plt.show()


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
    train_datagen = ImageDataGenerator(rescale=1./255,
                                                rotation_range=45,
                                                width_shift_range=.15,
                                                height_shift_range=.15,
                                                horizontal_flip=True,
                                                zoom_range=0.5,
                                                validation_split = 0.16)  
    # Generate batches of tensor image data with real-time data augmentation.
    # flow_from_directory: load images from directory, rescale and resize
    train_generator = train_datagen.flow_from_directory(directory = train_dir,
                                                target_size=(img_width, img_height),
                                                color_mode = color_mode,
                                                batch_size = batch_size,                                                       
                                                shuffle = shuffle,
                                                class_mode = class_mode,
                                                subset = "training",
                                                seed=seed
                                                               ) 
    validation_generator = train_datagen.flow_from_directory(train_dir,  # same directory as training data
                                                        target_size=(img_width, img_height),
                                                        batch_size=batch_size,
                                                        class_mode= class_mode,
                                                        subset='validation',
                                                        seed=seed) # set as validation data 

    # Creating the model
    ## The number of output channels for each Conv2D layer is controlled by the first argument (e.g., 32 or 64).
    ## Typically, as the width and height shrink, you can afford (computationally) to add more output channels in each Conv2D layer
    # For each example the model returns a vector of "logits" or "log-odds" scores, one for each class.
    # The tf.nn.softmax function converts these logits to "probabilities" for each class
    array_size = img_width*img_height
    dense_size = 128 # converts the 1d_array_size to a dense_size activations using a weight matrix of size * 1d_array_size and a bias matrix of size.
    num_classes = 42
    kernel_size = 3,3 # number of convolutional filters (width*height of the filter mask)
    padding = "same" # case insensitive. Other option: "valid"
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv2D(3,3, activation = "relu", padding=padding, input_shape = (28, 28,3)))
    model.add(tf.keras.layers.Dense(num_classes, activation = "softmax"))
    model.build()

    # Compiling the model
    # SparseCategoricalCrossentropi directly uses classes labels,
    ## so that they don't need to be numerically encoded.
    optimizer = "sgd" # Options: "sgd", "adam"
    model.compile(optimizer=optimizer,
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

    # Model summary
    model.summary()


    #Training the model
    history = model.fit_generator(
        train_generator,
        steps_per_epoch=3, # batch_size,
        epochs=15,
        verbose=1, # get a progress bar and ETA
        validation_data=validation_generator,
        validation_steps=2 # batch_size
    )



