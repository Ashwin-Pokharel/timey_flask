from flask import Flask , jsonify , request
import cv2
import numpy
from PIL import Image
from io import BytesIO
from flask_cors import CORS
from decouple import config
import requests
import tensorflow as tf
import json

app = Flask(__name__)
CORS(app)

classes = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

@app.route('/hello' , methods=['POST'])
def helloworld():
    return "Hello World"


@app.route('/check_face_exists' , methods=['POST'])
def checkImage():
    blob_string = request.files['file'].read()
    if(len(blob_string) < 100):
         return jsonify({
            "face_exists":False
        })
    try:
        image = cv2.imdecode(numpy.fromstring(blob_string, dtype=numpy.uint8), cv2.IMREAD_GRAYSCALE)
    except Exception as e:
        return jsonify({
            "face_exists":False
        })
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        image,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30) 
    )
    
    if len(faces) <= 0:
         return jsonify({
            "face_exists":False
        })

    x , y , w , h = faces[0]
    face_image = image[y:y + h, x:x + w]
    resized_image = cv2.resize(face_image , (48 , 48) , interpolation=cv2.INTER_NEAREST)
    image = numpy.array(resized_image)
    image = numpy.expand_dims(image ,axis=2)
    print(image.shape)
    data = json.dumps({
        "instances": [image.tolist()]
    })
    headers = {"content_type":"application/json"}
    r = requests.post(config('TENSOR_URL') , data=data , headers=headers)
    tensor_response = r.json()
    tensor_response = tensor_response['predictions']
    score = tf.nn.softmax(tensor_response[0])
    label = classes[numpy.argmax(score)]
    certainty = numpy.max(score)
    return jsonify({
            "face_exists":True,
            "emotion":label,
            "certainty":str(certainty)
    })



        






