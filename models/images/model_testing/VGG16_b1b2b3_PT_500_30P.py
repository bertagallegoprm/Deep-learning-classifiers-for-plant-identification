#!/usr/bin/env python
# coding: utf-8

# # VGG16_b1b2b3_PT_500_30P

# In[1]:


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


# ## Getting and saving the data

# In[2]:


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


# In[3]:


# CONFIGURE
local_path = get_local_repository_path("tfm")
model_name = "VGG16_b1b2b3_PT_500_30P"


# In[4]:


# DATA SET DIRECTORIES
source_dir = "data/images/image_preprocessing/processed_images_train_val_test/"
train_dir = os.path.join(local_path, source_dir, "train")
val_dir = os.path.join(local_path, source_dir, "val")
test_dir = os.path.join(local_path, source_dir, "test")


# In[5]:


# OUTPUTS
save_dir = os.path.join(os.path.abspath(os.getcwd()), "outputs", model_name)
# Create outputs folder
if not os.path.exists(save_dir):
    os.makedirs(save_dir, exist_ok=True)


# In[6]:


# INPUTS (for the weights)
input_dir = os.path.join(os.path.abspath(os.getcwd()), "inputs")
img_weights = "img_weights_VGG16_b1b2b3PT_500_30P.h5"


# In[7]:


# LABELS
class_names = sorted(os.listdir(train_dir))
print(class_names)


# In[8]:


# EDIT FOR EACH MODEL
# Model description
model_description = f"""
{model_name}

"""

# Save model description
with open(os.path.join(save_dir,"model_description.txt"), "w") as file:
    with redirect_stdout(file):
        print(model_description)


# ## Getting the test datset

# ### Image decodification
# 
# `ImageDataGenerator`:
# 
# - Read images from the disk.
# - Decode images in arrays of float pixel values (here RGB).
# - Rescale the floats in the arrays from values between 0 and 255 to 0 and 1.
# - Perform real-time image augmentation.
# 
# `flow_from_directory`:
# 
# - Generate the batches of array image data (aka tensors) with the real-time data augmentation defined in the `ImageDataGenerator`.
# - Resize the arrays.

# In[9]:


# CONFIGURATION ImageDataGenerator 
img_height = 224 
img_width = 224
color_mode= "rgb"
seed = 1234 


# In[10]:


# Test dataset
test_main_dir = os.path.join(local_path, source_dir)
test_batch_size = len(os.listdir(test_dir)) 
test_datagen = ImageDataGenerator(rescale=1./255)  
test_array = test_datagen.flow_from_directory(directory = test_main_dir,  
                                                    classes = ["test"],
                                                    batch_size = test_batch_size,
                                                    target_size=(img_width, img_height),
                                                    color_mode = color_mode,
                                                    shuffle = False,
                                                    class_mode= None,
                                                    seed=seed) 


# In[11]:


# TEST LABELS
def get_test_labels(test_files):
    """
    Return a list of labels: 
        "Genus_species"
    Arg.: a list of file names with the structure:
          "Genus_species_occurrencenumber.jpg",
          where Genus_species is the class name,   
    """
    test_labels = []
    for i in range(len(test_files)):
        test_file_split = test_files[i].split("_")
        # Remove occurence number and file extension
        class_name_splitted = test_file_split[:-1]
        class_name = "_".join(class_name_splitted)
        test_labels.append(class_name)
    return test_labels


# In[12]:


def test_labels_to_index(test_labels, class_names):
    """
    Return a 1D array of integers with the corresponding
    number for a class.
    Args.: - A list with the class name of each item in 
          the test data set.
           - A sorted list with the possible class names. 
    Eg.: test_labels[1] = "Buxus_sempervirens" corresponds to index 4
         in the list of class names.
    """
    test_labels_index = []
    for i in range(len(test_labels)):
        ind = class_names.index(test_labels[i])
        test_labels_index.append(ind)
    return np.array(test_labels_index)


# In[13]:


test_files = os.listdir(test_dir)
test_labels = get_test_labels(test_files)
test_labels[:5]


# In[14]:


test_labels_index = test_labels_to_index(test_labels, class_names)
test_labels_index[:5]


# ## Loading the model

# In[15]:


loaded_model = tf.keras.applications.VGG16()
model = Sequential()
for layer in loaded_model.layers[:-1]: 
    model.add(layer)
model.add(Dense(len(class_names), activation = "softmax"))
# Load weights
model.load_weights(os.path.join(input_dir, img_weights))


# ### Predict the probability of classifiying each class

# In[ ]:


# Get the probability of predicting each class for each image
predictions = model.predict_generator(test_array,steps=1,verbose=1)


# Predictions is a 2D array with a shape: (number of examples in test, number of classes)

# In[ ]:


predictions.shape


# In[ ]:


# Get predicted class for each example
def predicted_class(predictions):
    """
    Return a 1D array with the predicted class for each example.
    Arg.: 2D array predictions of shape (number of examples, number of classes)
    """
    pred_class = []
    for i in range(len(predictions)):
        higher_prob = max(predictions[i])
        ind, = np.where(np.isclose(predictions[i], higher_prob))
        pred_class.append(ind[0])
    return np.array(pred_class)

pred_class = predicted_class(predictions)


# ### Plot the confussion matrix

# In[ ]:


test_labels_index


# In[ ]:


pred_class


# In[ ]:


# Build the confusion matrix
cm = tf.math.confusion_matrix(test_labels_index, pred_class) 
# Convert from tensor to array
sess = tf.Session()
conf_mat = sess.run(cm)
conf_mat


# In[ ]:


def plot_confusion_matrix(cm, class_names, model_name):
    """
    Returns a matplotlib figure containing the plotted confusion matrix.

    Args:
    cm (array, shape = [n, n]): a confusion matrix of integer classes
    class_names (array, shape = [n]): String names of the integer classes
    """
    figure = plt.figure(figsize=(20, 20))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.BuGn)
    plt.title("Confusion matrix - "+ model_name, fontsize = 22)
    plt.colorbar()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names, rotation=90)
    plt.yticks(tick_marks, class_names)
    plt.savefig(os.path.join(save_dir,"conf_matrix.png"))


# In[ ]:


plot_confusion_matrix(conf_mat, np.array(class_names), model_name)

