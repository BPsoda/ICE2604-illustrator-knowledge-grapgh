from flask import Flask,render_template,request,redirect,url_for
import pymysql
import json
import requests
import json,random
import searcher
global result
with open("2.json","rb") as f:
    b=json.load(f)
app=Flask(__name__)
app.jinja_env.variable_start_string = '{['
app.jinja_env.variable_end_string = ']}'
se = searcher.Searcher()
# print(json.dumps(result[0], indent=2, separators=(',', ';')))
@app.route('/home',methods=['GET','POST'])
def vue():
    global result
    return render_template('final_project1.html')
@app.route('/a')
def jsonpic():
    return json.dumps([urls for urls in random.sample(b["data"],20) if "master" in urls["src"]])
@app.route('/search',methods=['GET','POST'])
def search():
    global result
    if (request.form):
        key = request.form['getinfo']
        result = se.search(key, 'id')
        print(result)
        return render_template('search.html',result=result)
    return render_template("search.html");
@app.route('/picture')
def showpicture():
    return render_template("showpic.html",initli=[urls["src"] for urls in random.sample(b["data"],20) if "master" in urls["src"]])
app.run(host='0.0.0.0',debug=True)
