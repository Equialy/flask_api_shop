from flask import Blueprint,  render_template
import logging


logger = logging.getLogger(__name__)

index_app = Blueprint(
    "index_app",
    __name__,
    template_folder="templates"
)

app = index_app

@app.route("/", endpoint="index")
def index_view():
    return render_template("index.html")
