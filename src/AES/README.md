# Visual Cryptography with AES Implementation


## What is this implementation about?
The purpose of this implementation is to encrypt and decrypt an image 
using visual cryptography and generate a ciphertext using AES and measure the performance.

The source code will take in an input image and a key string and follow the algorithm introduced in
the paper. There are four generated files:
- cipher.txt
- R.png
- P.png
- decryptedImage.jpg

## Files
- main.py : the implementation 

## Run
```
python3 main.py -i image
```
For example,
```
python3 main.py -i ../../images/photo.jpg
```


## Reference
- Venkata Krishna Pavan Kalubandi, Hemanth Vaddi, Vishnu Ramineni, and Agilandeeswari Loganathan, "A Novel Image Encryption Algorithm using AES and Visual Cryptography," in *International Conference on Next Generation Computing Technologies*, 2016.
