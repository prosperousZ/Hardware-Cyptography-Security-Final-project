import numpy as np
from PIL import Image
import cv2
import sys
import os


def generateCMYK(path, name):
  image = Image.open(path)

  outfile_1 = Image.new("CMYK", [dimension for dimension in image.size])
  outfile_2 = Image.new("CMYK", [dimension for dimension in image.size])
  outfile_s = Image.new("CMYK", [dimension for dimension in image.size])

  for x in range(0, image.size[0], 1):
    for y in range(0, image.size[1], 1):
      pixel = image.getpixel((x, y))
      outfile_1.putpixel((x, y), (pixel[0], 0, 0, 0))
      outfile_2.putpixel((x, y), (0, pixel[1], 0, 0))
      outfile_s.putpixel((x, y), (0, 0, pixel[2], 0))

  outfile_1.save("outputs/CMYK_" + name + "_C.jpg")
  outfile_2.save("outputs/CMYK_" + name + "_M.jpg")
  outfile_s.save("outputs/CMYK_" + name + "_Y.jpg")


def generateHalftone(name):
  image_C = Image.open("outputs/CMYK_" + name + "_C.jpg").convert('1')
  image_M = Image.open("outputs/CMYK_" + name + "_M.jpg").convert('1')
  image_Y = Image.open("outputs/CMYK_" + name + "_Y.jpg").convert('1')

  hf = Image.new("CMYK", [dimension for dimension in image_C.size])

  for x in range(0, image_C.size[0]):
    for y in range(0, image_C.size[1]):
      pixel_C = image_C.getpixel((x, y))
      pixel_M = image_M.getpixel((x, y))
      pixel_Y = image_Y.getpixel((x, y))

      hf.putpixel((x, y), (pixel_C, pixel_M, pixel_Y, 0))

  hf.save("outputs/Halftone_" + name + ".jpg")


def generateExtraction(name):
  image = Image.open("outputs/Halftone_" + name + ".jpg")
  
  dimx = int(image.size[0]/2)+1
  
  extraction = Image.new("CMYK", [dimx, image.size[1]])

  for x in range(0, image.size[0], 1):
    for y in range(0, image.size[1], 1):
      if x%2 == 0:
        extraction.putpixel((int(x/2), y), image.getpixel((x, y)))
           
  extraction.save("outputs/Extraction_" + name + ".jpg")
 

def applyCCT(pixel, mode):
  cct = Image.new("CMYK", [2, 2])
  #print(pixel) 
  # pixel is black
  if pixel[0] > 200 and pixel[1] > 200 and pixel[2] > 200:
    cct.putpixel((0, 0), (255, 255, 255, 0))
    cct.putpixel((0, 1), (255, 255, 255, 0))
    cct.putpixel((1, 0), (255, 255, 255, 0))
    cct.putpixel((1, 1), (255, 255, 255, 0))
  
  # pixel is blue 
  elif pixel[0] > 200 and pixel[1] > 200 and pixel[2] < 100:
    if mode == 1:
      cct.putpixel((0, 0), (255, 255, 0, 0))
      cct.putpixel((0, 1), (255, 255, 255, 0))
      cct.putpixel((1, 0), (255, 255, 255, 0))
      cct.putpixel((1, 1), (255, 255, 0, 0))
    else:
      cct.putpixel((0, 0), (255, 255, 255, 0))
      cct.putpixel((0, 1), (255, 255, 0, 0))
      cct.putpixel((1, 0), (255, 255, 0, 0))
      cct.putpixel((1, 1), (255, 255, 255, 0))
         
  # pixel is green 
  elif pixel[0] > 200 and pixel[1] < 100 and pixel[2] > 200:
    if mode == 1:
      cct.putpixel((0, 0), (255, 0, 255, 0))
      cct.putpixel((0, 1), (255, 255, 255, 0))
      cct.putpixel((1, 0), (255, 255, 255, 0))
      cct.putpixel((1, 1), (255, 0, 255, 0))
    else:
      cct.putpixel((0, 0), (255, 255, 255, 0))
      cct.putpixel((0, 1), (255, 0, 255, 0))
      cct.putpixel((1, 0), (255, 0, 255, 0))
      cct.putpixel((1, 1), (255, 255, 255, 0))

  # pixel is cyan 
  elif pixel[0] > 200 and pixel[1] < 100 and pixel[2] < 100:
    if mode == 1:
      cct.putpixel((0, 0), (255, 0, 0, 0))
      cct.putpixel((0, 1), (255, 255, 255, 0))
      cct.putpixel((1, 0), (255, 255, 255, 0))
      cct.putpixel((1, 1), (255, 0, 0, 0))
    else:
      cct.putpixel((0, 0), (255, 255, 255, 0))
      cct.putpixel((0, 1), (255, 0, 0, 0))
      cct.putpixel((1, 0), (255, 0, 0, 0))
      cct.putpixel((1, 1), (255, 255, 255, 0))
  
  # pixel is red 
  elif pixel[0] < 100 and pixel[1] > 200 and pixel[2] > 200:
    if mode == 1:
      cct.putpixel((0, 0), (0, 255, 255, 0))
      cct.putpixel((0, 1), (255, 255, 255, 0))
      cct.putpixel((1, 0), (255, 255, 255, 0))
      cct.putpixel((1, 1), (0, 255, 255, 0))
    else:
      cct.putpixel((0, 0), (255, 255, 255, 0))
      cct.putpixel((0, 1), (0, 255, 255, 0))
      cct.putpixel((1, 0), (0, 255, 255, 0))
      cct.putpixel((1, 1), (255, 255, 255, 0))

  # pixel is Magenta 
  elif pixel[0] < 100 and pixel[1] > 200 and pixel[2] < 100:
    if mode == 1:
      cct.putpixel((0, 0), (0, 255, 0, 0))
      cct.putpixel((0, 1), (255, 255, 255, 0))
      cct.putpixel((1, 0), (255, 255, 255, 0))
      cct.putpixel((1, 1), (0, 255, 0, 0))
    else:
      cct.putpixel((0, 0), (255, 255, 255, 0))
      cct.putpixel((0, 1), (0, 255, 0, 0))
      cct.putpixel((1, 0), (0, 255, 0, 0))
      cct.putpixel((1, 1), (255, 255, 255, 0))

  # pixel is yellow
  elif pixel[0] < 100 and pixel[1] < 100 and pixel[2] > 200:
    if mode == 1:
      cct.putpixel((0, 0), (0, 0, 255, 0))
      cct.putpixel((0, 1), (255, 255, 255, 0))
      cct.putpixel((1, 0), (255, 255, 255, 0))
      cct.putpixel((1, 1), (0, 0, 255, 0))
    else:
      cct.putpixel((0, 0), (255, 255, 255, 0))
      cct.putpixel((0, 1), (0, 0, 255, 0))
      cct.putpixel((1, 0), (0, 0, 255, 0))
      cct.putpixel((1, 1), (255, 255, 255, 0))

  # pixel is white
  else:
    if mode == 1:
      cct.putpixel((0, 0), (0, 0, 0, 0))
      cct.putpixel((0, 1), (255, 255, 255, 0))
      cct.putpixel((1, 0), (255, 255, 255, 0))
      cct.putpixel((1, 1), (0, 0, 0, 0))
    else:
      cct.putpixel((0, 0), (255, 255, 255, 0))
      cct.putpixel((0, 1), (0, 0, 0, 0))
      cct.putpixel((1, 0), (0, 0, 0, 0))
      cct.putpixel((1, 1), (255, 255, 255, 0))

  return cct


def applySCT(pixel):
  sct_1 = Image.new("CMYK", [2, 2])
  sct_2 = Image.new("CMYK", [2, 2])
  
  sct_1.putpixel((0, 0), (0, 0, 255, 0))
  sct_1.putpixel((1, 0), (255, 0, 0, 0))
  sct_1.putpixel((0, 1), (0, 0, 0, 0))
  sct_1.putpixel((1, 1), (0, 255, 0, 0))
  
  # pixel is black
  if pixel[0] > 200 and pixel[1] > 200 and pixel[2] > 200:
    sct_2.putpixel((0, 0), (0, 255, 0, 0))
    sct_2.putpixel((1, 0), (0, 0, 0, 0))
    sct_2.putpixel((0, 1), (255, 0, 0, 0))
    sct_2.putpixel((1, 1), (0, 0, 255, 0))
  
  # pixel is blue 
  elif pixel[0] > 200 and pixel[1] > 200 and pixel[2] < 100:
    sct_2.putpixel((0, 0), (0, 0, 255, 0))
    sct_2.putpixel((1, 0), (0, 255, 0, 0))
    sct_2.putpixel((0, 1), (0, 0, 0, 0))
    sct_2.putpixel((1, 1), (255, 0, 0, 0))
         
  # pixel is green 
  elif pixel[0] > 200 and pixel[1] < 100 and pixel[2] > 200:
    sct_2.putpixel((0, 0), (255, 0, 0, 0))
    sct_2.putpixel((1, 0), (0, 0, 255, 0))
    sct_2.putpixel((0, 1), (0, 0, 0, 0))
    sct_2.putpixel((1, 1), (0, 255, 0, 0))

  # pixel is cyan 
  elif pixel[0] > 200 and pixel[1] < 100 and pixel[2] < 100:
    sct_2.putpixel((0, 0), (0, 0, 255, 0))
    sct_2.putpixel((1, 0), (0, 0, 0, 0))
    sct_2.putpixel((0, 1), (255, 0, 0, 0))
    sct_2.putpixel((1, 1), (0, 255, 0, 0))
  
  # pixel is red 
  elif pixel[0] < 100 and pixel[1] > 200 and pixel[2] > 200:
    sct_2.putpixel((0, 0), (0, 255, 0, 0))
    sct_2.putpixel((1, 0), (255, 0, 0, 0))
    sct_2.putpixel((0, 1), (0, 0, 0, 0))
    sct_2.putpixel((1, 1), (0, 0, 255, 0))

  # pixel is Magenta 
  elif pixel[0] < 100 and pixel[1] > 200 and pixel[2] < 100:
    sct_2.putpixel((0, 0), (0, 0, 255, 0))
    sct_2.putpixel((1, 0), (255, 0, 0, 0))
    sct_2.putpixel((0, 1), (0, 255, 0, 0))
    sct_2.putpixel((1, 1), (0, 0, 0, 0))

  # pixel is yellow
  elif pixel[0] < 100 and pixel[1] < 100 and pixel[2] > 200:
    sct_2.putpixel((0, 0), (0, 0, 0, 0))
    sct_2.putpixel((1, 0), (255, 0, 0, 0))
    sct_2.putpixel((0, 1), (0, 0, 255, 0))
    sct_2.putpixel((1, 1), (0, 255, 0, 0))

  # pixel is white
  else:
    sct_2.putpixel((0, 0), (0, 0, 255, 0))
    sct_2.putpixel((1, 0), (255, 0, 0, 0))
    sct_2.putpixel((0, 1), (0, 0, 0, 0))
    sct_2.putpixel((1, 1), (0, 255, 0, 0))

  return (sct_1, sct_2)


def generateShares():
  image_1 = Image.open("outputs/Extraction_1.jpg").convert("CMYK")
  image_2 = Image.open("outputs/Extraction_2.jpg").convert("CMYK")
  image_s = Image.open("outputs/Extraction_s.jpg").convert("CMYK")

  share_1 = Image.new("CMYK", [image_1.size[0]*4, image_1.size[1]*2])
  share_2 = Image.new("CMYK", [image_1.size[0]*4, image_1.size[1]*2])


  for x in range(0, image_1.size[0], 1):
    for y in range(0, image_1.size[1], 1):
      #print("x = " + str(x) + ", y = " + str(y) + " , mode = 1")
      cct_1 = applyCCT(image_1.getpixel((x, y)), 1)
      #print("x = " + str(x) + ", y = " + str(y) + " , mode = 2")
      cct_2 = applyCCT(image_2.getpixel((x, y)), 2)
      sct_1, sct_2 = applySCT(image_s.getpixel((x, y)))

      # odd row
      if x%2 == 1:
        share_1.putpixel((4*x, 2*y), cct_1.getpixel((0, 0)))
        #print(cct_1.getpixel((0, 0)))
        #print("-----------")
        share_1.putpixel((4*x, 2*y+1), cct_1.getpixel((0, 1)))
        share_1.putpixel((4*x+1, 2*y), cct_1.getpixel((1, 0)))
        share_1.putpixel((4*x+1, 2*y+1), cct_1.getpixel((1, 1)))
        
        share_1.putpixel((4*x+2, 2*y), sct_1.getpixel((0, 0)))
        share_1.putpixel((4*x+2, 2*y+1), sct_1.getpixel((0, 1)))
        share_1.putpixel((4*x+3, 2*y), sct_1.getpixel((1, 0)))
        share_1.putpixel((4*x+3, 2*y+1), sct_1.getpixel((1, 1)))

        share_2.putpixel((4*x, 2*y), cct_2.getpixel((0, 0)))
        share_2.putpixel((4*x, 2*y+1), cct_2.getpixel((0, 1)))
        share_2.putpixel((4*x+1, 2*y), cct_2.getpixel((1, 0)))
        share_2.putpixel((4*x+1, 2*y+1), cct_2.getpixel((1, 1)))
        
        share_2.putpixel((4*x+2, 2*y), sct_2.getpixel((0, 0)))
        share_2.putpixel((4*x+2, 2*y+1), sct_2.getpixel((0, 1)))
        share_2.putpixel((4*x+3, 2*y), sct_2.getpixel((1, 0)))
        share_2.putpixel((4*x+3, 2*y+1), sct_2.getpixel((1, 1)))
     
      # even row
      else:
        share_1.putpixel((4*x, 2*y), sct_1.getpixel((0, 0)))
        share_1.putpixel((4*x, 2*y+1), sct_1.getpixel((0, 1)))
        share_1.putpixel((4*x+1, 2*y), sct_1.getpixel((1, 0)))
        share_1.putpixel((4*x+1, 2*y+1), sct_1.getpixel((1, 1)))
        
        share_1.putpixel((4*x+2, 2*y), cct_1.getpixel((0, 0)))
        share_1.putpixel((4*x+2, 2*y+1), cct_1.getpixel((0, 1)))
        share_1.putpixel((4*x+3, 2*y), cct_1.getpixel((1, 0)))
        share_1.putpixel((4*x+3, 2*y+1), cct_1.getpixel((1, 1)))

        share_2.putpixel((4*x, 2*y), sct_2.getpixel((0, 0)))
        share_2.putpixel((4*x, 2*y+1), sct_2.getpixel((0, 1)))
        share_2.putpixel((4*x+1, 2*y), sct_2.getpixel((1, 0)))
        share_2.putpixel((4*x+1, 2*y+1), sct_2.getpixel((1, 1)))
        
        share_2.putpixel((4*x+2, 2*y), cct_2.getpixel((0, 0)))
        share_2.putpixel((4*x+2, 2*y+1), cct_2.getpixel((0, 1)))
        share_2.putpixel((4*x+3, 2*y), cct_2.getpixel((1, 0)))
        share_2.putpixel((4*x+3, 2*y+1), cct_2.getpixel((1, 1)))

  share_1.save("outputs/Share_1.jpg")
  share_2.save("outputs/Share_2.jpg")


def generateOurShares():
  image_1 = Image.open("outputs/Halftone_1.jpg").convert("CMYK")
  image_2 = Image.open("outputs/Halftone_2.jpg").convert("CMYK")
  image_s = Image.open("outputs/Halftone_s.jpg").convert("CMYK")

  share_1 = Image.new("CMYK", [image_1.size[0]*4, image_1.size[1]*4])
  share_2 = Image.new("CMYK", [image_1.size[0]*4, image_1.size[1]*4])


  for x in range(0, image_1.size[0], 1):
    for y in range(0, image_1.size[1], 1):
      #print("x = " + str(x) + ", y = " + str(y) + " , mode = 1")
      cct_1 = applyCCT(image_1.getpixel((x, y)), 1)
      #print("x = " + str(x) + ", y = " + str(y) + " , mode = 2")
      cct_2 = applyCCT(image_2.getpixel((x, y)), 2)
      sct_1, sct_2 = applySCT(image_s.getpixel((x, y)))

      # odd row
      if x%2 == 1:
        share_1.putpixel((4*x, 4*y), cct_1.getpixel((0, 0)))
        share_1.putpixel((4*x, 4*y+1), cct_1.getpixel((0, 1)))
        share_1.putpixel((4*x+1, 4*y), cct_1.getpixel((1, 0)))
        share_1.putpixel((4*x+1, 4*y+1), cct_1.getpixel((1, 1)))
        
        share_1.putpixel((4*x+2, 4*y), sct_1.getpixel((0, 0)))
        share_1.putpixel((4*x+2, 4*y+1), sct_1.getpixel((0, 1)))
        share_1.putpixel((4*x+3, 4*y), sct_1.getpixel((1, 0)))
        share_1.putpixel((4*x+3, 4*y+1), sct_1.getpixel((1, 1)))
        
        share_1.putpixel((4*x, 4*y+2), cct_1.getpixel((0, 0)))
        share_1.putpixel((4*x, 4*y+3), cct_1.getpixel((0, 1)))
        share_1.putpixel((4*x+1, 4*y+2), cct_1.getpixel((1, 0)))
        share_1.putpixel((4*x+1, 4*y+3), cct_1.getpixel((1, 1)))

        share_1.putpixel((4*x+2, 4*y+2), sct_1.getpixel((0, 0)))
        share_1.putpixel((4*x+2, 4*y+3), sct_1.getpixel((0, 1)))
        share_1.putpixel((4*x+3, 4*y+2), sct_1.getpixel((1, 0)))
        share_1.putpixel((4*x+3, 4*y+3), sct_1.getpixel((1, 1)))
        
        
        share_2.putpixel((4*x, 4*y), cct_2.getpixel((0, 0)))
        share_2.putpixel((4*x, 4*y+1), cct_2.getpixel((0, 1)))
        share_2.putpixel((4*x+1, 4*y), cct_2.getpixel((1, 0)))
        share_2.putpixel((4*x+1, 4*y+1), cct_2.getpixel((1, 1)))
        
        share_2.putpixel((4*x+2, 4*y), sct_2.getpixel((0, 0)))
        share_2.putpixel((4*x+2, 4*y+1), sct_2.getpixel((0, 1)))
        share_2.putpixel((4*x+3, 4*y), sct_2.getpixel((1, 0)))
        share_2.putpixel((4*x+3, 4*y+1), sct_2.getpixel((1, 1)))
     
        share_2.putpixel((4*x, 4*y+2), cct_2.getpixel((0, 0)))
        share_2.putpixel((4*x, 4*y+3), cct_2.getpixel((0, 1)))
        share_2.putpixel((4*x+1, 4*y+2), cct_2.getpixel((1, 0)))
        share_2.putpixel((4*x+1, 4*y+3), cct_2.getpixel((1, 1)))
        
        share_2.putpixel((4*x+2, 4*y+2), sct_2.getpixel((0, 0)))
        share_2.putpixel((4*x+2, 4*y+3), sct_2.getpixel((0, 1)))
        share_2.putpixel((4*x+3, 4*y+2), sct_2.getpixel((1, 0)))
        share_2.putpixel((4*x+3, 4*y+3), sct_2.getpixel((1, 1)))
      
      # even row
      else:
        share_1.putpixel((4*x, 4*y), sct_1.getpixel((0, 0)))
        share_1.putpixel((4*x, 4*y+1), sct_1.getpixel((0, 1)))
        share_1.putpixel((4*x+1, 4*y), sct_1.getpixel((1, 0)))
        share_1.putpixel((4*x+1, 4*y+1), sct_1.getpixel((1, 1)))
        
        share_1.putpixel((4*x+2, 4*y), cct_1.getpixel((0, 0)))
        share_1.putpixel((4*x+2, 4*y+1), cct_1.getpixel((0, 1)))
        share_1.putpixel((4*x+3, 4*y), cct_1.getpixel((1, 0)))
        share_1.putpixel((4*x+3, 4*y+1), cct_1.getpixel((1, 1)))

        share_1.putpixel((4*x, 4*y+2), sct_1.getpixel((0, 0)))
        share_1.putpixel((4*x, 4*y+3), sct_1.getpixel((0, 1)))
        share_1.putpixel((4*x+1, 4*y+2), sct_1.getpixel((1, 0)))
        share_1.putpixel((4*x+1, 4*y+3), sct_1.getpixel((1, 1)))
        
        share_1.putpixel((4*x+2, 4*y+2), cct_1.getpixel((0, 0)))
        share_1.putpixel((4*x+2, 4*y+3), cct_1.getpixel((0, 1)))
        share_1.putpixel((4*x+3, 4*y+2), cct_1.getpixel((1, 0)))
        share_1.putpixel((4*x+3, 4*y+3), cct_1.getpixel((1, 1)))
        
        share_2.putpixel((4*x, 4*y), sct_2.getpixel((0, 0)))
        share_2.putpixel((4*x, 4*y+1), sct_2.getpixel((0, 1)))
        share_2.putpixel((4*x+1, 4*y), sct_2.getpixel((1, 0)))
        share_2.putpixel((4*x+1, 4*y+1), sct_2.getpixel((1, 1)))
        
        share_2.putpixel((4*x+2, 4*y), cct_2.getpixel((0, 0)))
        share_2.putpixel((4*x+2, 4*y+1), cct_2.getpixel((0, 1)))
        share_2.putpixel((4*x+3, 4*y), cct_2.getpixel((1, 0)))
        share_2.putpixel((4*x+3, 4*y+1), cct_2.getpixel((1, 1)))
        
        share_2.putpixel((4*x, 4*y+2), sct_2.getpixel((0, 0)))
        share_2.putpixel((4*x, 4*y+3), sct_2.getpixel((0, 1)))
        share_2.putpixel((4*x+1, 4*y+2), sct_2.getpixel((1, 0)))
        share_2.putpixel((4*x+1, 4*y+3), sct_2.getpixel((1, 1)))
        
        share_2.putpixel((4*x+2, 4*y+2), cct_2.getpixel((0, 0)))
        share_2.putpixel((4*x+2, 4*y+3), cct_2.getpixel((0, 1)))
        share_2.putpixel((4*x+3, 4*y+2), cct_2.getpixel((1, 0)))
        share_2.putpixel((4*x+3, 4*y+3), cct_2.getpixel((1, 1)))

  share_1.save("outputs/our_Share_1.jpg")
  share_2.save("outputs/our_Share_2.jpg")


def emulateSuperposition(mode="paper"):

  share_1 = Image.open("outputs/Share_1.jpg").convert("CMYK")
  share_2 = Image.open("outputs/Share_2.jpg").convert("CMYK")
  
  if mode == "our":
    share_1 = Image.open("outputs/our_Share_1.jpg").convert("CMYK")
    share_2 = Image.open("outputs/our_Share_2.jpg").convert("CMYK")

  superposition = Image.new("CMYK", [share_1.size[0], share_1.size[1]])

  for i in range(0, share_1.size[0], 1):
    for j in range(0, share_1.size[1], 1):
      #print("share_1[" + str(i) + ", " + str(j) + "] = ")
      #print(share_1.getpixel((i, j)))
      #print("share_2[" + str(i) + ", " + str(j) + "] = ")
      #print(share_2.getpixel((i, j)))

      if share_1.getpixel((i, j))[0] > 200:
        c1 = 255
      else:
        c1 = 0
      
      if share_1.getpixel((i, j))[1] > 200:
        m1 = 255
      else:
        m1 = 0

      if share_1.getpixel((i, j))[2] > 200:
        y1 = 255
      else:
        y1 = 0

      if share_2.getpixel((i, j))[0] > 200:
        c2 = 255
      else:
        c2 = 0
      
      if share_2.getpixel((i, j))[1] > 200:
        m2 = 255
      else:
        m2 = 0

      if share_2.getpixel((i, j))[2] > 200:
        y2 = 255
      else:
        y2 = 0

      c = c1 or c2
      m = m1 or m2
      y = y1 or y2
      
      superposition.putpixel((i, j),(c, m, y, 0) );

  superposition.save("outputs/Superposition.jpg")
  
  if mode == "our":
    superposition.save("outputs/our_Superposition.jpg")



def parse(argv):
  image1 = argv[0]
  image2 = argv[1]
  secret = argv[2]
  
  return (image1, image2, secret)


if __name__ == "__main__":
  image1, image2, secret = parse(sys.argv[1:])       
 
  CHECK_FOLDER = os.path.isdir("outputs")
  if not os.path.isdir("outputs"):
    os.makedirs("outputs")
  
  generateCMYK(image1, "1") 
  generateCMYK(image2, "2") 
  generateCMYK(secret, "s") 
  generateHalftone("1")
  generateHalftone("2")
  generateHalftone("s")

  # the method proposed in the paper 
  generateExtraction("1")
  generateExtraction("2")
  generateExtraction("s")

  generateShares()
  emulateSuperposition()

  # our method
  generateOurShares()
  emulateSuperposition("our") 
