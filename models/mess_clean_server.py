from flask import Flask, request, jsonify
from flask_cors import CORS 
import tensorflow as tf
import numpy as np
import io
from PIL import Image

app = Flask(__name__)
CORS(app)

MODEL_PATH = 'messycleanmodel.h5'
model = tf.keras.models.load_model(MODEL_PATH)

def preprocess_image(img):
    img = img.resize((150, 150))  # Resize the image to match model's expected sizing
    img = np.array(img) / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

@app.route('/messy_predict', methods=['POST'])
def predict():
    data = request.get_json()
    if 'imageUrl' not in data:
        return jsonify({'error': 'No image URL provided'}), 400
    
    filename = data['imageUrl']
    print(filename)
    
    try:
        # Process the image file using the filename
        img = Image.open(f'../server/uploads/{filename}')
        img_array = preprocess_image(img)
        prediction = model.predict(img_array)
        messy = float(prediction[0][0]) 
        return jsonify({'result': messy})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
