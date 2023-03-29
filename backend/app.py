from flask import Flask, request,jsonify
from flask_cors import CORS, cross_origin
import io
import cv2
import numpy as np
import base64
from io import BytesIO
import cv2
import json
import tensorflow as tf
from PIL import Image

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/upload', methods=['POST'])
@cross_origin(supports_credentials=True)
def upload_image():
    if 'image' not in request.files:
        return json.dumps({'message': 'No image'}), 400, {'ContentType': 'application/json'}

    image_file = request.files['image']
    image_bytes = image_file.read()
    img_pil = Image.open(image_file)
    img_pil_re = img_pil.resize((100,100),resample=Image.BICUBIC)
    img_pil_re= np.array(img_pil_re)
    img_pil_re = img_pil_re.reshape(1,100,100,3)

    image_cv2 = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

    img_resize = cv2.resize(image_cv2,(100,100))
    #img = cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB)
    img = img_resize.reshape(1,100,100,3)
    fruit_dict={0:'apple',1:'banana',2:'orange'}
    quality_dict={0:'Fresh',1:'Rotten'}
    label = {0: 'fresh apple', 1:'fresh banana', 2:'fresh orange', 3:'rotten apple', 4:'rotten banana', 5:'rotten orange'}
    # Example: resize image using cv2
    #image_cv2_resized = cv2.resize(image_cv2, (640, 480))
    quality_model = tf.keras.models.load_model('fruit_classifier.h5')
    fruit_model = tf.keras.models.load_model('local_fruit_final.h5')
        
    q_prediction = quality_model.predict(img_pil_re)
    op_arg = np.argmax(q_prediction, axis=1)
    message_q = quality_dict[op_arg[0]]#str(op_arg[0])

    f_prediction = fruit_model.predict(img_pil_re)
    op_arg1 = np.argmax(f_prediction, axis=1)
    message_f = fruit_dict[op_arg1[0]]#str(op_arg[0])
     

    return json.dumps({'message': message_q+' '+message_f}), 200, {'ContentType': 'application/json'}

@app.route('/', methods=['GET'])
def hello():
    return jsonify({'message':'Hello'})


if __name__ == '__main__':
    app.run(debug=True)