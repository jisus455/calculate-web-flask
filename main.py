from flask import Flask, redirect, session, render_template, request
from werkzeug.utils import secure_filename
from os import path

from business.ActionModel import ActionModel

app = Flask(__name__, template_folder='templates', static_folder='static')

UPLOAD_FOLDER = path.abspath('static/temp') 
ALLOWED_EXTENSIONS = {'txt', 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("index.html")
    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect('/')

        file = request.files['file']
        # check If the user does not select a file
        if file.filename == '':
            return redirect('/')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
            
            filename = file.filename
            route = path.abspath(f'static/temp/{filename}') 
            testsize = request.form.get('testsize')

            logicModel = ActionModel(route, testsize)
            logicModel.fitModel()
            accuracy_score = logicModel.getScore()

            return render_template("index.html", score=accuracy_score)


app.run(host="localhost", port=5000, debug=True)