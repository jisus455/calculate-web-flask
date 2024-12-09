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


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == "GET":
        return render_template("settings.html")
    
    if request.method == 'POST':
        model_select = request.form.get('model')
        type_param = request.form.get('type')
        
        if type_param == 'Auto':
            route = path.abspath('static/temp/weather_forecast_data.csv')
            testsize = 0.25 
            logicModel = ActionModel(route, testsize)
            logicModel.fitModel()
            best_comb, best_score = logicModel.bestParam()
            return render_template("settings.html", algorithm=best_comb['algorithm'], 
            neighbors=best_comb['n_neighbors'], weights=best_comb['weights'], accuracy=best_score)

app.run(host="localhost", port=5000, debug=True)