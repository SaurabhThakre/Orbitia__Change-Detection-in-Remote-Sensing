import tifffile as tiff
import numpy as np
import cv2 as cv
import os
from flask import *
from base64 import encodebytes
import zipfile
import uuid
from PIL import Image
app = Flask(__name__)  
 
@app.route('/')  
def upload():  
    return render_template("upload.html")  

img_map = {
    1 : 'natural_color',   # Shows natural RGB color
    2 : 'geology',         # Shows geological formations, lithology features, and faults
    3 : 'ndvi',            # Vegetation
    4 : 'bathymetric',     # Water bodies, suspended sediments in water
    5 : 'color_infrared',  #     
    6 : 'moisture_index',  # Estimates the amount of moisture content
    7 : 'ndwi'             # Water stress
}

satellites = {"landsat","sentinel","worldview"}

def stretch_8bit(bands, lower_percent=2, higher_percent=98):
    out = np.zeros_like(bands)
    for i in range(3):
        a = 0 
        b = 255 
        c = np.percentile(bands[:,:,i], lower_percent)
        d = np.percentile(bands[:,:,i], higher_percent)        
        t = a + (bands[:,:,i] - c) * (b - a) / (d - c)    
        t[t<a] = a
        t[t>b] = b
        out[:,:,i] =t
    return out.astype(np.uint8) 

def M(image_path):
    img = tiff.imread(image_path)  
#     img = np.rollaxis(img, 0, 3)
    return img

def convert_into_rgb(tiff_file_path, save_path, b1, b2, b3):
    print('Given path:'  + tiff_file_path)
    m = M(tiff_file_path)
    img = np.zeros_like(m)
    img[:,:,0] = m[:,:,b1-1] #red
    img[:,:,1] = m[:,:,b2-1] #green
    img[:,:,2] = m[:,:,b3-1] #blue
    image_rgb = stretch_8bit(img)[:,:,:3]
#     plt.imshow(image_rgb)
#     plt.imsave(arr= image_rgb, cmap='gray', fname= save_path)
    return image_rgb

def calculate_ndvi(tiff_file_path, nir, red):
    img = tiff.imread(tiff_file_path)
    
    band_nir = img[:,:,nir-1]
    band_red  = img[:,:,red-1]
    
    ndvi = np.zeros((img.shape[0] ,img.shape[1], 1))
    
    ndvi = (band_nir - band_red)/(band_nir + band_red)
    
    bands = np.expand_dims(ndvi, -1)
    out = np.zeros_like(bands)
    
    lower_percent=2
    higher_percent=98
    
    for i in range(1):
        a = 0 
        b = 255 
        c = np.percentile(bands[:,:,i], lower_percent)
        d = np.percentile(bands[:,:,i], higher_percent)        
        t = a + (bands[:,:,i] - c) * (b - a) / (d - c)    
        t[t<a] = a
        t[t>b] = b
        out[:,:,i] =t
        
    return out.astype(np.uint8)  

def calculate_ndwi(tiff_file_path, green, nir):
    img = tiff.imread(tiff_file_path)
    
    band_green = img[:,:,green-1]
    band_nir  = img[:,:,nir-1]
    
    moisture = np.zeros((img.shape[0] ,img.shape[1], 1))
    
    moisture = (band_green - band_nir)/(band_green + band_nir)
    
    bands = np.expand_dims(moisture, -1)
    out = np.zeros_like(bands)
    
    lower_percent=2
    higher_percent=98
    
    for i in range(1):
        a = 0 
        b = 255 
        c = np.percentile(bands[:,:,i], lower_percent)
        d = np.percentile(bands[:,:,i], higher_percent)        
        t = a + (bands[:,:,i] - c) * (b - a) / (d - c)    
        t[t<a] = a
        t[t>b] = b
        out[:,:,i] =t
        
    return out.astype(np.uint8)


def calculate_moisture(tiff_file_path, vnir, swir):
    img = tiff.imread(tiff_file_path)
    
    band_vnir = img[:,:,vnir-1]
    band_swir  = img[:,:,swir-1]
    
    moisture = np.zeros((img.shape[0] ,img.shape[1], 1))
    
    moisture = (band_vnir - band_swir)/(band_vnir + band_swir)
    
    bands = np.expand_dims(moisture, -1)
    out = np.zeros_like(bands)
    
    lower_percent=2
    higher_percent=98
    
    for i in range(1):
        a = 0 
        b = 255 
        c = np.percentile(bands[:,:,i], lower_percent)
        d = np.percentile(bands[:,:,i], higher_percent)        
        t = a + (bands[:,:,i] - c) * (b - a) / (d - c)    
        t[t<a] = a
        t[t>b] = b
        out[:,:,i] =t
        
    return out.astype(np.uint8)

def getImage(satellite, map_index, tiff_file):
    print(satellite)
    print( map_index)
    bands = tiff.imread(tiff_file).shape[2]
    
    # NATURAL COLOR
    if map_index == 1:
        if satellite == 'sentinel' and bands >= 4 :
            image = convert_into_rgb(tiff_file, '', 4, 3, 2)
            return image

        elif satellite == 'landsat' and bands >= 4:
            image = convert_into_rgb(tiff_file, '', 4, 3, 2)
            return image

        elif satellite == 'worldview' and bands >= 5:
            image = convert_into_rgb(tiff_file, '', 5, 3, 2)
            return image
        
        else:
            return None
    
    # GEOLOGY
    elif map_index == 2 :
        if satellite == 'sentinel' and bands >= 12:
            image = convert_into_rgb(tiff_file, '', 12, 11, 2)
            return image
        
        elif satellite == 'landsat' and bands >= 7:
            image = convert_into_rgb(tiff_file, '', 7, 6, 2)
            return image
        
        elif satellite == 'worldview' and bands >= 15:
            image = convert_into_rgb(tiff_file, '', 15, 11, 2) #try 15,10,2 also
            return image
        
        else:
            return None
        
    # NDVI INDEX
    elif map_index == 3:
        if satellite == 'sentinel' and bands >= 8:
            image = calculate_ndvi(tiff_file, 8, 4)
            return image
        
        elif satellite == 'landsat' and bands >= 5:
            image = calculate_ndvi(tiff_file, 5, 4)
            return image
        
        elif satellite == 'worldview' and bands >= 8:
            image = calculate_ndvi(tiff_file, 8, 5)
            return image
        
        else:
            return None
        
    # BATHYMETRIC
    elif map_index == 4:
        if satellite == 'sentinel' and bands >= 4:
            image = convert_into_rgb(tiff_file, '', 4, 3, 1)
            return image
        
        elif satellite == 'landsat' and bands >= 4:
            image = convert_into_rgb(tiff_file, '', 4, 3, 1)
            return image
        
        elif satellite == 'worldview' and bands >= 5:
            image = convert_into_rgb(tiff_file, '', 5, 3, 1)
            return image
        
        else:
            return None
        
    # COLOR INFRARED
    elif map_index == 5:
        if satellite == 'sentinel' and bands >= 8:
            image = convert_into_rgb(tiff_file, '', 8, 4, 3)
            return image
        
        elif satellite == 'landsat' and bands >= 5:
            image = convert_into_rgb(tiff_file, '', 5, 4, 3)
            return image
        
        elif satellite == 'worldview' and bands >= 8:
            image = convert_into_rgb(tiff_file, '', 8, 5, 3)
            return image
        
        else:
            return None
        
    # MOISTURE INDEX
    elif map_index == 6:
        if satellite == 'sentinel' and bands >= 12:
            image = calculate_moisture(tiff_file, 9, 12)
            return image
        
        elif satellite == 'landsat' and bands >= 6:
            image = calculate_moisture(tiff_file, 5, 6)
            return image
        
        elif satellite == 'worldview' and bands >= 11:
            image = calculate_moisture(tiff_file, 8, 11)
            return image
        
        else:
            return None
        
    # NDWI INDEX
    elif map_index == 7:
        if satellite == 'sentinel' and bands >= 8:
            image = calculate_ndwi(tiff_file, 3, 8)
            return image
        
        elif satellite == 'landsat' and bands >= 5:
            image = calculate_ndwi(tiff_file, 3, 5)
            return image
        
        elif satellite == 'worldview' and bands >= 8:
            image = calculate_ndwi(tiff_file, 3, 8)
            return image
        
        else:
            return None
    
     