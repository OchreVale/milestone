'''
@author: Benny Lisangi
main.py is a flask app that interacts with The Movie Database and the wikipedia APIs.
It gets the poster, the title, and the id of the query term.
The query term is also used to get the wikipedia page id necessary to generating
link for the query term. The Movie DataBase alsoprovides the trailer id which
corresponds to YouTube video id.The trailer id is fetched in fetch_YT and then
 used to access the trailer on YouTube if that trailer '''
import os
import flask
from flask_sqlalchemy import SQLAlchemy
import requests
from flask_login import LoginManager, login_required, login_user, current_user, UserMixin
from dotenv import find_dotenv, load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import functions
import random
load_dotenv(find_dotenv())
URL_TMDB = "https://api.themoviedb.org/3/search/movie"
QP_TMDB = {
    "api_key":os.getenv("TMDB_KEY")
}

app = flask.Flask(__name__)
app.secret_key = os.getenv("sk")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db= SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'
app.secret_key = bytes(os.getenv("session_key"), "utf8")

class Users(db.Model, UserMixin):
    '''
Creates the User table in the database. When creating an instance of this class aka a row in this
table, you must passage a firstname, lastname, email, and password to the constructor.
For example User(fistname=firstname, lastname = lastname, email = email, and password =
password)
    '''
    __tablename__:'Users'
    id = db.Column(db.Integer, primary_key= True, nullable = False)
    firstname = db.Column(db.String(50), nullable= False)
    lastname = db.Column(db.String(50), nullable= False)
    email = db.Column(db.String(150), unique = True ,nullable=False)
    password = db.Column(db.String(350), nullable=False)

    def __repr__(self):
        return f"<{self.id}:{self.firstname}>"
    def hash_pwd(self, pwd):
        '''
    This method using a werkzeug function generate_password_hash to hash passwords before
    storing them in the database. It takes as a parameter the password to be hashed and
    sets the password attribute of the User class to be that hashed password.
        '''
        self.password = generate_password_hash(pwd)
    def check_password(self, pwd):
        '''
        Checks the user's saved password against the submitted password (pwd). Returns true
        if they match and false otherwise.
        '''
        return check_password_hash(self.password, pwd)
class Reviews(db.Model):
    '''
    Creates the reviews table and stores data about submitted reviews and ratings to the
    database.
    '''
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    title = db.Column(db.String(50), nullable = False)
    movie_id = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, nullable = False)
    rating = db.Column(db.Integer)
    review = db.Column(db.String(280), nullable = False)
    def __repr__(self) -> str:
        '''
        returns a string representation of this of class.
        '''
        return f"<{self.movie_id}:{self.user_id}>"
    def comment(self):
        '''
        returns the review attribute of this class.'''
        return self.review
db.create_all()
@app.route("/")
def login():
    '''
    The main route of the app. It routes to the login page.
    '''
    return flask.render_template("login.html")
@login_manager.user_loader
def loaduser(user_id):
    '''
    loads this user's info in the session to allow for authentification.
    '''
    return db.session.query(Users).get(user_id)
@app.route("/validate", methods = ["POST"])
def validate_form():
    '''
    Validates the form submitted in the home page.
    '''
    if flask.request.method == "GET":
        return flask.redirect("/")
    data = flask.request.form
    pwd = data["password"]
    email = data["email"]
    query = Users.query.filter_by(email = email)
    user = query.first()
    if  user is not None and user.check_password(pwd):
        u_id = loaduser(user.id)
        login_user(u_id)
        return flask.redirect("/search")
    else:
        flask.flash("Wrong email address or wrong password")
        return flask.redirect("/")
@app.route("/signup")
def signup():
    '''
    renders the html page that allows the user to create an account.
    '''
    return flask.render_template("sign_up.html")
@app.route("/New User", methods = ["POST", "GET"])
def add_user():
    '''
    adds the user to the databse. Taking information submitted from /signup route.
    '''
    if flask.request.method == "POST":
        data = flask.request.form
        email = data["email"]
        query = Users.query.filter_by(email = email)
        user = query.first()
        if user is None:
            data = flask.request.form
            pwd = data["password"]
            first = data["firstname"]
            last = data['lastname']
            user = Users(firstname = first, lastname = last, email = email)
            user.hash_pwd(pwd)
            db.session.add(user)
            db.session.commit()
            return flask.render_template("login.html")
        flask.flash(f"An account is already associated with {user.email}")
        return flask.redirect("/New User")
    return flask.render_template("login.html")
@app.route("/search", methods = ["POST", "GET"])
@login_required
def form():
    '''
    This is the root directory and only displays a form that prompts a user to seach for a movie
    for a movie.
    '''

    return flask.render_template("form.html")
@app.route("/Home", methods = ["POST", "GET"])
def home():
    '''
    takes the input from the root, performs a movie search, fetches the id, title,
    poster path, pass parameters to fetch_wiki and fetch_YT, finally it displays the information.
    '''
    form_data = None
    if flask.request.method == "POST":
        form_data = flask.request.form["movie"]
        QP_TMDB["query"] = form_data
        response_ = requests.get(URL_TMDB, params= QP_TMDB)
        results = response_.json()["results"]
        poster_path = []
        titles = []
        images = []
        links = []
        youtube = []
        for  i ,result in enumerate (results):
            poster_path.append(result["poster_path"])
            titles.append(result["title"])
            youtube.append(functions.query_pararms(name = titles[i],id_ =str(result["id"])))

            links.append(functions.fetch_wiki(titles[i]))
            if poster_path[i] is not None:
                images.append("http://image.tmdb.org/t/p/w500"+result["poster_path"])
            else:
                break
        return flask.render_template("home.html", search = form_data, length = len(images),
                image = images, title = titles, link = links, YouTube = youtube)
    return flask.render_template("login.html")
    #getting data from wikipedia
random = []
@app.route("/delete", methods=["POST", "GET"])
@login_required
def delete():
    '''
    deletes comment from the database'''
    if flask.request.method == "GET":
        flask.redirect("/search")
    data = flask.request.args.get("cid")
    cid_ = data
    query = Reviews.query.filter_by(id = cid_).first()
    db.session.delete(query)
    db.session.commit()
    name = flask.request.args.get("name")
    id_ = flask.request.args.get("id")
    path = flask.request.args.get("path")
    redirect = f"/review and comments?name={name}&id={id_}&path={path}"
    return flask.redirect(redirect)
@app.route("/review and comments", methods = ["GET", "POST"])
@login_required
def display_review_page():
    '''
    displays the review page, and allows user to enter review.
    '''
    name = flask.request.args.get("name")
    id_ = flask.request.args.get("id")
    path = flask.request.args.get("path")
    youtube = functions.fetch_yt(id_)
    redirect = f"/review and comments?name={name}&id={id_}&path={path}"
    if flask.request.method == "POST":
        form_data = flask.request.form
        rating = form_data["rating"]
        comments = form_data["comments"]
        query = Reviews.query.filter_by(movie_id = id_, user_id = current_user.id).first()
        if query is None:
            record = Reviews(title = name, movie_id = int(id_),
            user_id = current_user.id, rating = int(rating), review = comments)
            db.session.add(record)
        else:
            query.rating = int(rating)
            query.review = comments
    db.session.commit()
    query = Reviews.query.filter_by(movie_id = id_).all()
    reviews = []
    user_ids = []
    comments_ids = []
    score = 0
    for record in query:
        user = Users.query.filter_by(id = record.user_id).first()
        reviews.append(f"\"{record.review}\" ~ {user.firstname}")
        score += record.rating
        user_ids.append(record.user_id)
        comments_ids.append(record.id)
    if len(query) > 0:
        score /= len(query)
    return flask.render_template("review.html", name = name,
            link = youtube, redirect_back = redirect,
            score = score, comments = reviews, path = path,
            user_ids = user_ids, comments_ids = comments_ids,
            current_user_id = current_user.id, len_ = len(reviews),mid =id_)
bp = flask.Blueprint(
    "bp",
    __name__,
    template_folder="./static/react",
)

# route for serving React page
@bp.route("/react")
def index():
    # NB: DO NOT add an "index.html" file in your normal templates folder
    # Flask will stop serving this React page correctly
    return flask.render_template("index.html")
@bp.route("/home", methods =["POST", "GET"])
def Home():
    facts = [
         "I am a man.",
         "I am fluent in 3 languages.",
         "I love playing chess on my free time."
     ]
    random_choice = random.choice(facts)
    return flask.jsonify({"fact":random_choice})

app.register_blueprint(bp)
app.run(os.getenv("IP","0.0.0.0"), port = int(os.getenv("PORT","8080")),debug=True)
