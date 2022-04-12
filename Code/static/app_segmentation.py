import tensorflow as tf
from flask import *
from getmodel import *
import tifffile as tiff
import numpy as np  
import os
import cv2
from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.pyplot as plt
from PIL import Image

app = Flask(__name__) 



def M(image_path):
    img = tiff.imread(image_path)  
#     img = np.rollaxis(img, 0, 3)
    return img

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

def convert_into_rgb(tiff_file_path,save_name):
    print('Given path:'  + tiff_file_path)
    m = M(tiff_file_path)
    img = np.zeros_like(m)
    img[:,:,0] = m[:,:,0] #red
    img[:,:,1] = m[:,:,1] #green
    img[:,:,2] = m[:,:,2] #blue
    image_rgb = stretch_8bit(img)[:,:,:3]
#     plt.imshow(image_rgb)
    plt.imsave(arr= image_rgb, cmap='gray', fname= save_name)
    return image_rgb


# @app.route('/segmentation', methods = ['POST']) 
# def success():  
#     if request.method == 'POST':
#         print(tf.__version__)
#         way = request.form.get('type')     #road or building
#         place=request.form.get('city')    #paris or khartoum or vegas 
#         files = request.files["data"]  
#         IMAGE_UPLOADS = 'static/segmentation_upload/'
#         app.config['IMAGE_UPLOADS'] = IMAGE_UPLOADS
#         files.save(os.path.join(app.config["IMAGE_UPLOADS"], files.filename))
#         if way=='road':
#             if place=='paris' :
#                 #my_model = tf.keras.models.load_model('./model/test_paris.h5')
#                 mrv = getmymodelvegas()
#                 mrv.load_weights('./model/paris_road2.h5')
#                 my_model = mrv
               
#             elif place=='khartoum':
#                 mrv = getmymodelvegas()
#                 mrv.load_weights('./model/khartoum_road2.h5')
#                 my_model = mrv
#             elif place == 'vegas':
#                 # my_model = tf.keras.models.load_model('C:/Users/SilverWrath/Documents/FLASK_DL/test/model/vegas_road2.h5')
#                 mrv = getmymodelvegas()
#                 mrv.load_weights('./model/vegas_road2.h5')
#                 my_model = mrv
              

#         elif way=='building':
#             if place=='paris' :
#                 mrv = getmymodelvegas()
#                 mrv.load_weights('./model/paris_building.h5')
#                 my_model = mrv
#             elif place=='khartoum':
#                 mrv = getmymodelvegas()
#                 mrv.load_weights('./model/khartoum_building.h5')
#                 my_model = mrv
#             elif place == 'vegas':
#                 mrv = getmymodelvegas()
#                 mrv.load_weights('./model/vegas_building.h5')
#                 my_model = mrv

         
#         shape_to_resize = (640, 640)

#         filepath = os.path.join(app.config["IMAGE_UPLOADS"], files.filename)

#         tarr = cv2.resize(convert_into_rgb(filepath,'static/segmentation_upload/myImage.jpg'), shape_to_resize)

#         totest = np.expand_dims(tarr, 0)

#         # tpred - stores output of model.

#         # Here, my_model = model_road_paris
#         tpred = my_model.predict(totest)

#         myoutput = (tpred > 0.05).astype(np.uint8)
#         print("\nmyoutput shape:", myoutput.shape)
#         print("\nmyoutput shape:", np.squeeze(myoutput).shape)
#         plt.imsave('static/segmentation_upload/outputimage.png',np.squeeze(myoutput))
#         print("\nSAVED SUCCESFULLY!!\n")
#         response =  { 'Status' : 'Success', 'input': 'static/segmentation_upload/myImage.jpg', 'output':'static/segmentation_upload/outputimage.png'}
#         print(response)

#         return jsonify(response) 
        


if __name__ == '__main__':  
    app.run(debug = True)