from flask import Flask,render_template,request
import searcher
app=Flask(__name__)
app.jinja_env.variable_start_string = '{['
app.jinja_env.variable_end_string = ']}'
se = searcher.Searcher()
@app.route('/search',methods=['POST'])
def search():
    key = request.form['getinfo']
    result = se.search(key, 'id')
    return render_template('search.html',result=result)
app.run(host='0.0.0.0',debug=True)