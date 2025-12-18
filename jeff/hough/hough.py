import cv2
import matplotlib.pyplot as plt
import os
import numpy as np
import math
import cmath

if __name__ == "__main__":

    # Init vars
    downscale_height = 1
    downscale_width = 1

    # Load image
    img = cv2.imread('erbario-00001.jpg')
    # Downsize for processing
    img_height, img_width = img.shape[:2]
    new_height = int(img_height / downscale_height)
    new_width = int(img_width / downscale_width)
    new_dimensions = (new_width, new_height)
    #img = cv2.resize(img, new_dimensions, interpolation=cv2.INTER_AREA)
    img_height, img_width = img.shape[:2]

    # Convert img to gray and find edges
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_canny = cv2.Canny(img_gray, 150, 200)
    cv2.imwrite("canny_img.png", img_canny)


    # Load template
    template_mask = cv2.imread('erbario-00001_1.jpeg', cv2.IMREAD_GRAYSCALE)
    _, template_mask = cv2.threshold(template_mask, 127, 255, cv2.THRESH_BINARY)
    # Expand mask by 5 pixels in all directions
    pixels = 5
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (pixels*2+1, pixels*2+1))
    new_mask = cv2.dilate(template_mask, kernel, iterations=1)


    #template = img_canny.copy()
    #template = np.where(new_mask, template, 0)

    # Use mask to copy img edges, including inner edges
    template_mask = new_mask
    contours, _ = cv2.findContours(template_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(contours[0])
    template_edges_cropped = img_canny[y:y+h, x:x+w]
    template_mask_cropped = template_mask[y:y+h, x:x+w]
    template = cv2.bitwise_and(template_edges_cropped, template_edges_cropped, mask=template_mask_cropped)
    template_height, template_width = template.shape


    cv2.imwrite("canny_temp.png", template)
    
    # Downsize for processing
    #template_height, template_width = template.shape[:2]
    #new_height = int(template_height / downscale_height)
    #new_width = int(template_width / downscale_width)
    #new_dimensions = (new_width, new_height)
    #img = cv2.resize(template, new_dimensions, interpolation=cv2.INTER_AREA)

    # Using only outer edges # Comment below out to use inner edgess
    template_gray = cv2.imread('erbario-00001_1.jpeg', cv2.IMREAD_GRAYSCALE)
    template = cv2.Canny(template_gray, 150, 200)
    template = cv2.Canny(new_mask, 150, 200)
    ########################################

    cv2.imwrite("canny_temp.png", template)


    # Create Hough 
    ght = cv2.createGeneralizedHoughGuil()
    #ght.setTemplate(template_canny)
    ght.setTemplate(template)
    # Set parmams
    # Angle
    ght.setMinAngle(0)
    ght.setMaxAngle(360)
    ght.setAngleStep(1)
    ght.setAngleEpsilon(1)
    # Scale
    ght.setMinScale(0.8)
    ght.setMaxScale(1.2)
    ght.setScaleStep(0.05)
    # Thresholds
    ght.setAngleThresh(500)
    ght.setScaleThresh(500)
    ght.setPosThresh(100)
    # Misc
    ght.setLevels(360)
    ght.setMinDist(25)
    #ght.setXi(90)


    positions = ght.detect(img_canny)

    if positions[0] is not None and positions[0].size > 0:
    
        if len(positions[0].shape) == 3:
            num_detections = positions[0].shape[1]
            print(f"\nFound {num_detections} detections:")
            
            result_img = img.copy()
            
            for i in range(num_detections):
                center_x = int(positions[0][0, i, 0])
                center_y = int(positions[0][0, i, 1])
                scale = float(positions[0][0, i, 2])
                angle = float(positions[0][0, i, 3])
                detected_width = int(template_width * scale)
                detected_height = int(template_height * scale)
                
                print(f"\nDetection {i+1}:")
                print(f"  Position: ({center_x}, {center_y})")
                print(f"  Scale: {scale:.3f}")
                print(f"  Angle: {angle:.1f}")
                
                rect = ((center_x, center_y), (detected_width, detected_height), angle)
                box = cv2.boxPoints(rect)
                box = np.int32(box)
                
                cv2.drawContours(result_img, [box], 0, (0, 255, 0), 2)
                cv2.circle(result_img, (center_x, center_y), 8, (0, 0, 255), -1)
            
            cv2.imwrite("results.jpg", result_img)
    else:
        print("No detections found!")
