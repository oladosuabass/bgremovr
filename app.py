from distutils.log import debug
import os
from xmlrpc.client import ProtocolError
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import requests
from PIL import Image, ImageShow, ImageFile
from io import BytesIO
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

UPLOAD_FOLDER = ''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    def allowed_file(filename):
      return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if request.method == 'POST':
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
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            os.path.join(app.config['UPLOAD_FOLDER'], filename)
            return redirect(url_for('uploaded', name=filename))

    return render_template('upload.html')

@app.route('/uploaded/<name>')
def uploaded(name):
  p = os.path.join(UPLOAD_FOLDER, name)
  # open(p)
  try:
    response = requests.post(
      'https://api.remove.bg/v1.0/removebg',
      files={'image_file': open(p, 'rb')},
      data={'size': 'auto'},
      headers={'X-Api-Key': 'rpSnxLVxhXvMmU6a5TcNaiCj'},
    )
    if response.status_code == requests.codes.ok:
        with open('no-bg.png', 'wb') as out:
            out.write(response.content)

        cloudinary.config( 
          cloud_name = "bg-remove", 
          api_key = "683241377425755", 
          api_secret = "--SnMyUylv1MgRrx_eiU5As1jXU",
          secure = True
        )
        cloudinary.uploader.upload("no-bg.png", public_id = "no_bg")
        x = cloudinary.api.resources()
    else:
        print("Error:", response.status_code, response.text)
  except (Exception, ProtocolError, TypeError):
    return render_template('error.html', error=response.text)
  return render_template('uploaded.html', name=p, response=x['resources'][0]['secure_url'])

# if __name__ == '__main__':
#   app.run(debug=True)