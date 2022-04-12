import cv2
import sklearn
import uuid
from sklearn.cluster import KMeans
from collections import Counter
from sklearn.decomposition import PCA
import skimage.morphology
import numpy as np
import time
import os

# file imports
from app_playground import *
from app_segmentation import *

from flask import *
from flask import render_template, url_for


app = Flask(__name__, template_folder='./templates', static_folder='./static')


@app.route("/")
def home():
    return render_template('index.html', title='index')


@app.route("/index.html")
def home1():
    return render_template('index.html', title='index')


@app.route("/pca-analysis.html")
def page1():
    return render_template('pca-analysis.html', title='page1')


@app.route('/pcaanalysis', methods=['POST', 'GET'])
def pcaanalysis():
    if request.method == 'POST':
        UPLOAD_PCA = './static/'
        app.config['UPLOAD_PCA'] = UPLOAD_PCA
        image1_path = request.files['file']
        image2_path = request.files['file1']
        image1_path.save(os.path.join(
            app.config["UPLOAD_PCA"], image1_path.filename))
        image2_path.save(os.path.join(
            app.config["UPLOAD_PCA"], image2_path.filename))
        response = find_PCAKmeans(os.path.join(app.config["UPLOAD_PCA"], image1_path.filename), os.path.join(
            app.config["UPLOAD_PCA"], image2_path.filename))
        print(response)
        response['img1'] = image1_path.filename
        response['img2'] = image2_path.filename
        print(response)
        return jsonify(response)

    else:
        return render_template('pca-analysis.html')


# pca final
def find_PCAKmeans(imagepath1, imagepath2):
    UPLOAD_PCA = './static/'
    app.config['UPLOAD_PCA'] = UPLOAD_PCA

    image1 = np.asarray(cv2.imread(imagepath1, 0))
    image2 = np.asarray(cv2.imread(imagepath2, 0))
    
    image1 = cv2.resize(image1, (256,256))
    image2 = cv2.resize(image2, (256,256))

    print("Image1 shape: ", image1.shape)
    print("Image2 shape: ", image2.shape)

    new_size = np.asarray(image1.shape) / 5
    new_size = new_size.astype(int) * 5

    print(new_size)

    image1 = cv2.resize(image1, (new_size[0], new_size[1])).astype(int)
    image2 = cv2.resize(image2, (new_size[0], new_size[1])).astype(int)

    diff_image = abs(image1 - image2)

    vector_set, mean_vec = find_vector_set(diff_image, new_size)
    pca = PCA()
    pca.fit(vector_set)
    EVS = pca.components_

    FVS = find_FVS(EVS, diff_image, mean_vec, new_size)
    components = 3
    least_index, change_map = clustering(FVS, components, new_size)

    change_map[change_map == least_index] = 255
    change_map[change_map != 255] = 0

    change_map = change_map.astype(np.uint8)
    kernel = np.asarray(((0, 0, 1, 0, 0),
                         (0, 1, 1, 1, 0),
                         (1, 1, 1, 1, 1),
                         (0, 1, 1, 1, 0),
                         (0, 0, 1, 0, 0)), dtype=np.uint8)

    cleanChangeMap = cv2.erode(change_map, kernel)
    print("-----------------------------DONE WITH CHANGE MAP---------------------------------------")

    unique_filename = str(uuid.uuid4().hex)
    cv2.imwrite(os.path.join(
        app.config["UPLOAD_PCA"], unique_filename+'.jpg'), cleanChangeMap)

    outputFile = unique_filename + ".jpg"
    response = {'status': 'Success', 'imagePath': outputFile}
    return response


def find_vector_set(diff_image, new_size):

    i = 0
    j = 0
    vector_set = np.zeros((int(new_size[0] * new_size[1] / 25), 25))
    while i < vector_set.shape[0]:
        while j < new_size[0]:
            k = 0
            while k < new_size[1]:
                block = diff_image[j:j+5, k:k+5]
                feature = block.ravel()
                vector_set[i, :] = feature
                k = k + 5
            j = j + 5
        i = i + 1

    mean_vec = np.mean(vector_set, axis=0)
    # Mean normalization
    vector_set = vector_set - mean_vec
    return vector_set, mean_vec


def find_FVS(EVS, diff_image, mean_vec, new):

    i = 2
    feature_vector_set = []

    while i < new[1] - 2:
        j = 2
        while j < new[0] - 2:
            block = diff_image[i-2:i+3, j-2:j+3]
            feature = block.flatten()
            feature_vector_set.append(feature)
            j = j+1
        i = i+1

    FVS = np.dot(feature_vector_set, EVS)
    FVS = FVS - mean_vec
    print("[INFO] Feature vector space size", FVS.shape)
    return FVS


def clustering(FVS, components, new):
    kmeans = KMeans(components, verbose=0)
    kmeans.fit(FVS)
    output = kmeans.predict(FVS)
    count = Counter(output)

    least_index = min(count, key=count.get)
    change_map = np.reshape(output, (new[0] - 4, new[1] - 4))
    return least_index, change_map


# -------------------------------------------------------------------------------------------
# playground

@app.route("/feature-extraction.html", methods=['GET'])
def page2():
    return render_template('feature-extraction.html')


@app.route('/featureExtraction', methods=['POST'])
def success():
    if request.method == 'POST':
        image_list = []
        UPLOAD_FOLDER = 'static/playground_output'

        PLAYGROUND_INPUT = 'static/playground_input/'
        app.config['PLAYGROUND_INPUT'] = PLAYGROUND_INPUT

        satellite = request.form.get('satellite')
        print(satellite)
        files = request.files["data"]
        print(files.filename)
        #  file_like_object = file.stream._file
        #  zipfile_ob = zipfile.ZipFile(file_like_object)
        #  file_names = zipfile_ob.namelist()
        #  # Filter names to only include the filetype that you want:
        #  file_names = [file_name for file_name in file_names if file_name.endswith(".tif")]
        #  files = [(zipfile_ob.open(name).read(),name) for name in file_names]

        print("-------------------dffdnbfdf===========================================")
        print(files)
        files.save(os.path.join(
            app.config["PLAYGROUND_INPUT"], files.filename))

        tp1 = getImage(satellite, 1, os.path.join(
            app.config["PLAYGROUND_INPUT"], files.filename))

        if type(tp1) == type(None):
            image_list.append('null')
        else:
            unique_filename = str(uuid.uuid4().hex)
            cv.imwrite(os.path.join(UPLOAD_FOLDER,
                                    unique_filename+'.tif'), tp1)
            outfile = os.path.splitext(os.path.join(
                UPLOAD_FOLDER, unique_filename))[0] + ".jpg"
            im = Image.open(os.path.join(
                'static/playground_output/', unique_filename+'.tif'))
            im.save(outfile, "JPEG", quality=100)

            image_list.append('static/playground_output/' +
                              unique_filename+'.jpg')

        tp2 = getImage(satellite, 2, os.path.join(
            app.config["PLAYGROUND_INPUT"], files.filename))
        if type(tp2) == type(None):
            image_list.append('null')
        else:
            unique_filename = str(uuid.uuid4().hex)
            cv.imwrite(os.path.join(UPLOAD_FOLDER,
                                    unique_filename+'.tif'), tp2)
            outfile = os.path.splitext(os.path.join(
                UPLOAD_FOLDER, unique_filename))[0] + ".jpg"
            im = Image.open(os.path.join(
                'static/playground_output/', unique_filename+'.tif'))
            im.save(outfile, "JPEG", quality=100)
            image_list.append('static/playground_output/' +
                              unique_filename+'.jpg')

        tp3 = getImage(satellite, 3, os.path.join(
            app.config["PLAYGROUND_INPUT"], files.filename))
        if type(tp3) == type(None):
            image_list.append('null')
        else:
            unique_filename = str(uuid.uuid4().hex)
            cv.imwrite(os.path.join(UPLOAD_FOLDER,
                                    unique_filename+'.tif'), tp3)
            outfile = os.path.splitext(os.path.join(
                UPLOAD_FOLDER, unique_filename))[0] + ".jpg"
            im = Image.open(os.path.join(
                'static/playground_output/', unique_filename+'.tif'))
            im.save(outfile, "JPEG", quality=100)
            image_list.append('static/playground_output/' +
                              unique_filename+'.jpg')

        tp4 = getImage(satellite, 4, os.path.join(
            app.config["PLAYGROUND_INPUT"], files.filename))
        if type(tp4) == type(None):
            image_list.append('null')
        else:
            unique_filename = str(uuid.uuid4().hex)
            cv.imwrite(os.path.join(UPLOAD_FOLDER,
                                    unique_filename+'.tif'), tp4)
            outfile = os.path.splitext(os.path.join(
                UPLOAD_FOLDER, unique_filename))[0] + ".jpg"
            im = Image.open(os.path.join(
                'static/playground_output/', unique_filename+'.tif'))
            im.save(outfile, "JPEG", quality=100)
            image_list.append('static/playground_output/' +
                              unique_filename+'.jpg')

        tp5 = getImage(satellite, 5, os.path.join(
            app.config["PLAYGROUND_INPUT"], files.filename))
        if type(tp5) == type(None):
            image_list.append('null')
        else:
            unique_filename = str(uuid.uuid4().hex)
            cv.imwrite(os.path.join(UPLOAD_FOLDER,
                                    unique_filename+'.tif'), tp5)
            outfile = os.path.splitext(os.path.join(
                UPLOAD_FOLDER, unique_filename))[0] + ".jpg"
            im = Image.open(os.path.join(
                'static/playground_output/', unique_filename+'.tif'))
            im.save(outfile, "JPEG", quality=100)
            image_list.append('static/playground_output/' +
                              unique_filename+'.jpg')

        tp6 = getImage(satellite, 6, os.path.join(
            app.config["PLAYGROUND_INPUT"], files.filename))
        if type(tp6) == type(None):
            image_list.append('null')
        else:
            unique_filename = str(uuid.uuid4().hex)
            cv.imwrite(os.path.join(UPLOAD_FOLDER,
                                    unique_filename+'.tif'), tp6)
            outfile = os.path.splitext(os.path.join(
                UPLOAD_FOLDER, unique_filename))[0] + ".jpg"
            im = Image.open(os.path.join(
                'static/playground_output/', unique_filename+'.tif'))
            im.save(outfile, "JPEG", quality=100)
            image_list.append('static/playground_output/' +
                              unique_filename+'.jpg')

        tp7 = getImage(satellite, 7, os.path.join(
            app.config["PLAYGROUND_INPUT"], files.filename))
        if type(tp7) == type(None):
            image_list.append('null')
        else:
            unique_filename = str(uuid.uuid4().hex)
            cv.imwrite(os.path.join(UPLOAD_FOLDER,
                                    unique_filename+'.tif'), tp7)
            outfile = os.path.splitext(os.path.join(
                UPLOAD_FOLDER, unique_filename))[0] + ".jpg"
            im = Image.open(os.path.join(
                'static/playground_output/', unique_filename+'.tif'))
            im.save(outfile, "JPEG", quality=100)
            image_list.append('static/playground_output/' +
                              unique_filename+'.jpg')

        response = {'status': 'success', 'imagePath': image_list}
        print(response)

        return jsonify(response)


# Playground end-------------------------------------------------------------------------------------------------------


# Segmentation start ----------------------------------------------------------------------------------------------------
@app.route("/segmentation-analysis.html",  methods=['GET'])
def page3():
    return render_template('segmentation-analysis.html')


@app.route('/segmentation', methods=['POST'])
def segmentation():
    if request.method == 'POST':
        print(tf.__version__)
        way = request.form.get('type')  # road or building
        place = request.form.get('city')  # paris or khartoum or vegas
        files = request.files["data"]
        IMAGE_UPLOADS = 'static/segmentation_upload/'
        app.config['IMAGE_UPLOADS'] = IMAGE_UPLOADS
        files.save(os.path.join(app.config["IMAGE_UPLOADS"], files.filename))
        if way == 'road':
            if place == 'paris':
                #my_model = tf.keras.models.load_model('./model/test_paris.h5')
                mrv = getmymodelvegas()
                mrv.load_weights('./model/paris_road2.h5')
                my_model = mrv

            elif place == 'khartoum':
                mrv = getmymodelvegas()
                mrv.load_weights('./model/khartoum_road2.h5')
                my_model = mrv
            elif place == 'vegas':
                # my_model = tf.keras.models.load_model('C:/Users/SilverWrath/Documents/FLASK_DL/test/model/vegas_road2.h5')
                mrv = getmymodelvegas()
                mrv.load_weights('./model/vegas_road2.h5')
                my_model = mrv

        elif way == 'building':
            if place == 'paris':
                mrv = getmymodelvegas()
                mrv.load_weights('./model/paris_building.h5')
                my_model = mrv
            elif place == 'khartoum':
                mrv = getmymodelvegas()
                mrv.load_weights('./model/khartoum_building.h5')
                my_model = mrv
            elif place == 'vegas':
                mrv = getmymodelvegas()
                mrv.load_weights('./model/vegas_building.h5')
                my_model = mrv

        shape_to_resize = (640, 640)

        filepath = os.path.join(app.config["IMAGE_UPLOADS"], files.filename)

        # tarr = cv2.resize(convert_into_rgb(filepath,'static/segmentation_upload/myImage.jpg'), shape_to_resize)

        unique_filenameinput = str(uuid.uuid4().hex)
        tarr = cv2.resize(convert_into_rgb(filepath, os.path.join(
            'static/segmentation_upload/', unique_filenameinput+'.jpg')), shape_to_resize)

        totest = np.expand_dims(tarr, 0)

        # tpred - stores output of model.

        # Here, my_model = model_road_paris
        tpred = my_model.predict(totest)
        unique_filename = str(uuid.uuid4().hex)

        myoutput = (tpred > 0.05).astype(np.uint8)
        print("\nmyoutput shape:", myoutput.shape)
        print("\nmyoutput shape:", np.squeeze(myoutput).shape)
        plt.imsave(os.path.join('static/segmentation_upload/',
                                unique_filename+'.png'), np.squeeze(myoutput), cmap="gray")

        print("\nSAVED SUCCESFULLY!!\n")
        response = {'Status': 'Success', 'input': os.path.join(
            'static/segmentation_upload/', unique_filenameinput+'.jpg'), 'output': os.path.join('static/segmentation_upload/', unique_filename+'.png')}
        print(response)

        return jsonify(response)

# segmentation ends-----------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True)
