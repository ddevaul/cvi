from skimage import morphology
import cv2
import matplotlib.pyplot as plt
import numpy as np

image = cv2.imread("../../extracted_images/page35.jpeg")
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
k = 2
_, binary_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)
processed_img = morphology.binary_dilation(binary_image, morphology.disk(k))
processed_img = morphology.binary_dilation(binary_image, morphology.disk(k))

plt.imshow(processed_img, cmap="gray")
plt.show()
# processed_img = morphology.binary_erosion(processed_img, morphology.disk(k))
# processed_img = morphology.binary_erosion(processed_img, morphology.disk(k))

plt.imshow(processed_img, cmap="gray")
plt.show()
# print(processed_img)
print(processed_img.shape)
red = image[:,:, 0]
green = image[:,:, 1]
blue = image[:,:, 2]
im2 = image.copy()
# processed_img = processed_img.astype(np.uint8) * 250
im2[processed_img] = 0
plt.imshow(im2)
plt.show()
contours, hierarchy = cv2.findContours(processed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
big_contours = []
return_image = image.copy()
for contour in contours:
  if cv2.contourArea(contour) > 200:

    x, y, w, h = cv2.boundingRect(contour)
    # red_mean = np.mean(rect_img[:, :, 0])
    # green_mean = np.mean(rect_img[:, :, 1])
    # blue_mean = np.mean(rect_img[:, :, 2])
    short = min(w, h)
    long = max(w, h)
    # if (long / short) < 10:
    big_contours.append(contour)
    return_image = cv2.rectangle(return_image, (x,y), (x+w, y+h), (0, 255,0 ), 20)


# image_with_contours = cv2.drawContours(image, contours, -1, (0,255,0), 3)

# plt.imshow(image_with_contours)
plt.imshow(return_image)
plt.show()