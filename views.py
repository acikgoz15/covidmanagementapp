from datetime import datetime
from flask import Flask, render_template, current_app, abort, request, redirect, url_for
import psycopg2
from movie import Movie


db = psycopg2.connect(user = "postgres",
                      password = "bomonti44",
                      host = "localhost",
                      port = "5432",
                      database = "dbcovid")
cursor = db.cursor()  
books=cursor.execute("SELECT * FROM Hospital_new order by hospital_id")

def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html",day = day_name)

def movies_page():
    db = current_app.config["db"]
    movies = db.get_movies()
    return render_template("movies.html", movies = sorted(movies))

def movie_page(movie_key):
    db = current_app.config["db"]
    movie = db.get_movie(movie_key)
    if movie is None:
        abort(404)
    return render_template("movie.html", movie=movie)


def movie_add_page():
    if request.method == "GET":
        return render_template(
            "movie_edit.html", min_year=1887, max_year=datetime.now().year
        )
    else:
        form_title = request.form["title"]
        form_year = request.form["year"]
        movie = Movie(form_title, int(form_year) if form_year else None)
        db = current_app.config["db"]
        movie_key = db.add_movie(movie)
        return redirect(url_for("movie_page", movie_key=movie_key))

def hospital_page():

    if request.method == "GET":
        return render_template(
            "hospital_add.html", min_year=1887, max_year=datetime.now().year, books = books, form = form
        )
    else:
        form_title = request.form["title"]
        form_year = request.form["year"]
        movie = Movie(form_title, int(form_year) if form_year else None)
        db = current_app.config["db"]
        movie_key = db.add_movie(movie)
        return redirect(url_for("movie_page", movie_key=movie_key))


# @app.route("\bookList")
# Def booklist():
# 	books=db.execute("SELECT * FROM booklist order by bookid")
#     return render_template("BookList.html", books=books)

# <table class="table">
#   <thead>
#     <tr>
#       <th scope="col">#</th>
#       <th scope="col">ISBN</th>
#       <th scope="col">Title</th>
#       <th scope="col">Author</th>
# 	  <th scope="col">Year</th>
# 	  <th scope="col">Star Rating</th>
#     </tr>
#   </thead>
# 	{% for book in books %}
# 	<tr>
# 	<th scope="row">{{book.bookid}}</th>
# 	<td>{{book.isbn}}
# 	</td>
# 	<td>{{book.title}}
# 	</td>
# 	<td>{{book.author}}
# 	</td>
# 	<td>{{book.year}}
# 	</td>
# 	</tr>
# 	{% endfor %}
# </table>