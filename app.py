from flask import Flask, request, render_template, redirect, flash
from werkzeug import secure_filename
import homer
from config import *
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'Your scalloped potatoes are F**KED'

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/homerfy', methods=['POST'])
def homerfy():
    file = request.files['bg_img']
    extension = os.path.splitext(file.filename)[1]
    if file and extension.lower() in ALLOWED_EXTENSIONS:
        filename = secure_filename(file.filename)
        full_path = os.path.join(app.config['UPLOAD_FOLDER'], str(time.time()).replace('.', '') + filename)
        file.save(full_path)
        img = homer.new(full_path)
        return redirect(img)
    elif not file:
        flash('D\'oh! You forgot to upload a file.')
        return render_template('index.html')
    elif extension.lower() not in ALLOWED_EXTENSIONS:
        flash('Only .jpg, .jpeg, and .png files are allowed.')
        return render_template('index.html')


    flash('Something went wrong.')
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
