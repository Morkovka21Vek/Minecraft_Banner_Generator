from PIL import Image
import os
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Textures")
imgs_Path = os.listdir(path)
for imgPath in imgs_Path:
    img = Image.open(os.path.join(path, imgPath))
    img = img.crop((0, 0, 21, 41))
    img.save(os.path.join(path, imgPath))