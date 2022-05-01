import numpy as np
from PIL import Image
import sys, getopt
sys.path.insert(0, "../../utility")
import performance
import os,errno


def encrypt(input_image, share_size):
    image = np.asarray(input_image)
    (row, column, depth) = image.shape
    size =(row, column, depth, share_size)
    shares = np.random.randint(0, 256, size)
    shares[:,:,:,-1] = image.copy()
    for i in range(share_size-1):
        shares[:,:,:,-1] = shares[:,:,:,-1] ^ shares[:,:,:,i]

    return shares, image

def decrypt(shares):
    (row, column, depth, share_size) = shares.shape
    shares_image = shares.copy()
    for i in range(share_size-1):
    	shares_image[:,:,:,-1] = shares_image[:,:,:,-1] ^ shares_image[:,:,:,i]

    final_output = shares_image[:,:,:,share_size-1]
    output_image = Image.fromarray(final_output.astype(np.uint8))
    return output_image, final_output

    
if __name__ == "__main__":

    try:
       os.remove("./Output_XOR.jpg")
       #print("% s removed successfully")
    except OSError as error:
       print(error)
       #print("File path can not be removed")

    try:
       os.remove("./XOR_Share_1.jpg")
       #print("% s removed successfully")
    except OSError as error:
       print(error)
       #print("File path can not be removed")

    try:
       os.remove("./XOR_Share_2.jpg")
       #print("% s removed successfully")
    except OSError as error:
       print(error)
       #print("File path can not be removed")
          
    try:
       os.remove("./XOR_Share_3.jpg")
       #print("% s removed successfully")
    except OSError as error:
       print(error)
       #print("File path can not be removed")
          
    try:
       os.remove("./XOR_Share_4.jpg")
       #print("% s removed successfully")
    except OSError as error:
       print(error)
       #print("File path can not be removed")
          
    try:
       os.remove("./XOR_Share_5.jpg")
       #print("% s removed successfully")
    except OSError as error:
       print(error)
       #print("File path can not be removed")
          
    try:
       os.remove("./XOR_Share_6.jpg")
       #print("% s removed successfully")
    except OSError as error:
       print(error)
       #print("File path can not be removed")
          
    try:
       os.remove("./XOR_Share_7.jpg")
       #print("% s removed successfully")
    except OSError as error:
       print(error)
       #print("File path can not be removed")
       
    try:
       os.remove("./XOR_Share_8.jpg")
       #print("% s removed successfully")
    except OSError as error:
       print(error)
       #print("File path can not be removed")

    print("The error is just showing that previous Encrypted share were deleted\n")

    print("Save input image as 'image1.jpg' in the same folder as this file\n")

    try:
        share_size = int(input("Input the number of shares images you want to create for encrypting (min is 2, max is 8) : "))
        if share_size < 2 or share_size > 8:
            raise ValueError
    except ValueError:
    	print("Input is not a valid integer!")
    	exit(0)

  
    try:
        input_image = Image.open('image1.jpg')

    except FileNotFoundError:
    	print("Input file not found!")
    	exit(0)

    print("Image uploaded successfully!")
    print("Input image size (in pixels) : ", input_image.size)   
    print("Number of shares image = ", share_size)

    shares, input_matrix = encrypt(input_image, share_size)

    for ind in range(share_size):
        image = Image.fromarray(shares[:,:,:,ind].astype(np.uint8))
        name = "XOR_Share_" + str(ind+1) + ".jpg"
        image.save(name)

    output_image, output_matrix = decrypt(shares)

    output_image.save('Output_XOR.jpg')
    print("Image is saved 'Output_XOR.jpg' ...")
    
    print("Evaluation metrics : ")
    MSE = performance.MSE("./image1.jpg", "./Output_XOR.jpg")
    print("MSE = " + str(MSE))
    PSNR = performance.PSNR("./image1.jpg", "./Output_XOR.jpg")
    print("PSNR = " + str(PSNR))
  
