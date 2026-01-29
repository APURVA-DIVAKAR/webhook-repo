import os
from flask import Flask
from dotenv import load_dotenv

# Import MongoDB extension (Flask-PyMongo)
from app.extensions import mongo

# Import webhook routes blueprint
from app.webhook.routes import webhook_bp

load_dotenv()

# Flask App Factory
def create_app():  

    # Create Flask app instance
    app = Flask(__name__)

    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise RuntimeError("MONGO_URI not set")

    app.config["MONGO_URI"] = mongo_uri

    # Attaches MongoDB client to the app context
    mongo.init_app(app)

    # Register application routes
    app.register_blueprint(webhook_bp)

    return app
