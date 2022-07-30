from turtle import backward
from webbrowser import BackgroundBrowser
from PIL import Image
import PIL
import time
import math
import numpy as np
import random

def save(img, name):
    img.save(name + ".png", "PNG")

def open(imgname):
    return Image.open(imgname)

def load(image):
    return image.load()

def distance(c1,c2):
    r1,g1,b1 = c1
    r2,g2,b2 = c2
    return math.sqrt(((r2-r1)**2+(g2-g1)**2+(b2-b1)**2))
    
def matrix_create(img):
    img_colors = img.convert('RGB')
    img_colorpixels = load(img_colors)
    width = img.size[0]
    height = img.size[1]
    res = np.array(np.zeros((width,height)), dtype=tuple)
    for x in range(width):
        for y in range(height):
            res[y, x] = img_colorpixels[x,y]
    return res

def colorset_create(matrix_img):
    res = set()
    for i in matrix_img:
        for j in i:
            if j not in res:
                res.add(j)
    return res
    
def distance3d(c1,c2):
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    return math.sqrt((r2-r1)**2 + (g2-g1)**2 + (b2-b1)**2)

def closest(colorlist, n):
    dist = -1
    for i in colorlist:
        if i != n:
            if dist < 0 or distance3d(n,i) <= dist:
                dist = distance3d(n,i)
                closesti = i
    return closesti

def chain_center(chain):
    xtotal = 0
    ytotal = 0
    ztotal = 0
    for coord in chain:
        x,y,z = coord
        xtotal += x
        ytotal += y
        ztotal += z
    return (int(xtotal/len(chain)),int(ytotal/len(chain)),int(ztotal/len(chain)))

def cluster_centers(colorlist):
    chains = []
    subchain = set()
    for i in colorlist:
        if not any(i in sublist for sublist in chains):
            chaincheck = i
            while closest(colorlist, chaincheck) not in subchain and not any(closest(colorlist, chaincheck) in sublist2 for sublist2 in chains):
                chaincheck = closest(colorlist, chaincheck)
                subchain.add(chaincheck)
            subchain.add(i)
            chains.append(subchain)
            subchain = set()
    print('Simplified down to', len(chains), 'colors.')
    chain_centers = [chain_center(chain) for chain in chains]
    return chain_centers

def closestcolor(c, colorset):
    if c in colorset:
        return c
    mindist = 500
    for color in colorset:
        dist = distance(c, color)
        if dist < mindist:
            mindist = dist
            mincolor = color
    return mincolor

def huelistcheck(c, huelist, threshold):
    if c in huelist:
        return True
    for hue in huelist:
        if distance3d(c, hue) < threshold:
            return True
    return False

def colorsimplifymain():
    a = False
    while not a:
        imgname = input('Image file name: ')
        try:
            img = open(imgname)
            a = True
        except FileNotFoundError:
            print('File not found (either doesn\'t exist, is not in this folder, or has a different format, try again)')
    cont = 'again'
    count = 0
    start = time.time()
    matrix = matrix_create(img)
    colorset = colorset_create(matrix)
    end = time.time()
    print('Matrix and color set created in ' + str(round(end-start, 2)) + ' seconds.')
    print('There are', len(colorset), 'different colors of pixels in this image.')
    width = img.size[0]
    height = img.size[1]
    start = time.time()
    colorlist = cluster_centers(colorset)
    while len(colorlist) > 10:
        len1 = len(colorlist)
        colorlist = cluster_centers(colorlist)
        print("Dropped to", len(colorlist), "clusters from", str(len1), 'in', time.time() - start, "seconds.")
    end = time.time()
    print('Cluster centers dropped down to', len(colorlist), 'in', round(end-start,2), ' seconds total.')
    while cont == '' or cont not in 'stop|dont|end|close|done':
        end = time.time()
        print('Clusters hues (0 to', str(len(colorlist) - 1) + '):')
        print(colorlist)
        print('Choose cluster hues to keep:')
        clusterchoose = True
        keep = set()
        kept = ''
        backchoose = True
        thresholdinput = True
        while clusterchoose == True:
            huecheck = True
            while huecheck:
                hueind = input('Hue number (type \'done\' if that\'s all): ')
                if hueind != "" and hueind in "stop|no|dont|done":
                    clusterchoose = False
                    huecheck = False
                else:
                    try:
                        hueind = int(hueind)
                        keep.add(colorlist[hueind])
                        print(keep)
                        kept += str(hueind)
                        huecheck = False
                    except:
                        print("Enter a valid number please.")
        while backchoose:
            backr = input("Background Color R Value: ")
            backg = input("Background Color G Value: ")
            backb = input("Background Color B Value: ")
            try:
                backr = int(backr)
                backg = int(backg)
                backb = int(backb)
                res = PIL.Image.new(mode = "RGB", size = (width, height), color = (backr, backg, backb))
                backchoose = False
            except:
                print("Enter valid RGB values please")
        res_pixels = load(res)
        while thresholdinput:
            try:
                threshold = abs(int(input("Enter tolerance threshold: ")))
                thresholdinput = False
            except:
                print("Enter valid threshold")
        for x in range(width):
            for y in range(height):
                if huelistcheck(matrix[y, x], keep, threshold):
                    res_pixels[x,y] = matrix[y, x]
        save(res, imgname[:-4] + '_Simplified_' + kept + '_' + str(threshold))
        start = time.time()
        print('Created', imgname[:-4] + '_Simplified_' + kept + '_' + str(threshold) + '.png in', round(start-end, 2), 'seconds.')
        count += 1
        cont = input('Simplify again?: ')

colorsimplifymain()
a = input()
