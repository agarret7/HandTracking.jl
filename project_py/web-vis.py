from flask import Flask, render_template, Response, request, g
import os
import cv2
import numpy as np

app = Flask(__name__, template_folder='.')


image = cv2.imread("static/creepy.png", cv2.IMREAD_COLOR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed', methods=['GET', 'POST'])
def video_feed():
    global image
    if request.method == 'GET':
        def gen_frames():
            while True:
                ret, buf = cv2.imencode('.jpg', image)
                frame = buf.tobytes()
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    elif request.method == 'POST':
        f = request.files["image"]
        image_arr = np.fromfile(request.files["image"], np.uint8)
        image = cv2.imdecode(image_arr, cv2.IMREAD_COLOR)
        return Response("success", 200)
        # TODO process image visualization before displaying
