from flask import Flask, request, redirect, url_for, flash, render_template
import os
import subprocess

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = 'uploads/'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and file.filename.endswith('.cc'):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'walk.cc')
        file.save(filename)
        compile_and_execute()
        return redirect(url_for('results'))
    else:
        return redirect(request.url)

def compile_and_execute():
    subprocess.call("rm -f ./a.out", shell=True)
    retcode = subprocess.call(f"/usr/bin/g++ {app.config['UPLOAD_FOLDER']}/walk.cc", shell=True)
    if retcode:
        return
    subprocess.call("rm -f ./output", shell=True)
    retcode = subprocess.call("./testing.sh", shell=True)
    flash(f"Score: {retcode} out of 2 correct.")
    with open(f"{app.config['UPLOAD_FOLDER']}/walk.cc",'r') as fs:
        flash("Original submission:")
        flash(fs.read())

@app.route('/results')
def results():
    return render_template('res.html') 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)

