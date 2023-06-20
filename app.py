#import the necessary libraries

from flask import Flask, render_template, request
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from PIL import Image


#Initialized Flask App

app = Flask(__name__)

#route for the home page where users can upload an image
@app.route('/')
def home():
    return render_template('index.html')


# Add a route to serve static files
@app.route('/static/<path:filename>')
def static_files(filename):
    return app.send_static_file(filename)


#route to handle the image upload and perform the prediction
@app.route('/predict', methods=['POST'])
def predict():
    # Get the uploaded image from the request
    img_file = request.files['image']
    img_path = 'static/images/' + img_file.filename
    img_file.save(img_path)
    
    # Load and preprocess the image
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = preprocess_input(x)
    x = tf.expand_dims(x, axis=0)
    
    # Load the pre-trained model and make predictions
    model = ResNet50(weights='imagenet')
    preds = model.predict(x)
    decoded_preds = decode_predictions(preds, top=3)[0]
    
    # Render the predictions on a results page
    return render_template('results.html', predictions=decoded_preds, filename=img_file.filename)

#Run the Flask App
if __name__ == '__main__':
    app.run(port=5009)

