import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import numpy as np


images = [
    'page30.jpeg',  
    'erbario-00015.jpg',
    'img5.jpg',
    'page35.jpeg',
    'erbario-00034.jpg',
    'img10.jpg'
]

labels = [
    'Voynich page 30',
    'Erbario page 15',
    'Tractatus page 5',
    'Voynich page 35',
    'Erbario page 34',
    'Tractatus page 10'
]

target_size = (500, 700)
resized_images = []
for img_path in images:
    img = Image.open(img_path)
    img_resized = img.resize(target_size, Image.LANCZOS)
    resized_images.append(np.array(img_resized))

fig, axes = plt.subplots(2, 3, figsize=(7, 6))
axes = axes.flatten()

for i, (img, label) in enumerate(zip(resized_images, labels)):
    axes[i].imshow(img)
    axes[i].set_title(label)
    axes[i].axis('off')

plt.tight_layout()
plt.savefig('voynich_figure.png', dpi = 300, bbox_inches = 'tight')
plt.show()