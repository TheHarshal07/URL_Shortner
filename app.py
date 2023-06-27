from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
class Urls(db.Model):
    id = db.Column("id_", db.Integer, primary_key=True)
    long = db.Column("long",db.String())
    short = db.Column("short",db.String(3))

    def __init__(self, long, short):
        self.long = long
        self.short = short

@app.before_request
def creat_tables():
    db.create_all()

def shorten_url():
    letter = string.ascii_lowercase + string.ascii_uppercase
    while True:
        rand_letter = random.choices(letter,k=3)
        rand_letter = "".join(rand_letter)                          # Over here we are joining the the randome letters
        short_url = Urls.query.filter_by(short=rand_letter).first() # bascially here we are checking if the short column has same letter as we have random letter,'''
                                                                    # if yes then do not use this combination and then again will form another combination of letters 
        if not short_url:
            return rand_letter
                    
@app.route("/")
def home():
    return render_template("urlfile.html")

@app.route("/index", methods=['POST','GET'])
def index():
    if request.method == "POST":
        url_receive = request.form["ur"]
        found_url = Urls.query.filter_by(long=url_receive).first() # here we are checking wether the url is exist or not
        if found_url:
            return redirect(url_for("display_short_url", url=found_url.short))
        else:
            short_url = shorten_url()
            new_url = Urls(url_receive,short_url)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url", url=short_url))
    else:
        return render_template("urlfile.html")
@app.route('/display/<url>')
def display_short_url(url):
    return render_template("shorturl.html", short_url_display=url)

@app.route('/<short_url>')
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return f'<h1> Url does not exis </h1>'


if __name__ == "__main__":
    app.run(debug=True)