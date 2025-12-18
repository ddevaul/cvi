import cv2 
import numpy as np
import os
import json
from tqdm import tqdm

def calculate_roundness_and_stuff(img_file: str):

  new_obj = {}
  area = 0
  y_bar = 0
  x_bar = 0
  img = cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)
  for y in range(0, img.shape[0]):
    for x in range(0, img.shape[1]):
      if img[y][x] == 255:
        area += 1
        y_bar += y 
        x_bar += x
  x_bar = x_bar / area
  y_bar = y_bar / area
  a = 0
  b = 0
  c = 0
  for y in range(0, img.shape[0]):
    for x in range(0, img.shape[1]):
      if img[y][x] == 255:
          a += np.pow((x-x_bar), 2)
          c += np.pow((y - y_bar), 2)
          b += (x - x_bar) * (y - y_bar)
        
  b *= 2
  theta1 = np.arctan2(b, (a-c)) / 2
  e1 = a * np.pow(np.sin(theta1), 2) - b * np.sin(theta1) * np.cos(theta1) + c * np.pow(np.cos(theta1), 2)

  theta2 = np.arctan2(-b, (c-a)) / 2
  
  e2 = a * np.pow(np.sin(theta2), 2) - b * np.sin(theta2) * np.cos(theta2) + c * np.pow(np.cos(theta2), 2)

  new_obj['centroid_xy'] = [x_bar, y_bar]
  new_obj['area'] = area
  e_min = None 
  e_max = None
  if e1 < e2: 
      new_obj['E_min'] = e1
      new_obj['orientation'] = np.degrees(theta1)
      e_min = e1 
      e_max = e2
  else: 
      new_obj['E_min'] = e2
      new_obj['orientation'] = np.degrees(theta2)
      e_min = e2
      e_max = e1
  
  new_obj['roundness'] = e_min / e_max
  return new_obj 

def go_thru_images():
  img_dir = "./plant_images_plant_masks"
  imgs = os.listdir(img_dir)
  img_stuff = []
  for img in tqdm(imgs):
     roundness = calculate_roundness_and_stuff(f"{img_dir}/{img}")
     roundness["file"] = img
     img_stuff.append(roundness)
  with open("voynich_plant_roundness.json", "w") as f:
     json.dump(img_stuff, f, indent=2)

go_thru_images()