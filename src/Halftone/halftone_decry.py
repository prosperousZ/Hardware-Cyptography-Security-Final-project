import numpy as np
from PIL import Image
import sys
import os

import performance

#combine four shares to get the decrypted image.
def combineShares(outputDireName,inputFile1,inputFile2,inputFile3,inputFile4):
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
    
    #print("Save input image as 'Input.png' in the same folder as this file\n")
    n = len(sys.argv)
    current_directory = os.getcwd()
    if(n <= 4):
         sys.exit("Please select four shares")
    try:
     
        inputFile1 = Image.open(current_directory + '/' + sys.argv[1])
        inputFile2 = Image.open(current_directory+ '/' + sys.argv[2])
        inputFile3 = Image.open(current_directory+'/' + sys.argv[3])
        inputFile4 = Image.open(current_directory+'/' + sys.argv[4])

    except FileNotFoundError:
    	sys.exit("Input file not found!")

    print("Image uploaded successfully!")
    #create a folder to put outfiles
    output_image = combineShares(current_directory,inputFile1,inputFile2,inputFile3,inputFile4)
    print("size: ",inputFile1.size)
    output_image = output_image.resize((int(inputFile1.size[0]/2),int(inputFile1.size[1]/2)))
    output_image.save(current_directory + '/outputs/decrypted.jpg', mode = "CMYK")
    print("\nImage is saved 'decrypted.jpg' in outputs directory...")
    
      # performance evaluation
    print("Evaluation metrics : ")
    MSE = performance.MSE(sys.argv[5], "./decrypted.jpg")
    print("MSE = " + str(MSE))
    PSNR = performance.PSNR(sys.argv[5], "./decrypted.jpg")
    print("PSNR = " + str(PSNR))
  

    output_image = Image.open('./decrypted.jpg')
    if output_image.mode == 'CMYK':
        output_image = output_image.convert('RGB')
    output_matrix = np.asarray(output_image)
