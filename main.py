import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
import random
from tqdm import tqdm
colors = [[29, 29, 33], [176, 46, 38], [94, 124, 22], [131, 84, 50], [60, 68, 170], [137, 50, 184], [22, 156, 156], [157, 157, 151], 
  [71, 79, 82],[243, 139, 170], [128, 199, 31], [254, 216, 61], [58, 179, 218], [199, 78, 189], [249, 128, 29], [249, 255, 254]]

#f, axarr = plt.subplots(1, 2)

def closest(colors,color):
    colorsNp = np.array(colors)
    #color = np.array(color)
    distances = np.sqrt(np.sum((colorsNp-color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))
    #print(index_of_smallest[0][0])
    smallest_distance = colors[index_of_smallest[0][0]]
    return smallest_distance 

#inpPath = input("Укажите пожалуйста полный путь до Вашей картинки 20 на 40: >>>")

def reducingColors(inpPath):
	img = Image.open(inpPath) 
	for x in range(img.size[0]):
		for y in range(img.size[1]):
			if len(img.getpixel((x, y))) > 3:
				if img.getpixel((x, y))[3] != 0:
					img.putpixel((x, y), tuple(closest(colors, img.getpixel((x, y))[:3])))
			else:
				img.putpixel((x, y), tuple(closest(colors, img.getpixel((x, y)))))
    #return img

#axarr[0].imshow(reducingColors(inpPath))

files = os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Textures'))
textures = [Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Textures', i)) for i in files]

backgroundImg = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "base.png"))#.convert("RGB")

colorsImgs = [Image.new('RGB',(20, 40),tuple(i)) for i in colors]

total_size = len(colorsImgs)*2*len(textures)*len(colorsImgs)
path_to_save = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

val = 0

if not os.path.exists(path_to_save):
    os.makedirs(path_to_save)

with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
	for imgBackCol in colorsImgs:
		for count in range(1, 2):
			for i in range(count):
				for maskIm in textures:
					for imgCol in colorsImgs:
						progress_bar.update(1)
						img = Image.new('RGB',(20, 40),(0,0,0))
						img.paste(imgBackCol, mask=backgroundImg)
						img.paste(imgCol, mask=maskIm)
						img.save(os.path.join(path_to_save, str(val)+'.jpg'))
						val += 1
		#imgCol = Image.new('RGB',(20, 40),tuple(colors[random.randint(0, len(colors)-1)]))
		#maskIm = textures[random.randint(0, len(textures)-1)]
		#img.paste(imgCol, mask=maskIm)
	#axarr[1].imshow(img)
#plt.show()
print(total_size, val)

#img = Image.new('RGB',(20, 40),(0,0,0))
#imgBackCol = Image.new('RGB',(20, 40),tuple(backCol))
#img.paste(imgBackCol, mask=backgroundImg)