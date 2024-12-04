import os
from flask import Flask
from flask_cors import CORS
from schema.db_routes import db_routes
from db_operations.routes import op_routes
from media_operations.docs_routes import docs_routes


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(db_routes, url_prefix="/db")
app.register_blueprint(op_routes, url_prefix="/")
app.register_blueprint(docs_routes, url_prefix="/media")

@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World")
    return f"Hello {name}!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))

