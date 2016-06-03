#!/usr/bin/env python
# encoding: utf-8
import requests
import locale
import ast
locale.setlocale(locale.LC_ALL, 'en_US.utf8')


#  r = requests.post("https://v1-api.visioncloudapi.com/face/detection?api_id=fef59d1492a64b5ab5df102b8a3b6067&api_secret=cd8738e236c9470d837025ec4b3b9b6e", files = files, data=params)
#  print r.text
def post_get(filepath):
    files = {'file':open(str(filepath), 'rb')}
    params = {'emotions':'1', 'attributes':'1'}
    r = requests.post('https://v1-api.visioncloudapi.com/face/detection?api_id=fef59d1492a64b5ab5df102b8a3b6067&api_secret=cd8738e236c9470d837025ec4b3b9b6e', files = files, data = params)
    print r.text
    return ast.literal_eval(r.text)


class Face(object):
    def __init__(self, face_id, ract, attributes, emotions, eye_dist):
        self.face_id = face_id
        self.ract = ract
        #  self.attributes = attributes
        #  self.emotions = emotions
        self.attributes = attributes
        self.emotions = emotions
        self.eye_dist = eye_dist
        self.age = attributes['age']
        self.gender = attributes['gender']
        self.attractive =  attributes['attractive']
        self.smile = attributes['smile']
        self.angry = emotions['angry']
        self.calm = emotions['calm']
        self.disgust = emotions['disgust']
        self.happy = emotions['happy']
        self.sad = emotions['sad']
        self.surprised = emotions['surprised']
        self.confused = emotions['confused']
        self.squint = emotions['squint']
        self.screaming = emotions['screaming']
        self.scared = emotions['scared']

def get_obj(r_text):
    face_obj_list = []
    for face in r_text['faces']:
        current_face = Face(face['face_id'], face['rect'], face['attributes'], face['emotions'], face['eye_dist'])
        face_obj_list.append(current_face)
    return face_obj_list
