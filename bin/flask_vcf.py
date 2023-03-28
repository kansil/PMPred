from flask import Flask, render_template, request, flash, redirect
from werkzeug.utils import secure_filename
import subprocess
from subprocess import Popen, PIPE
import os, shutil

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

app.config['UPLOAD_FOLDER'] = "annovar/example/"

@app.route("/index1", methods=['GET', 'POST'])
def index1():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        for file in files:
            filename = secure_filename(file.filename)
            file.save(app.config['UPLOAD_FOLDER']+ filename)
            file = open(app.config['UPLOAD_FOLDER'] + filename, "r")
            command = ['nextflow', 'run', 'main.nf']
            work = "work/"
            input_file = "annovar/example/"
            command2 = ["find", work, "-type", "d", "-empty", "-delete"]
            command3 = ["find", input_file, "-type", "f", "-delete"]
            subprocess.call(command, stdin=file)
            subprocess.call(command2)
            subprocess.call(command3)
            df = pd.read_csv("uploads/PMPred.csv",sep=',')
        return render_template('content.html',tables=[df.to_html(classes='variants')],titles = ['Variant Table'])
    return render_template("index1.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug = True)
