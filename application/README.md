# Visual Cryptography with Meaning Shares 


## What is this implementation about?
The purpose of this implementation is to encrypt a secret image using two cover images.
Overlaying the two generated shares could decrypt and get the secret image back.

## Files
- main.py : the implementation
- image1.jpg : the first image for generating the first meaning share
- image2.jpg : the second image for generating the second  meaning share
- secret.jpg : the secret image to be encrypted
- outputs/ : folders to store the shares

## Run
```
python3 main.py ./image1.jpg ./image2.jpg ./secret.jpg
```

## Reference
- Hsien-Chu Wu, Hao-Cheng Wang, and Rui-Wen Yu, "Color Visual Cryptography Scheme Using Meaning Shares," International Conference on Intelligent Systems Design and Applications," 2008.
- Young-Chang Hou, "Visual cryptography for color images, "Pattern Recognition," 2003. 
