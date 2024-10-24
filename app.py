from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# In-memory storage for books
books = []


# redirects to the github repository of this project
@app.route("/github")
def github():
    return redirect("https://github.com/FreeMan-join/myflaskapp")


# new changes for better performance
# ************************************************
# ************************************************


@app.route("/new")
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return "Welcome to the Library!"


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        file = request.files["photo"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            books.append({"title": title, "author": author, "photo": filename})
        return redirect(url_for("view_books"))
    return render_template("add_book.html")


@app.route("/view_books")
def view_books():
    return render_template("view_books.html", books=books)


@app.route("/delete_book/<int:book_index>", methods=["POST"])
def delete_book(book_index):
    if 0 <= book_index < len(books):
        books.pop(book_index)
    return redirect(url_for("view_books"))


if __name__ == "__main__":
    app.run(debug=True)
