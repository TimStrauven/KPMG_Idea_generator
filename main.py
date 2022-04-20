import os
import uuid
from flask import Flask, flash, request, redirect
import speech_recognition as sr
import subprocess
from openai_link import openai_completion


UPLOAD_FOLDER = './data'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/save-record', methods=['POST'])
def save_record():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    file_name = str(uuid.uuid4()) + ".mp3"
    full_file_name = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    file.save(full_file_name)

    full_name_wav = full_file_name.replace(".mp3", ".wav")

    process = subprocess.Popen(['ffmpeg', '-i', full_file_name, full_name_wav])
    process.wait()

    r = sr.Recognizer()
    with sr.AudioFile(full_name_wav) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)

    os.remove(full_file_name)
    os.remove(full_name_wav)
    answer = openai_completion(text, 200)
    return answer

if __name__ == '__main__':
    app.run()
