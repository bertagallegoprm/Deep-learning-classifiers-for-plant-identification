from matplotlib import image
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage
from PIL import Image


im = image.imread("cropped.jpg")
print(im.shape)
print(im)
im = im.astype("float32") # convert pixels from in to float
im /=255.0 # rescale pixels 0-1
print(im)



# n = 10
# l = 256
# im = np.zeros((l, l))
# np.random.seed(1)
# points = l*np.random.random((2, n**2))
# im[(points[0]).astype(np.int), (points[1]).astype(np.int)] = 1
# im = scipy.ndimage.gaussian_filter(im, sigma=l/(4.*n))
# im = im.astype("float32")
# im /=255.0

mask = (im > im.mean()).astype(np.float)
# mask += 0.1 * im
# img = mask + 0.2*np.random.randn(*mask.shape)

# hist, bin_edges = np.histogram(img, bins=60)
# bin_centers = 0.5*(bin_edges[:-1] + bin_edges[1:])

# binary_img = img > 0.5

# # img = Image.fromarray(binary_img, 'RGB')
# image.imsave("mask.jpg", img)