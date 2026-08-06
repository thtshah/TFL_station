from flask import Flask, render_template
app = Flask(__name__)

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/<name>")
def welcome(name):
    print(name)
    return render_template("welcome.html", name=name)

@app.route("/about")
def about():
    sites = ['twitter', 'facebook', 'instagram', 'whatsapp']
    return render_template("about.html", sites=sites)

@app.route("/contact/<role>")
def contact(role):
    return render_template("contact.html", person=role)

if __name__=="__main__":
    app.run(port=8001)