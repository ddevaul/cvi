import json 
import matplotlib.pyplot as plt
import cv2
import math
import pickle as pkl

prompt = "plant"


with open(f"closest_images_embeddings_{prompt}.pkl", "rb") as f:
  closest_imgs = pkl.load(f)

# erbario
# closest_imgs.sort(reverse=True, key=lambda t: t[3])
# tractatus
closest_imgs.sort(reverse=True, key=lambda t: t[4])

for o in closest_imgs:
  v_f = o[0]['file'].split(".")[0]
  e_f = o[1]['file'].split(".")[0]
  t_f = o[2]['file'].split(".")[0]
  print(v_f, e_f, t_f)
  v_pg = v_f.split("_")[0]
  e_pg = e_f.split("_")[0]
  t_pg = t_f.split("_")[0]
  voynich_file = f"plant_images_{prompt}_cleaned/{v_f}.jpeg"
  erbario_file = f"erbario_plant_images_{prompt}_cleaned/{e_f}.jpeg"
  tractatus_file = f"tractatus_plant_images_{prompt}_cleaned/{t_f}.jpeg"
  v = cv2.imread(voynich_file, cv2.IMREAD_COLOR)
  e = cv2.imread(erbario_file, cv2.IMREAD_COLOR)
  t = cv2.imread(tractatus_file, cv2.IMREAD_COLOR)
  fig, axs = plt.subplots(1, 2)
  axs[0].imshow(v)
  v_pg = v_f.split("_")[0]
  axs[0].set_title(f"Voynich {v_pg}")
  axs[1].imshow(t)
  t_pg = t_f.split("_")[0]
  axs[1].set_title(f"Tractatus {t_pg}")
  # axs[1].imshow(e)
  # axs[1].set_title(e_f)

  plt.show()
