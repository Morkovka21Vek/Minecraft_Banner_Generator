import numpy as np
from PIL import Image
colors = [[29, 29, 33], [176, 46, 38], [94, 124, 22], [131, 84, 50], [60, 68, 170], [137, 50, 184], [22, 156, 156], [157, 157, 151], 
  [71, 79, 82],[243, 139, 170], [128, 199, 31], [254, 216, 61], [58, 179, 218], [199, 78, 189], [249, 128, 29], [249, 255, 254]]

def closest(colors,color):
    colorsNp = np.array(colors)
    #color = np.array(color)
    distances = np.sqrt(np.sum((colorsNp-color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))
    #print(index_of_smallest[0][0])
    smallest_distance = colors[index_of_smallest[0][0]]
    return smallest_distance 

inpPath = input("Укажите пожалуйста полный путь до Вашей картинки 21 на 41: >>>")
#inpPath = r"C:\Users\User\Documents\GitHub\Minecraft_Banner_Generator\HSV.png"
img = Image.open(inpPath) 
for x in range(img.size[0]):
    for y in range(img.size[1]):
        #print(*tuple(closest(colors, img.getpixel((x, y)))))
        img.putpixel((x, y), tuple(closest(colors, img.getpixel((x, y))[:3])))
img.save("Hello.png")