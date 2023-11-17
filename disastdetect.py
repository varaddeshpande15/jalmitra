import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
'''
pandas and numpy are not required here but were used to train the original model.
the model was trained on a web service optimised for training models (kaggle). 
since we didn't want to retrain the model everytime JalMitra is hosted on a webserver,
we froze the model, exported it and reimported it here. the development notebook for the model will also be uploaded to the github repository. 
'''

#also disabling AVX support because the localhost we ran the server on has a GPU (RTX 2060) - so we do not require CPU enhanced performance.
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from tensorflow import keras
import keras.utils as image_utils
from tensorflow.keras.applications.imagenet_utils import preprocess_input
from PIL import Image

model = keras.models.load_model('JM_issuedetectv1.keras')

def classifydisast (image_path):
    #show_image(image_path)
    image = image_utils.load_img(image_path, target_size=(224, 224))
    image = image_utils.img_to_array(image)
    image = image.reshape(1,224,224,3)
    image = preprocess_input(image)
    preds = model.predict(image)
    return preds
    
def calc_severity(image_path):
    pred_arr = classifydisast(image_path)
    print ("Possible Occurrences in Image: ")
    if pred_arr[0][0]>0:
        print ("Broken Pipeline - Severity 2")
        print ("Weight: ", pred_arr[0][0])
    if pred_arr[0][1]>0:
        print ("Pothole - Severity 3")
        print ("Weight: ", pred_arr[0][1])
    if pred_arr[0][2]>0:
        print ("Water Pollution - Severity 1")
        print ("Weight: ", pred_arr[0][2])
    if pred_arr[0][0] > pred_arr[0][1] and pred_arr[0][0] > pred_arr[0][2]:
        return 2
    elif pred_arr[0][1] > pred_arr[0][0] and pred_arr[0][1] > pred_arr[0][2]:
        return 3
    else:
        return 1

'''
def show_image(image_path):
    image = np.asarray(Image.open(image_path))
    print(image.shape)
    plt.imshow(image)
'''