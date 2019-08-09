import os
from flask import Flask, flash, request, redirect, url_for, jsonify, send_from_directory, render_template
from werkzeug.utils import secure_filename
import random
import string
from flask_cors import CORS
import img_converter

UPLOAD_FOLDER = 'temp'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
CORS(app)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """
    Check if file is an allowed type by its extension

    :param filename: the filename e.g. image.png
    :returns: boolean
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_random_name(filename, name_length=15):
    """
    Create a random name for saving file in the temp folder, the filename is a mix of ascii lower and uppercase

    :param filename: the filename e.g. image.png
    :param name_length: the length of the random name generated
    :returns: a string of random filename with the same extension e.g. zxfSSDF.png
    """
    _, file_extension = os.path.splitext(filename)
    letters = string.ascii_lowercase + string.ascii_uppercase
    random_name = ''.join(random.choice(letters) for i in range(name_length)) + file_extension
    return random_name

@app.route('/upload_file', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'error':'File key is not in sent form data'})
        return resp, 400

    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        resp = jsonify({'error':'Please select a file'})
        return resp, 400
        
    if file and allowed_file(file.filename):
        random_name = create_random_name(file.filename)
        filename = secure_filename(random_name)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img_converter.convert_image(filename)

        resp = jsonify({'filename':filename})
        return resp, 200

@app.route('/download_file/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/static/js/<filename>', methods=['GET'])
def static_files_js(filename):
    return send_from_directory('static/js', filename)

@app.route('/static/css/<filename>', methods=['GET'])
def static_files_css(filename):
    return send_from_directory('static/css', filename)
