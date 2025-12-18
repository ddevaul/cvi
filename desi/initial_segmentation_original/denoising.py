from skimage import morphology
import cv2
import matplotlib.pyplot as plt
import numpy as np

image = cv2.imread("../../extracted_images/page35.jpeg")
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
k = 3
_, binary_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)
processed_img = morphology.binary_dilation(binary_image, morphology.disk(k))
# processed_img = morphology.binary_dilation(binary_image, morphology.disk(k))
processed_img = morphology.binary_erosion(processed_img, morphology.disk(k))
processed_img = morphology.binary_dilation(binary_image, morphology.disk(k))
# processed_img = morphology.binary_dilation(binary_image, morphology.disk(k))
processed_img = morphology.binary_erosion(processed_img, morphology.disk(k))
# processed_img = morphology.binary_erosion(processed_img, morphology.disk(k))

# processed_img = morphology.binary_erosion(processed_img, morphology.disk(k))

im2 = image.copy()
im2[:,:,0][processed_img] = 255
im2[:,:,1][processed_img] = 255
im2[:,:,2][processed_img] = 255

plt.imshow(im2)
plt.show()