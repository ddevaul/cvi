import json 
import matplotlib.pyplot as plt
import cv2
import math

prompt = "plant"

with open(f"closest_{prompt}.json", "r") as f:
  closest_imgs = json.load(f)

closest_imgs.sort(reverse=False, key=lambda c: abs(c['voynich']['roundness'] - c['erbario']['roundness']))

for o in closest_imgs:
  v_f = o['voynich']['file'].split(".")[0]
  e_f = o['erbario']['file'].split(".")[0]
  t_f = o['tractatus']['file'].split(".")[0]
  voynich_file = f"plant_images_{prompt}_cleaned/{v_f}_cleaned.jpeg"
  erbario_file = f"erbario_plant_images_{prompt}_cleaned/{e_f}_cleaned.jpeg"
  tractatus_file = f"tractatus_plant_images_{prompt}_cleaned/{t_f}_cleaned.jpeg"
  v = cv2.imread(voynich_file, cv2.IMREAD_COLOR)
  e = cv2.imread(erbario_file, cv2.IMREAD_COLOR)
  t = cv2.imread(tractatus_file, cv2.IMREAD_COLOR)
  fig, axs = plt.subplots(1, 2)
  axs[0].imshow(v)
  v_pg = v_f.split("_")[0]
  axs[0].set_title(f"Voynich {v_pg}")
  # axs[1].imshow(t)
  # t_pg = t_f.split("_")[0]
  # axs[1].set_title(f"Tractatus {t_pg}")
  axs[1].imshow(e)
  axs[1].set_title(e_f)
  plt.show()
