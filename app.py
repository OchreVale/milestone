import flask
import random
app = flask.Flask(__name__)

# set up a separate route to serve the index.html file generated
# by create-react-app/npm run build.
# By doing this, we make it so you can paste in all your old app routes
# from Milestone 2 without interfering with the functionality here.
bp = flask.Blueprint(
    "bp",
    __name__,
    template_folder="./static/react",
)

# route for serving React page
@bp.route("/")
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

app.run()
