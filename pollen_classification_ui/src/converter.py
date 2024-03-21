import tensorflow as tf
from tensorflow import keras

def convert_h5_to_pb(h5_model_path, pb_model_dir):
    # Load your Keras model
    model = keras.models.load_model(h5_model_path)

    # Save the model in TensorFlow SavedModel format
    tf.saved_model.save(model, pb_model_dir)

# Specify the path to your .h5 model and the directory where you want to save the .pb model
h5_model_path = '../model/mobilenet_16_03.h5'
pb_model_dir = '../model/mobilenet_pb'

convert_h5_to_pb(h5_model_path, pb_model_dir)