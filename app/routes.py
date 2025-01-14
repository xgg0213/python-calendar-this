from flask import Blueprint, render_template
from .templates import *

# Create the Blueprint
bp = Blueprint(
    "main",  # Name of the Blueprint
    __name__,  # Import name (required for locating resources)
    url_prefix="/"  # Top-level route
)

@bp.route("/")
def main():
    return render_template("main.html")