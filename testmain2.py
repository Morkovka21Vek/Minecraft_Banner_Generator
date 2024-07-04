import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
import random
from tqdm import tqdm
from numba import njit, prange
import time
import itertools
colors = [[29, 29, 33], [176, 46, 38], [94, 124, 22], [131, 84, 50], [60, 68, 170], [137, 50, 184], [22, 156, 156], [157, 157, 151], 
  [71, 79, 82],[243, 139, 170], [128, 199, 31], [254, 216, 61], [58, 179, 218], [199, 78, 189], [249, 128, 29], [249, 255, 254]]

#sizeImg = (20, 40)

inpPath = input("Укажите пожалуйста полный путь до Вашей картинки 20 на 40: >>>")
inpImg = Image.open(inpPath)
inpImgNp = np.array(inpImg)

@njit(fastmath = True, cache=True)
def closestImageComparison(colorNp1, colorNp2):
    distances = np.sqrt(np.sum((colorNp1-colorNp2)**2))
    return distances

@njit(fastmath = True, cache=True, parallel=True)
def imageComparison(imgNp, GenerateImgNp):
    val = 0
    for x in prange(20):#range(img.size[0]):
        for y in prange(40):#range(img.size[1]):
            Comparison = closestImageComparison(GenerateImgNp[y, x], imgNp[y, x][:3])
            val += Comparison
    return val

files = os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Textures'))
textures = [Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Textures', i)) for i in files]

backgroundImgMask = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "base.png"))#.convert("RGB")
backgroundImgs = []

colorsImgs = [Image.new('RGB',(20, 40),tuple(i)) for i in colors]

total_size = 6553600#len(colorsImgs)*2*len(textures)*len(colorsImgs) #6553600
path_to_save = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')

for color in colorsImgs:
    img = Image.new('RGB',(20, 40),(0,0,0))
    img.paste(color, mask=backgroundImgMask)
    backgroundImgs.append(img)

val = 0

if not os.path.exists(path_to_save):
    os.makedirs(path_to_save)

minComparison = float('inf')
minComparisonImg = None

stTime = time.time()

# allVariants = 0
# for count in prange(1, 3):
#     imgsList = []
#     for _ in range(count):
#         imgsList.append(textures)
#         imgsList.append(colorsImgs)
#     variants = itertools.product(colorsImgs, *imgsList)
#     allVariants += len(list(variants))

# print(allVariants)
for count in prange(1, 3):
    imgsList = []
    for _ in range(count):
        imgsList.append(textures)
        imgsList.append(colorsImgs)
    variants = itertools.product(backgroundImgs, *imgsList)
    list_variants = list(variants)
    total_size = len(list_variants)
    print(f"{count}/2", total_size)
    with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
        #print(len(list_variants))
        for _, Variantval in enumerate(list_variants):
            img = Variantval[0]
            for i in prange(1 ,len(Variantval), 2):
                img.paste(colorsImgs[i+1], mask=textures[i])
            x = imageComparison(inpImgNp, np.array(img))
            if x < minComparison:
                minComparison = x
                minComparisonImg = img
            #val += 1
            progress_bar.update(1)
    print(minComparison)
    minComparisonImg.save(f"outImg_({count}in2).png")

endTime = time.time()
print(total_size, val, endTime-stTime, minComparison)
minComparisonImg.show()
minComparisonImg.save("outImg.png")

#img = Image.new('RGB',(20, 40),(0,0,0))
#imgBackCol = Image.new('RGB',(20, 40),tuple(backCol))
#img.paste(imgBackCol, mask=backgroundImg)