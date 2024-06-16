from flask import Flask,redirect, render_template, request,url_for
app = Flask(__name__)


@app.route('/')
def student():
    return render_template('read_marks.html')


@app.route('/result',methods = ['POST','GET']) # type: ignore
def result():
    if request.method == 'POST':
        n1 = int(request.form['phy'])
        n2 = int(request.form['che'])
        n3 = int(request.form['math'])
        average = (n1+n2+n3)//3
        return render_template('result.html',result=average)



if __name__ == '__main__':
    app.run(debug=True)