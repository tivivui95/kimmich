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

USERNAME = 'admin'
PASSWORD = 'admin'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
@app.route('/', methods=['GET', 'POST'])
# Signin
def get_signin():
    if request.method == 'POST':
        username = request.form['fname']
        password = request.form['fpass']
    else:
        return render_template('signin.html')
    if username == USERNAME and password == PASSWORD:
        return redirect('/predict')
    else:
        return redirect('/signin')
@app.route('/register', methods=['GET', 'POST'])
# Register
def get_register():
    return render_template('register.html')
# history
@app.route('/history', methods=['GET','POST'])
def history():
    return render_template('history.html')
#chandoan
@app.route('/predict')
def index():
    return render_template('index.html')
@app.route('/1')
def huy1():
    return render_template("out.html")
@app.route('/2')
def huy2():
    return render_template("out1.html")
@app.route('/3')
def huy3():
    return render_template("out2.html")
@app.route('/4')
def huy4():
    return render_template("out3.html")
@app.route('/5')
def huy5():
    return render_template("out4.html")
@app.route('/6')
def huy6():
    return render_template("out5.html")
@app.route('/searching',methods=['GET', 'POST'])
def ui():
    return render_template("timxungquanh.html")
def bankinh():
    if request.methods =='POST':
        r = request.form['r']
        return redirect(redirect('/map'))
@app.route('/map')
def bando(r):
    # if request.method == 'POST':
    #     mount = request.form['mountain']
    #     river = request.form['river']
    #     museum = request.form['museum']
    #     church = request.form['church']
    #     r = request.form ['r'] 
    duongdan = "https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json?apiKey=lhgSmEU_UD6yeMyexdpmXy4ZSj6ajWOQMgiNPOKnSVw&mode=retrieveLandmarks&prox=" + "10.7582605" + "," + "106.7457218" + ","+str(r)
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
    gmap1 = gmplot.GoogleMapPlotter(10.7582605, 106.7457218, 15) 
    gmap1.apikey = "AIzaSyCo3Ls0mMAoX2Lcq3158VZSVpLMc1PEJfk"
    latitude = []
    longitude = [] 
    for i in range(len(toado)):
        latitude.append(toado[i][0])
        longitude.append(toado[i][1])
    for i in range(len(latitude)):
        gmap1.marker(latitude[i], longitude[i], label = convert(ten[i]) + convert(loai[i]))
    # if request.method == 'POST':
    #     church = request.form["church"]
    #     mountain = request.form["mountain"]
    # for i in range(len(ten)):
    #     gmap1.scatter(latitude[i],longitude[i],'#FF0000', size = 40, marker = False)
    #     gmap1.polygon(latitude, longitude, color = 'cornflowerblue')

    gmap1.scatter(latitude, longitude, '#FF0000', size = 40, marker = False)
    gmap1.polygon(latitude, longitude, color = 'cornflowerblue')
    gmap1.draw("./templates/map11.html") 
    print(loai)
    print(ten)
    return render_template("map11.html")
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file',
                                filename=filename))
@app.route('/templates/<filename>')
def uploaded_file(filename):
    PATH_TO_TEST_IMAGES_DIR = app.config['UPLOAD_FOLDER']
    TEST_IMAGE_PATHS = [os.path.join(PATH_TO_TEST_IMAGES_DIR,filename.format(i)) for i in range(1, 2)]
    for image_path in TEST_IMAGE_PATHS:
        
        out = detect_landmarks(image_path)
        x = out[0]
        longi= out[2]
        lati = out[1]
        print(image_path)
    gmap1 = gmplot.GoogleMapPlotter(longi, lati, 13 )
    gmap1.apikey = "AIzaSyCo3Ls0mMAoX2Lcq3158VZSVpLMc1PEJfk"
    gmap1.draw("map11.html") 
    if (x=="St. Basil's Cathedral"):
        return redirect("/1")
    elif (x =="Saigon Notre-Dame Basilica"):
        return redirect("/2")
    elif (x =="Ba Dinh Square"):
        return redirect("/3")
    elif (x =="Reunification Palace"):
        return redirect("/4")
    elif (x =="Temple Of Literature"):
        return redirect("/5")
    elif (x =="Halong Bay"):
        return redirect("/6") 
    else:
        return render_template("map11.html")       
    # photos = glob.glob(os.path.join("/uploads/",filename))
    # path_out="{{url_for('static', filename='"+str(filename)+"')}}"
    # # img = cv2.imread(image_path)
    # # cv2.imwrite(path_out,img)
    # with open("trichdan.json",encoding ="utf-8") as json_file:
    #     data = json.load(json_file)
    #     cap = data[x]
    # output = str(x)+": "+str(cap)
    # with document(title=x) as doc:
    #     h1(x,align="middle")
    #     div(img(src=path_out), _class='photo',align="middle")
    #     div(p(output),align="middle")

    # with open("templates/out.html",'w',encoding="utf-8") as f:
    #     f.write(doc.render())
    # return render_template("out.html")



if __name__ == '__main__':
    app.run(threaded = True,port=5000)
    
