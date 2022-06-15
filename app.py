from flask import Flask, render_template, request
import joblib
import numpy as np

model = joblib.load(open('model.pkl','rb'))

app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/prediction', methods=['POST'])
def prediction():
    if request.method == 'POST':
        TSH =(request.form["TSH"])
        FTI =(request.form["FTI"])
        TT4 =(request.form["TT4"])
        T3 =(request.form["T3"])
        query_hypothyroid =(request.form["query_hypothyroid"])
        on_thyroxine =(request.form["on_thyroxine"])
        sex =(request.form["sex"])
        pregnant =(request.form["pregnant"])
        psych =(request.form["psych"])
        arr=np.array([[TSH, FTI ,TT4, T3,query_hypothyroid,on_thyroxine,sex,pregnant,psych]])
        prediction = model.predict(arr)

    return render_template('after.html',data=prediction)

if __name__ == "__main__":
    app.run()