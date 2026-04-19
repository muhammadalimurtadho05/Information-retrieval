from flask import Flask, render_template, request
from main import retrieval as rt  

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    query = ''
    data = ''
    if request.method == 'POST':
        query = request.form['query']
        data = rt(query)
    return render_template("index.html", query=query, data=data)

@app.route("/about")
def about():
    print("About Page")
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)