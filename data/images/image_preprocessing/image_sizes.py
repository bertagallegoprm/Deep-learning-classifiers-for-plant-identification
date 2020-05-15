from PIL import Image
import os
import statistics
import matplotlib.pyplot as plt


def get_image_sizes(source_dir):
    """
    Return a list of lists with 
    (image_width, image_height)
    for every image in the directory
    and classes subdirectories.
    """
    img_sizes = []
    if os.path.exists(source_dir):
        for species_folder in os.listdir(source_dir):
            for image_file in os.listdir(os.path.join(source_dir, species_folder)):
                try:
                    image_obj = Image.open(os.path.join(source_dir, species_folder, image_file))
                    img_width, img_height = image_obj.size
                    img_sizes.append([img_width,img_height])                  
                except:
                    print(f"Unable to open {image_file}.")
                    pass
    else:
        print(f"Folder {source_dir} not found.")
    print("End.")
    return img_sizes


def get_widths(img_sizes):
    widths = []
    for size in img_sizes:
        widths.append(size[0])
    return widths


def get_heights(img_sizes):
    heights = []
    for size in img_sizes:
        heights.append(size[1])
    return heights 


def show_image_statistics(img_sizes):
    print(f"Bigger: {max(img_sizes)}")
    print(f"Smaller: {min(img_sizes)}")
    widths = get_widths(img_sizes)
    heights = get_heights(img_sizes)
    print(f"Average width: {round(sum(widths)/len(widths))}, stdev: {round(statistics.stdev(widths))}")
    print(f"Average height, stdev: {round(sum(heights)/len(heights))}, stdev: {round(statistics.stdev(heights))}")
    print(f"Median width: {statistics.median(widths)}")
    print(f"Median height: {statistics.median(heights)}")
    print(f"Count width below 1000 px: {sum(i < 1000 for i in widths)} of {len(widths)}")
    print(f"Count height below 2000 px: {sum(i < 1000 for i in heights)} of {len(heights)}")


def plot_image_dimensions(img_sizes):
    widths = get_widths(img_sizes)
    heights = get_heights(img_sizes)
    plt.scatter(widths, heights, alpha=0.8, color="grey", marker="o", s=2)
    plt.xlabel("Image widths (px)", fontsize=8)
    plt.ylabel("Image heights (px)", fontsize=8)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)


def plot_dimension_distribution(img_sizes):
    widths = get_widths(img_sizes)
    heights = get_heights(img_sizes)
    #fig, ax = plt.subplots()
    plt.hist([widths,heights], bins = 40, alpha = 0.5, 
             color=["lightgrey","lightblue"], 
             edgecolor="grey", label=["Width","Height"])
    plt.ylabel("Frequency (px)", fontsize=8)
    plt.xlabel("Image widths / heights (px)", fontsize=8)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.legend()


def plot_image_sizes(img_sizes, destination_path):
    fig, axs = plt.subplots(2)
    fig.suptitle('Image sizes')
    plt.subplot(2,1,1)
    plot_image_dimensions(img_sizes)
    plt.subplot(2,1,2)
    plot_dimension_distribution(img_sizes)
    plt.savefig(destination_path)


if __name__ == "__main__":

    # SOURCE images
    source_dir = "data/images/raw_images"

    img_sizes = get_image_sizes(source_dir)
    show_image_statistics(img_sizes)

    # DESTINATION plot
    destination_path = "data/images/image_preprocessing/image_sizes.png"
    plot_image_sizes(img_sizes, destination_path)
