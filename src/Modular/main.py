import numpy as np
from PIL import Image
import sys, getopt

sys.path.insert(0, "../../utility")
import performance

import os,errno
import glob


def encrypt(input_image, share_size):
  image = np.asarray(input_image)
  (row, column, depth) = image.shape
  size =(row, column, depth, share_size)
  shares = np.random.randint(0, 256, size)
  shares[:,:,:,-1] = image.copy()
  for i in range(share_size-1):
    shares[:,:,:,-1] = (shares[:,:,:,-1] + shares[:,:,:,i])%256

  return shares


def decrypt(shares):
  (row, column, depth, share_size) = shares.shape
  shares_image = shares.copy()
  for i in range(share_size-1):
    shares_image[:,:,:,-1] = (shares_image[:,:,:,-1] - shares_image[:,:,:,i] + 256)%256

  final_output = shares_image[:,:,:,share_size-1]
  output_image = Image.fromarray(final_output.astype(np.uint8))
  return output_image

    
if __name__ == "__main__":

  share_size = int(sys.argv[1])
  try:
    if share_size < 2 or share_size > 8:
      print("Share size must be between 2 and 8")
      raise ValueError
  except ValueError:
    print("Input is not a valid integer!")
    exit(0)

  # create a folder to store output images
  if not os.path.isdir("outputs"):
    os.makedirs("outputs")

  # remove existing files in the outputs folder
  else:
    files = glob.glob("./outputs/*.jpg")
    for f in files:
      os.remove(f)

  try:
    inputfile = sys.argv[2]
    input_image = Image.open(inputfile)
  except FileNotFoundError:
    print("Input file not found!")
    exit(0)

  print("Number of shares image = ", share_size)

  shares = encrypt(input_image, share_size)

  for idx in range(share_size):
    image = Image.fromarray(shares[:,:,:,idx].astype(np.uint8))
    name = "./outputs/Modular_Share_" + str(idx+1) + ".jpg"
    image.save(name)

  output_image = decrypt(shares)

  output_image.save("./outputs/Output_Modular.jpg")
  print("Image is saved './outputs/Output_Modular.jpg' ...")
  
  print("Evaluation metrics : ")
  MSE = performance.MSE(inputfile, "./outputs/Output_Modular.jpg")
  print("MSE = " + str(MSE))
  PSNR = performance.PSNR(inputfile, "./outputs/Output_Modular.jpg")
  print("PSNR = " + str(PSNR))
  
