import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.utils import plot_model 
import os
import numpy as np
import matplotlib.pyplot as plt
from contextlib import redirect_stdout
import pandas as pd
import pydot_ng as pydot
import graphviz
from datetime import datetime

def get_local_repository_path(repository_name):
    """
    Return local absolute path from home directory
    to the repository folder (including it).
    Arg.: Name of the repository.
    """
    wd_path = os.getcwd()
    split_wd_path = wd_path.split("/")
    tfm_position = split_wd_path.index(repository_name)
    local_path_split = split_wd_path[:tfm_position+1]
    return "/".join(local_path_split)

def get_timestamp():
    """Get date and time for naming the files"""
    timestamp = datetime.now()
    timestamp_iso = timestamp.isoformat()
    timestamp_iso_seconds = timestamp_iso[:-7] 
    return timestamp_iso_seconds


###########################################################################################
# TO CONFIGURE 
###########################################################################################
# MODEL
model_name = "vgg16_b1b2b3b4_pretrained"
# load pre-trained model with the weights
loaded_model = tf.keras.applications.VGG16()
# layers to freeze in model (limit between frozen and not frozen layers)
limit_layer = 15
# LOCAL PATH
local_path =  get_local_repository_path("tfm")
# IMAGES DATA
img_height = 224 
img_width = 224
color_mode= "rgb"
# MODEL TRAINING
epochs = 500  
steps_per_epoch = 4
# Model description
model_description = f"""
{model_name}
loaded_model = tf.keras.applications.VGG16()
limit_layer = 15
model = Sequential()
for layer in loaded_model.layers[:-1]: 
    model.add(layer)
for layer in model.layers[:limit_layer]:
    layer.trainable = False
for layer in model.layers[limit_layer:]:
    layer.trainable = True
model.add(Dense(len(class_names), activation = "softmax"))
"""

############################################################################################
# PATHS
############################################################################################
# DATA SET DIRECTORIES
source_dir = "data/images/image_preprocessing/processed_images_train_val_test/"
train_dir = os.path.join(local_path, source_dir, "train")
val_dir = os.path.join(local_path, source_dir, "val")
test_dir = os.path.join(local_path, source_dir, "test")

# OUTPUTS
# OUTPUTS
date = get_timestamp()
save_dir = os.path.join(os.path.abspath(os.getcwd()), "outputs", model_name+"_"+date)
# Create outputs folder
if not os.path.exists(save_dir):
    os.makedirs(save_dir, exist_ok=True)

# LABELS
class_names = sorted(os.listdir(train_dir))
print(f"Classes: {class_names}")

# Save model description
with open(os.path.join(save_dir,"model_description.txt"), "w") as file:
    with redirect_stdout(file):
        print(model_description)

############################################################################################
# MODEL CONFIGURATION 
############################################################################################
# MODEL ARCHITECTURE
####################
# Add the layers of model to a new sequential model 
model = Sequential()
for layer in loaded_model.layers[:-1]: # remove last layer
    model.add(layer)
# Rename model
model._name = model_name
model.name
# Freeze the weights in first blocks
for layer in model.layers[:limit_layer]:
    layer.trainable = False
for layer in model.layers[limit_layer:]:
    layer.trainable = True
# Add last layer for categories
model.add(Dense(len(class_names), activation = "softmax"))

# Save model summary
model.summary()
with open(os.path.join(save_dir,"model_summary.txt"), "w") as file:
    with redirect_stdout(file):
        model.summary()

# Plot model architecture and save it as .png
try:
    rankdir = "TB" # TB: vertical; LR: horizontal
    plot_model(model, to_file = os.path.join(save_dir,"model_plot.png"), 
            show_shapes=True, show_layer_names = True, rankdir = rankdir)
except:
    print("Unable to plot model.")
    pass


############################################################################################
# INPUT TRAIN DATASET 
############################################################################################
# CONFIGURATION ImageDataGenerator 
class_mode="categorical"                                  
shuffle=True                                                               
seed = 1234 

# AUGMENTATION
##############
train_datagen = ImageDataGenerator(rescale=1./255,
                                            brightness_range = [0.2,1.5],
                                            zoom_range = [0.5,1.0],
                                            rotation_range=45,
                                            horizontal_flip=True,
                                            vertical_flip=True,
                                            shear_range = 0.2,
                                            fill_mode = "reflect") 

train_array = train_datagen.flow_from_directory(directory = train_dir,
                                            target_size=(img_width, img_height),
                                            color_mode = color_mode,
                                            shuffle = shuffle,
                                            class_mode = class_mode,
                                            #subset = "training",
                                            seed=seed
                                            ) 

############################################################################################
# INPUT VAL DATASET
############################################################################################
val_datagen = ImageDataGenerator(rescale=1./255) 

validation_array = val_datagen.flow_from_directory(val_dir, 
                                                    target_size=(img_width, img_height),
                                                    color_mode = color_mode,
                                                    class_mode= class_mode,
                                                    #subset='validation',
                                                    seed=seed)

############################################################################################
# COMPILING AND FITTING THE MODEL
############################################################################################            
# COMPILING THE MODEL
#####################
# SparseCategoricalCrossentropi directly uses classes labels,
## so that they don't need to be numerically encoded.
optimizer = "sgd" # Options: "sgd", "adam"
model.compile(optimizer=optimizer,
            loss = "categorical_crossentropy",
            metrics=['accuracy'])

# FIT CHECKOUTS
###############
# Early stopping (when loss does not fall anymore to avoid overfitting)
callback = tf.keras.callbacks.EarlyStopping(monitor="val_loss",patience = 30)

# Checkpoint to save model weights and history before it stops training
checkpoint_filepath = os.path.join(save_dir, "/tmp/checkpoint")
model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(filepath = checkpoint_filepath,
                                                              save_weights_only = True,
                                                              monitor= "val_acc",
                                                              save_best_only = True)

# TRAINING THE MODEL
####################
history = model.fit_generator(
    train_array,
    #batch_size = batch_size,
    steps_per_epoch= 4,
    epochs=epochs,
    verbose=1, # get a progress bar and ETA
    validation_data=validation_array,
    validation_steps=2, # batch_size
    callbacks = [callback, model_checkpoint_callback]
)

# Save model history to csv
history_df = pd.DataFrame(history.history) 
history_df.to_csv(os.path.join(save_dir, "model_history.csv"), sep=",", index=False)

# Save model weights
model.save_weights(os.path.join(save_dir, "weights.h5")) 

# EVALUATING MODEL TRAINNING
############################
# Parameters measured during model training
history_dict = history.history
print(history_dict.keys())
try:
    acc = history_dict["acc"]
    val_acc = history_dict["val_acc"]
    loss = history_dict["loss"]
    val_loss = history_dict["val_loss"]
except:
    try:
        acc = history_dict["accuracy"]
        val_acc = history_dict["val_accuracy"]
        loss = history_dict["loss"]
        val_loss = history_dict["val_loss"]
    except:
        pass  

try: 
    epochs_range = range(epochs)
    plt.figure(figsize=(8, 8))
    plt.suptitle(model_name)
    # Accuracy plots
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label="Training Accuracy")
    plt.plot(epochs_range, val_acc, label="Validation Accuracy")
    plt.legend(loc="lower right")
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.title("Training and Validation Accuracy")
    # Loss plots
    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label="Training Loss") 
    plt.plot(epochs_range, val_loss, label="Validation Loss")
    plt.legend(loc="upper right")
    plt.title("Training and Validation Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.savefig(os.path.join(save_dir,"acc_loss_plot.png"))
    plt.show()
except:
    print("Not able to plot accuracy and loss during epochs.")
    pass

print("End.")
