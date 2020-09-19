from flask import Flask , jsonify , request
import cv2
import numpy
import File

app = Flask(__name__)

@app.route('/hello' , methods=['POST'])
def helloworld():
    return "Hello World"


@app.route('/check_face_exists' , methods=['POST'])
def checkImage():
    new_file = request.files['file']
    npimg = numpy.fromfile(new_file , numpy.unit8)
    image = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
    )
    '''
    for (x , y , w , h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_color = image[y:y + h, x:x + w] 
        print("[INFO] Object found. Saving locally.") 
        cv2.imwrite(str(w) + str(h) + '_faces.jpg', roi_color) 
	'''

    if len(faces) <= 0:
        return {
            "face_exists": True
        }
    else:
        for(x , y  , w , h) in faces:
            cv2.rectangle(image , (x , y) , (x + w , y + h) , (0 , 255 , 0))
            new_image = image[y:y + h, x:x + w]

            





