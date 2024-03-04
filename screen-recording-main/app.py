from flask import Flask, render_template, request, jsonify
import pyautogui
import cv2
import numpy as np
import os
import shutil
import webbrowser
import datetime
from multiprocessing import Process
from time import sleep

app = Flask(__name__)
def save_video():
    try:
        now = datetime.datetime.now()
        filename = f"output_{now.strftime('%Y%m%d_%H%M%S')}.avi"
        shutil.copy("output.avi", filename)
        os.remove("output.avi")  # Remove the temporary file
        return filename
    except Exception as e:
        print(f"Error saving video: {e}")
        return None
# Function to record screen
def record_screen_v():
    SCREEN_SIZE = tuple(pyautogui.size())
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    fps = 12.0
    out = cv2.VideoWriter("output.avi", fourcc, fps, SCREEN_SIZE)
    record_seconds = 100000
    for i in range(int(record_seconds * fps)):
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)
        if (open("cache","r").read() == "stop"):
            open("cache","w").write("")
            break
    cv2.destroyAllWindows()
    out.release()

# This function starts the recording
def rec():
    if ("__cache__" in os.listdir()):
        open("__cache__","w").write("")
    else:
        open("__cache__","a").write("")
    while True:
        y=open("__cache__","r").read()
        if (y == "do"):
            record_screen_v()
        else:
            sleep(2)

# Function for releasing recorded video
def save_video():
    try:
        now = datetime.datetime.now()
        filename = f"output_{now.strftime('%Y%m%d_%H%M%S')}.avi"
        shutil.copy("output.avi", filename)
        return filename
    except Exception as e:
        print(f"Error saving video: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-recording', methods=['POST'])
def start_recording():
    open("__cache__", "w").write("do")
    open("cache", "w").write("")
    return jsonify({"message": "Recording started."})

@app.route('/stop-recording', methods=['POST'])
def stop_recording():
    open("__cache__", "w").write("")
    open("cache", "w").write("stop")
    return jsonify({"message": "Recording stopped."})

@app.route('/release-video', methods=['POST'])
def release_video():
    saved_file = save_video()
    if saved_file:
        return jsonify({"message": "File saved.", "filename": saved_file})
    else:
        return jsonify({"error": "Failed to save video."}), 500

@app.route('/open-github')
def open_github():
    try:
        webbrowser.open("https://github.com/abhineetraj1")
        return jsonify({"message": "GitHub opened successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    t = Process(target=rec)
    t.start()
    app.run(debug=True)
