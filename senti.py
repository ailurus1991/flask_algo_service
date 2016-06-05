# encoding:utf-8
import goslate
import os
#  from matplotlib import pyplot,pylab as plt
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,jsonify
#  import numpy as np
#  import cv2
from rumor import RumorJudges, PreLoading, Add
import Image
import senseTime

import json

senti = Flask(__name__)
senti.config['UPLOAD_FOLDER'] = 'uploads/'
senti.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg','png','JPG'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in senti.config['ALLOWED_EXTENSIONS']

clf = PreLoading()
@senti.route('/')
@senti.route('/index')
def index():
    return render_template('index.html')

@senti.route('/multi', methods=['POST'])
def multi():
    # Get the name of the uploaded files
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            filename = file.filename
            print(file.filename)
            file.save(os.path.join(senti.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)

    file1 = uploaded_files[0]

    file_path = './uploads/'+file1.filename

    face_obj_list = senseTime.get_obj(senseTime.post_get(file_path))
#    print '图里有' + str(len(face_obj_list)) + '张脸'
#    for face in face_obj_list:
#        print face.gender
#        print face.age
#        print face.face_id

    #  file2 = uploaded_files[1]

    #  img_rgb = cv2.imread('uploads/'+file1.filename)

    #  print('uploads/'+file1.filename)
    face_infos = []
    face_id_list = []
    for face_obj in face_obj_list:
        face_id = face_obj.face_id
        face_rect = face_obj.ract
        face_attributes =  face_obj.attributes
        face_emotions = face_obj.emotions
        face_id_list.append(face_obj.face_id)
        d = {"face_id": face_id, "rect":face_rect, "face_attributes":face_attributes, "face_emotions":face_emotions}
        face_infos.append(d)

    verification = senseTime.get_verification(senseTime.verify(face_id_list[0], face_id_list[1]))


    #  print(type(img_rgb))
    return_dict = {}
    return_dict['file_path'] = file_path
    return_dict['face_dict'] = face_obj_list
    #return jsonify({"path":file_path, "rect":face_rect, "face_attributes":face_attributes, "face_emtions":face_emtions})# + face_infos
    print '---------------'
    print json.dumps({"path":file_path, "faces":face_infos, "verification":verification})
    return json.dumps({"path":file_path, "faces":face_infos})

    #  return redirect(url_for('uploaded_file',filename="tm"+filename))


@senti.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(senti.config['UPLOAD_FOLDER'], filename))
        print filename
        #  img = cv2.imread('uploads/'+filename)

    if 'Denoise Image' in request.form['submit']:
        print "hahah"
        return redirect(url_for('uploaded_file',filename="d"+filename))

    elif 'Detect Face' in request.form['submit']:
		faceCascade = cv2.CascadeClassifier('static/xml/haarcascade_frontalface_alt.xml')
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=5,minSize=(30, 30),flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
		for (x, y, w, h) in faces:
			cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
		im = Image.fromarray(img)
		im.save('uploads/face'+filename)
		return redirect(url_for('uploaded_file',filename="face"+filename))
    elif 'Smoothen Image' in request.form['submit']:
		kernel = np.ones((5,5),np.float32)/25
		dst = cv2.filter2D(img,-1,kernel)
		im = Image.fromarray(dst)
		im.save('uploads/smooth'+filename)
		return redirect(url_for('uploaded_file',filename="smooth"+filename))
    elif 'Detect Blue Colour' in request.form['submit']:
		# Convert BGR to HSV
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		# define range of blue color in HSV
		lower_blue = np.array([110,50,50])
		upper_blue = np.array([130,255,255])
		# Threshold the HSV image to get only blue colors
		mask = cv2.inRange(hsv, lower_blue, upper_blue)
		# Bitwise-AND mask and original image\
		res = cv2.bitwise_and(img,img, mask= mask)
		im = Image.fromarray(res)
		im.save('uploads/blue'+filename)
		return redirect(url_for('uploaded_file',filename="blue"+filename))

@senti.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(senti.config['UPLOAD_FOLDER'],
                               filename)

@senti.route('/api/v1/sentiment_upload/<message>', methods=['GET'])
def sentiment_upload(message):
    global clf
    text = message.encode('utf-8')
    label = 0
    content = u''
    if text[:5] == 'rumor':
        label = 1
        content = text[5:]
        Add(label, content)
        response = {'action' : 1}
        return jsonify(response)
    elif text[:5] == 'truth':
        label = 0
        content = text[5:]
        Add(label, content)
        response = {'action' : 0}
        return jsonify(response)
    elif text[:7] == 'retrain':
        clf = PreLoading()
        response = {'action' : 2}
        return jsonify(response)

    return 'I GOT YOU!'

@senti.route('/api/v1/sentiment/<message>', methods=['GET'])
def sentiment(message):
    text = RumorJudges(message.encode('utf-8'), clf)
    response = {'polarity' : text.polarity , 'subjectivity' : text.subjectivity}
    return jsonify(response)


@senti.route('/translate')
def translate():
    textVal = request.args.get('textVal', 0, type=str)
    langVal = request.args.get('langVal', 0, type=str)
    gs = goslate.Goslate()
    return jsonify(result=gs.translate(textVal,langVal))

if __name__ == "__main__":
    senti.run('0.0.0.0', debug=True, port=1111)
