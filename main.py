from flask import Flask, request, render_template,session
import sqlite3
from database import auth,change_password,get_homeworks,add_homework
import os

app = Flask(__name__)

app.secret_key = "admin"


@app.route("/", methods = ['GET', 'POST'])
def start_page():
    if(request.method == "GET"):
        return render_template("login.html", isNotLogin = False)
    else:
        data = request.form # dict
        #data = request.get_json() # {"username": "anatoly"} - dict
        #data = request.data # {"username": "anatoly"} - str
        if(auth(data["username"], data["password"])):
            session["username"] = data["username"]
            session["password"] = data["password"]
            session['homeworks'] = get_homeworks(data['username'])
            return render_template("index.html", name = session["username"])
        else:
            return render_template("login.html", isNotLogin = True)
    
@app.route("/change-password", methods = ['POST'])
def change_password_database():
    data = request.form
    username = session.get("username")
    if not username:
        return "Error",404

    if(change_password(username, data['old-password'], data['new-password'])):
        return "Success", 200
    else:
        return "Error", 400
@app.route("/homework", methods = ["GET"])
def homework_page():
    if(request.method == "GET"):
        username = session.get("username")
        homeworks = get_homeworks(username)
        if not username:
            return "Error", 404
        return render_template("homework-page.html", name = username, homeworks = homeworks)

@app.route("/create-homework", methods=["POST"])
def homework_page_post():
    username = session.get("username") # admin
    if not username:
        return "Error", 404

    title = request.form.get("title")
    description = request.form.get("description")
    image = request.files.get("image")
    image_path = None
    
    if image and image.filename != "":
        filename = image.filename

        upload_folder = os.path.join("static", "uploads")

        os.makedirs(upload_folder, exist_ok=True)
        
        filepath = os.path.join(upload_folder,filename)
        image.save(filepath)
        image_path = f"uploads/{filename}"

    add_homework(username,title,description,image_path)

    homeworks = get_homeworks(username)

    session["homeworks"] = homeworks

    return render_template("homework.html", name=username, homeworks=homeworks)

app.run(host = "0.0.0.0", port = 3000)
