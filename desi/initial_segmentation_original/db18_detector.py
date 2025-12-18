import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def detect(file_name: str, detector):

	
	img_size = (2560, 2560)
	image = cv2.imread(file_name)
	image = cv2.resize(image, img_size)
	img_mean = np.mean(image, axis=(0,1))

	detector.setInputParams(1.0/255, img_size, img_mean, True)


	boxes, _ = detector.detect(image)

	image_with_boxes = image.copy()

	for box in boxes:
		cv2.polylines(image_with_boxes, [box], True, (0, 255,0), 2)

	plt.imshow(image_with_boxes)
	plt.show()
	print(boxes)

def main():
	files = os.listdir("../plant_images")
	detector = cv2.dnn_TextDetectionModel_DB("DB_TD500_resnet18.onnx")
	detector.setBinaryThreshold(0.4)
	detector.setPolygonThreshold(0.5)
	for f in files:
		contoured_image = detect(f"../plant_images/{f}", detector)
		plt.imshow(contoured_image)
		plt.show()

main()