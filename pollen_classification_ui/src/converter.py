import tensorflow as tf

# Load your TensorFlow model
model = tf.keras.models.load_model('../model/model.h5')

# Convert the model to TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the TensorFlow Lite model
with tf.io.gfile.GFile('model.tflite', 'wb') as f:
    f.write(tflite_model)