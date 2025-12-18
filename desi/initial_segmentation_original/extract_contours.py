import cv2 
import numpy as np
import matplotlib.pyplot as plt 
import os

def contour_image(img_path: str):

	image = cv2.imread(img_path)
	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(gray_image, 127, 255, 0)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		# for i, contour in enumerate(contours):
		#   im = cv2.drawContours(image, contours, i, (0,255,0), 3)
		#   area = cv2.contourArea(contour)
		#   if area < 100:
		#     continue
		#   print(area)
		#   plt.imshow(im)
		#   plt.show()

	big_contours = []
	return_image = image.copy()
	for contour in contours:
		if cv2.contourArea(contour) > 1000 and cv2.contourArea(contour) > 50:

			x, y, w, h = cv2.boundingRect(contour)
			# red_mean = np.mean(rect_img[:, :, 0])
			# green_mean = np.mean(rect_img[:, :, 1])
			# blue_mean = np.mean(rect_img[:, :, 2])
			short = min(w, h)
			long = max(w, h)
			# if (long / short) < 10:
			big_contours.append(contour)
			return_image = cv2.rectangle(return_image, (x,y), (x+w, y+h), (0, 255,0 ), 20)
				# plt.imshow(rect_img)
				# plt.show()
	
	# image_with_contours = cv2.drawContours(image, cv2.bonbig_contours, -1, (0,255,0), 3)
	# plt.imshow(image_with_contours)
	# plt.show()
				
	return return_image

def main():
	files = os.listdir("../plant_images")
	for f in files:
		contoured_image = contour_image(f"../plant_images/{f}")
		plt.imshow(contoured_image)
		plt.show()

main()