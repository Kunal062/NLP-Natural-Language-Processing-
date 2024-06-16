from flask import Flask,redirect, render_template, request,url_for
app = Flask(__name__)
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import joblib
ps = PorterStemmer()
swords = stopwords.words('english')

def clean_txt(sent):
    tokens = word_tokenize(sent)  # Step-1. Tokenize the text
    tokens = [token for token in tokens if token.isalnum()]  # Step-2 Remove the punctuations
    tokens = [token for token in tokens if token.lower() not in swords]  # Step-3 Remove stopwords
    tokens = [ps.stem(token) for token in tokens]  # step-4 Remove the suffixes
    return tokens 

classifier = joblib.load('classifier.model')
tfidf = joblib.load('preprocessor.model')

@app.route('/')
def student():
    return render_template('spamdetector.html')
@app.route('/spamfinder',methods=['GET','POST']) # type: ignore
def result():
    if request.method == 'POST':
        data = dict(request.form)
        message = tfidf.transform([data['message']])
        data['result'] = classifier.predict(message)[0]
        return render_template('spamoutput.html',data=data['result'])
    
    
if __name__ == '__main__':
    app.run(debug=True)