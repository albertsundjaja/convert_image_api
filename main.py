import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import random
import string

UPLOAD_FOLDER = 'temp'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
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

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            
            return redirect(request.url)

        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            random_name = create_random_name(file.filename)
            filename = secure_filename(random_name)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            resp = jsonify({'filename':filename})
            return resp
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''