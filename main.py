import os
import uuid
from flask import Flask, flash, request, redirect
import speech_recognition as sr
import subprocess
from openai_link import openai_completion
import miro.miro_conn as miro_conn

UPLOAD_FOLDER = './data'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/miroweb')
def miroweb():
    return app.send_static_file('miro_web_plugin.html')

@app.route('/miroweb/sidebar.html')
def miroweb_sidebar():
    return app.send_static_file('sidebar.html')


@app.route('/save-record', methods=['POST'])
def save_record() -> str:
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
    # save mp3 file
    file_name = str(uuid.uuid4()) + ".mp3"
    full_file_name = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    file.save(full_file_name)

    # Convert the mp3 file to wav file (sr.Recognizer() did not work with mp3)
    # todo : figure out way to eliminate this step (or check to stream blob directly into sr.Recognizer?)
    full_name_wav = full_file_name.replace(".mp3", ".wav")
    process = subprocess.Popen(['ffmpeg', '-i', full_file_name, full_name_wav])
    process.wait()

    r = sr.Recognizer()
    with sr.AudioFile(full_name_wav) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)

    # Delete the audio files
    os.remove(full_file_name)
    os.remove(full_name_wav)

    # Get the text in list from all sticky notes on the board
    # and use it as examples for GPT-3
    exist_stickies = miro_conn.get_stickies_text()
    for sticky in exist_stickies:
        text = f"{text}, example:'{sticky}'"

    # Get the text from openai
    answer = openai_completion(text, 2000)
    # add new sticky note on board
    miro_conn.create_sticky(answer)
    # return the answer to display on the web page
    return answer

if __name__ == '__main__':
    app.run()
