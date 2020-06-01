import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_acc_loss(acc,val_acc,loss,val_loss,epochs):
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
    print("acc_loss_plot.png created")


if __name__ == "__main__":
    # This file must be run from the same directory
    # where the model script or notebook is stored
    # -it searches for the path "outputs/model_name/model_history.csv"
    # PATHS ##############################################
    model_name = input("Enter model name: ")
    local_path = os.path.abspath(os.getcwd()) # run from repository main folder
    repository_path = os.path.join(local_path, "models", "images", "experiments", "plain_scripts")
    source_dir = os.path.join(local_path,repository_path, "outputs", model_name)
    save_dir = os.path.join(local_path, repository_path, "outputs", model_name)
    ######################################################
    try:
        history_df = pd.read_csv(os.path.join(source_dir, "model_history.csv"))
        history_dict = history_df.to_dict()
    except:
        print("Unable to open model_history.csv.")
        raise

    try: # the key names vary across tf versions
        acc = np.array(list(history_dict["acc"].values()))
        val_acc = np.array(list(history_dict["val_acc"].values()))
        loss = np.array(list(history_dict["loss"].values()))
        val_loss = np.array(list(history_dict["val_loss"].values()))
        epochs = len(acc)
        epochs_range = np.array(range(epochs))
    except:
        try:
            acc = np.array(list(history_dict["accuracy"].values()))
            val_acc = np.array(list(history_dict["val_accuracy"].values()))
            loss = np.array(list(history_dict["loss"].values()))
            val_loss = np.array(list(history_dict["val_loss"].values()))
            epochs = len(acc)
            epochs_range = np.array(range(epochs))
        except:
            pass
    plot_acc_loss(acc,val_acc,loss,val_loss,epochs)
    print("End.")