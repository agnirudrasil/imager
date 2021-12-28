import cv2 as cv
import numpy as np
import imutils
from urllib.request import urlopen
import os

def GnP(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv.imdecode(image, -1)
    #resize the image to with of 500
    image = imutils.resize(image, width=500)
    # return the image
    image = cv.cvtColor(image, cv.COLOR_RGBA2RGB)
    return image



def canny_img(img):
    """
    Canny edge detection
    """
    img = cv.Canny(img, 75, 120)
    img = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
    return img

def cartoonify(frame):

    gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
    gray = cv.medianBlur(gray, 3)
    edges = cv.adaptiveThreshold(
        gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 9, 10)
  # Making a Cartoon of the image
    color = cv.bilateralFilter(frame, 12, 250, 250)
    cartoon = cv.bitwise_and(color, color, mask=edges)
    cartoon_image = cv.stylization(cartoon, sigma_s=150, sigma_r=0.25)
    frame = cartoon_image
    #frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    
    return frame


def watercolor(frame):
    frame = cv.stylization(frame, sigma_s=60, sigma_r=0.6)
    #frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    return frame


def pencil(frame):
    pencil, color = cv.pencilSketch(frame, sigma_s=60, sigma_r=0.5, shade_factor=0.010)
    #frame = cv.cvtColor(pencil, cv.COLOR_BGR2RGB)
     
    return color

def pen(frame):
    gray_image=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    inverted=255-gray_image
    blurred=cv.GaussianBlur(inverted,(21,21),0)
    invertedblur=255-blurred
    pencilsketch=cv.divide(gray_image,invertedblur,scale=256.0)
    return pencilsketch

def econify(frame):
    canny = canny_img(frame)

    blue, g, r = cv.split(canny) 
    blank = np.zeros(canny.shape[:2], dtype='uint8')

    green = cv.merge([blank,g,blank])
        
    frame = green
    #frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    
    return frame

def negative(frame):
    frame = cv.bitwise_not(frame)
    #frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    
    return frame


def getmodel(model_name):

    style_models_file = ['candy.t7', 'composition_vii.t7', 'feathers.t7', 'la_muse.t7', 'mosaic.t7', 'starry_night.t7', 'the_scream.t7', 'the_wave.t7', 'udnie.t7']
    style_models_name = ['candy', 'composition', 'feathers', 'muse', 'mosaic', 'night', 'scream', 'wave', 'udnie']
    model_path = 'models'
    style_models_dict = {name: os.path.join(model_path, filee) for name, filee in zip(style_models_name, style_models_file)}
    if model_name not in style_models_name:
        return None

    model = cv.dnn.readNetFromTorch(style_models_dict[model_name])
    return model

def style_transfer(image, model):

    
    (h, w) = image.shape[:2]
    

    blob = cv.dnn.blobFromImage(image, 1.0, (w, h), (103.939, 116.779, 123.680), swapRB=False, crop=False)
    model.setInput(blob)
    output = model.forward()

    output = output.reshape((3, output.shape[2], output.shape[3]))
    output[0] += 103.939
    output[1] += 116.779
    output[2] += 123.680
    output /= 255.0
    output = output.transpose(1, 2, 0)
    output = np.clip(output, 0.0, 1.0)
    output = imutils.resize(output, width=500)
    output = output*255
    return output
