from flask import Flask, render_template,request,redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
import cv2
from detect_landmark import detect_landmarks
import json
import glob
from dominate import document
from dominate.tags import *
import gmplot
import urllib
import urllib.request
import gmplot 
import re
import sys

patterns = {
    '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
    '[đ]': 'd',
    '[èéẻẽẹêềếểễệ]': 'e',
    '[ìíỉĩị]': 'i',
    '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
    '[ùúủũụưừứửữự]': 'u',
    '[ỳýỷỹỵ]': 'y'
}

def convert(text):
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
        # deal with upper case
        output = re.sub(regex.upper(), replace.upper(), output)
    return output
  
duongdan = "https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json?apiKey=lhgSmEU_UD6yeMyexdpmXy4ZSj6ajWOQMgiNPOKnSVw&mode=retrieveLandmarks&prox=" + "10.7582605" + "," + "106.7457218" + ",0.5"
response = urllib.request.urlopen(duongdan)
data = json.loads(response.read())
locdulieu = []
toado = []
ten = []
loai = []
for i in range(len(data["Response"]["View"][0]["Result"])):
    if (data["Response"]["View"][0]["Result"][i]["Location"]["Name"] not in locdulieu):
        loai.append(str(data["Response"]["View"][0]["Result"][i]["Location"]["LocationType"]))
        ten.append(str(data["Response"]["View"][0]["Result"][i]["Location"]["Name"]))
        toado.append([float(data["Response"]["View"][0]["Result"][i]["Location"]["DisplayPosition"]["Latitude"]), 
            float(data["Response"]["View"][0]["Result"][i]["Location"]["DisplayPosition"]["Longitude"])])
        locdulieu.append(data["Response"]["View"][0]["Result"][i]["Location"]["Name"])
gmap1 = gmplot.GoogleMapPlotter(10.7582605, 106.7457218, 13) 
gmap1.apikey = "AIzaSyCo3Ls0mMAoX2Lcq3158VZSVpLMc1PEJfk"
latitude = []
longitude = [] 
for i in range(len(toado)):
    latitude.append(toado[i][0])
    longitude.append(toado[i][1])
for i in range(len(latitude)):
    gmap1.marker(latitude[i], longitude[i], label = convert(ten[i]) + convert(loai[i]))
gmap1.scatter(latitude, longitude, '#FF0000', size = 40, marker = False)
gmap1.polygon(latitude, longitude, color = 'cornflowerblue')
gmap1.draw("map11.html")
for i in range(len(ten)):
    plot(ten[i], Latitude[i], longitude[i])
    
print(loai)
print(latitude)
print(longitude)