import tensorflow as tf
from tensorflow import keras

# Load your Keras model
model = keras.models.load_model('../model/densenet_best.h5')

# Save the model in TensorFlow SavedModel format
tf.saved_model.save(model, '../model/densenet_best.pb')