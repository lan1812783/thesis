from flask import request
from flask import jsonify
from flask import Flask, render_template
from flask import flash, redirect, url_for
from werkzeug.utils import secure_filename
import os

from accident_detection import get_prediction

UPLOAD_FOLDER = 'videos/uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def form_submitted():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        print(request.__dict__)
        filename = secure_filename(file.filename)
        filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filename)
        start_timestamp = float(request.form['start'])
        end_timestamp = float(request.form['end'])
        probability = get_prediction(filename, start_timestamp, end_timestamp)[0][0]
        return render_template('index.html', accidentProbability="%.2f" % probability, noAccidentProbability="%.2f" % (1 - probability))
    return redirect(request.url)

@app.route('/')
def index():
    return render_template('index.html', accidentProbability="", noAccidentProbability="")



# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('download_file', name=filename))
#     return
if __name__ == "__main__":
    app.run(debug=True)
