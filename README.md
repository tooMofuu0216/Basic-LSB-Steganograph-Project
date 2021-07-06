# Basic-LSB-Steganograph-Project

I **DO NOT** claim any of the idea comes entirely from me\
Trying to implement Basic Steganograph for **image** and **sound** file (wav only) using LSB algorithm with other's idea

## Image Steganograph (class SteganoImg)

```python
i_stegano = SteganoImg()
# hide data
# para1: path, para2: msg
i_stegano.hide('resource/input.JPG', 'heLLo World!')
# reveal data
# para1: path
i_stegano.extract('resource/input'+'_out.PNG')
```

## Audio Steganograph (class SteganoSound)

```python
s_stegano = SteganoSound()
# hide data
# para1: path, para2: msg
s_stegano.hide('resource/Pack#2_Kit 1_Groove 1_180BPM.wav', 'heLLo World!')
# reveal data
# para1: path
s_stegano.extract('resource/Pack#2_Kit 1_Groove 1_180BPM'+'_out.wav')
```

Reference Link:\
(Audio):\
https://sumit-arora.medium.com/audio-steganography-the-art-of-hiding-secrets-within-earshot-part-2-of-2-c76b1be719b3
(Image):\
https://github.com/rroy1212/Image_Steganography/blob/master/ImageSteganography.ipynb


