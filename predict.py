import tensorflow as tf
classifierLoad = tf.keras.models.load_model('model.h5')
import os
import numpy as np
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input

base_dir = 'Dataset/'
catgo = os.listdir(base_dir)



#test_image = np.expand_dims(test_image, axis=0)
#result = classifierLoad.predict(test_image)
#ind = np.argmax(result)
#print(ind)
img = image.load_img('Dataset/Frogeye leaf spot/Frogeye leaf spot (1).jpg', target_size=(100, 100))
x = image.img_to_array(img)
x = preprocess_input(x)
# Rescale image.
#x = x / 255.
x = np.expand_dims(x, axis=0)
images = np.vstack([x])
result = classifierLoad.predict(images)
ind = np.argmax(result)
print(ind)
print(catgo[ind])