import numpy as np
from PIL import Image
from ColourMetrics import psnr, normxcorr2D
import cv2
import sys
import os

def combineShares(outputDireName,infile1,infile2,infile3,infile4):
    #infile1 = Image.open(outputDireName+'/CMYK_Share3_1.jpg')
    #infile2 = Image.open(outputDireName+'/CMYK_Share3_2.jpg')
    #infile3 = Image.open(outputDireName+'/CMYK_Share3_3.jpg')
    #infile4 = Image.open(outputDireName+'/CMYK_Share3_shareMask.jpg')

    outfile = Image.new('CMYK', infile1.size)

    for x in range(0,infile1.size[0],2):
        for y in range(0,infile1.size[1],2):

            C = infile1.getpixel((x+1, y))[0]
            M = infile2.getpixel((x+1, y))[1]
            Y = infile3.getpixel((x+1, y))[2]
            K = infile4.getpixel((x+1, y))[3]

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
     
        infile1 = Image.open(current_directory + '/' + sys.argv[1])
        infile2 = Image.open(current_directory+ '/' + sys.argv[2])
        infile3 = Image.open(current_directory+'/' + sys.argv[3])
        infile4 = Image.open(current_directory+'/' + sys.argv[4])

    except FileNotFoundError:
    	sys.exit("Input file not found!")

    print("Image uploaded successfully!")
    #create a folder to put outfiles
    output_image = combineShares(current_directory,infile1,infile2,infile3,infile4)
    print("size: ",infile1.size)
    output_image = output_image.resize((int(infile1.size[0]/2),int(infile1.size[1]/2)))
    output_image.save(current_directory + '/decrypted.jpg', mode = "CMYK")
    print("\nImage is saved 'decrypted.jpg' ...")
    
    output_image = Image.open(current_directory+'/decrypted.jpg')
    if output_image.mode == 'CMYK':
        output_image = output_image.convert('RGB')
    output_matrix = np.asarray(output_image)
