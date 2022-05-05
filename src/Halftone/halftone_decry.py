import numpy as np
from PIL import Image
import sys
import os

sys.path.insert(0, "../../utility")
import performance

#combine four shares to get the decrypted image.
def combineShares(inputFile1,inputFile2,inputFile3,inputFile4):
  outfile = Image.new('CMYK', inputFile1.size)
  for x in range(0,inputFile1.size[0],2):
    for y in range(0,inputFile1.size[1],2):

      C = inputFile1.getpixel((x+1, y))[0]
      M = inputFile2.getpixel((x+1, y))[1]
      Y = inputFile3.getpixel((x+1, y))[2]
      K = inputFile4.getpixel((x+1, y))[3]

      outfile.putpixel((x, y), (C,M,Y,K))
      outfile.putpixel((x+1, y), (C,M,Y,K))
      outfile.putpixel((x, y+1), (C,M,Y,K))
      outfile.putpixel((x+1, y+1), (C,M,Y,K))

  print("Combined Shares!")
  return outfile


if __name__ == "__main__":
    
  n = len(sys.argv)
  
  if(n <= 4):
    sys.exit("Please select four shares")
  
  try: 
    inputFile1 = Image.open(sys.argv[1])
    inputFile2 = Image.open(sys.argv[2])
    inputFile3 = Image.open(sys.argv[3])
    inputFile4 = Image.open(sys.argv[4])

  except FileNotFoundError:
    sys.exit("Input file not found!")

  #create a folder to put outfiles
  output_image = combineShares(inputFile1,inputFile2,inputFile3,inputFile4)
  output_image = output_image.resize((int(inputFile1.size[0]/2),int(inputFile1.size[1]/2)))
  output_image.save('./outputs/decrypted.jpg', mode = "CMYK")
  print("\nImage is saved to './outputs/decrypted.jpg'...")
  
  # performance evaluation
  print("Evaluation metrics : ")
  MSE = performance.MSE(sys.argv[5], "./outputs/decrypted.jpg")
  print("MSE = " + str(MSE))
  PSNR = performance.PSNR(sys.argv[5], "./outputs/decrypted.jpg")
  print("PSNR = " + str(PSNR))


  output_image = Image.open('./outputs/decrypted.jpg')
  if output_image.mode == 'CMYK':
    output_image = output_image.convert('RGB')
  output_matrix = np.asarray(output_image)
