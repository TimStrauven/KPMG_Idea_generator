import os
import uuid
from flask import Flask, flash, request, redirect
import speech_recognition as sr
import subprocess
from utils.idea_generator import OpenAI_Generator
from utils.preprocessing import Preprocessing
import miro.miro_conn as miro_conn

UPLOAD_FOLDER = './data'
if os.path.exists('./data') == False:
    os.mkdir('./data')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/user.html')
def root():
    return app.send_static_file('user.html')

@app.route('/facilitator.html')
def facilitator():
    return app.send_static_file('facilitator.html')

@app.route('/miro_user_plugin.html')
def miroweb_user():
    return app.send_static_file('miro_user_plugin.html')

@app.route('/miro_fac_plugin.html')
def miroweb_fac():
    return app.send_static_file('miro_fac_plugin.html')

@app.route('/icon.svg')
def get_icon():
    return app.send_static_file('icon.svg')

@app.route('/save_facilitator', methods=['POST'])
def save_facilitator():
    workshop = int(request.form['workshop'])
    with open('data/facilitator_status.txt', 'w') as f:
        f.write(str(workshop))
    return "done"

@app.route('/loaduser', methods=['GET'])
def load_user():
    # TODO final version should use push, but js timer is ok for demo
    workshop = 0
    with open('data/facilitator_status.txt', 'r') as f:
        workshop = int(f.read())
    return f"{workshop}"

@app.route('/str-to-gpt', methods=['POST'])
def str_to_gpt_post() -> str:
    question = request.form['question']
    temp = int(request.form['temp'])
    print(temp)
    answer = text_to_return(question, temp)
    return answer

@app.route('/avalanche', methods=['POST'])
def avalanche_post() -> str:
    question = request.form['question']
    preprocessor = Preprocessing(question)
    text_list = preprocessor.avalanche()
    for idea in text_list:
         # Get the text from openai
        answer = OpenAI_Generator(idea, 1).generate_idea()
        # add new sticky note on board
        miro_conn.create_sticky(answer)
        # TODO needs to be completed with option to select a single letter
    return "done"

@app.route('/save-record', methods=['POST'])
def save_record() -> str:
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    temp = int(request.form['temp'])
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

    answer = text_to_return(text, temp)
    return answer

def text_to_return(text: str, temp: int) -> str:
    # Get the text in list from all sticky notes on the board
    # and use it as examples for GPT-3
    preprocessor = Preprocessing(text)

    if temp == 0:
        text = preprocessor.process_crazy_text()
    elif temp == 1:
        text = preprocessor.process_normal_text()

    # exist_stickies = miro_conn.get_stickies_text()
    #for sticky in exist_stickies:
    #    text = f'{text}. Example:{sticky}'
    text = f'{text}.'
    # Get the text from openai
    answers = OpenAI_Generator(text, 10).generate_idea()
    # add new sticky note on board
    for answer in answers:
        miro_conn.create_sticky(answer)
    # return the answer to display on the web page
    return answer

if __name__ == '__main__':
    app.run()
