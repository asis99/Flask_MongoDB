import json
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-only-change-me")

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data.json"

# Create the MongoDB client only when a URI is configured.
mongo_client = None
submissions_collection = None
mongo_uri = os.getenv("MONGODB_URI")

if mongo_uri:
    try:
        mongo_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        database_name = os.getenv("MONGODB_DATABASE", "flask_assignment")
        collection_name = os.getenv("MONGODB_COLLECTION", "submissions")
        submissions_collection = mongo_client[database_name][collection_name]
        # Verify connectivity during startup so configuration errors are visible.
        mongo_client.admin.command("ping")
        print("Connected to MongoDB Atlas successfully.")
    except PyMongoError as exc:
        print(f"MongoDB connection could not be established: {exc}")
        submissions_collection = None


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api")
def api_data():
    """Read a JSON list from data.json and return it as an API response."""
    try:
        with DATA_FILE.open("r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        if not isinstance(data, list):
            return jsonify({"error": "The backend JSON file must contain a list."}), 500

        return jsonify(data), 200
    except FileNotFoundError:
        return jsonify({"error": "data.json was not found."}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "data.json contains invalid JSON."}), 500
    except OSError:
        app.logger.exception("Unable to read data.json")
        return jsonify({"error": "Unable to read API data."}), 500


@app.post("/submit")
def submit_form():
    """Validate form fields and save the submission to MongoDB."""
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    errors = []
    if not name:
        errors.append("Name is required.")
    if not email:
        errors.append("Email is required.")
    elif "@" not in email or "." not in email.rsplit("@", 1)[-1]:
        errors.append("Please enter a valid email address.")
    if not message:
        errors.append("Message is required.")

    if errors:
        return render_template(
            "index.html", errors=errors,
            form_data={"name": name, "email": email, "message": message}
        ), 400

    if submissions_collection is None:
        return render_template(
            "index.html",
            errors=["Database is not connected. Check your MongoDB Atlas URI and network access."],
            form_data={"name": name, "email": email, "message": message}
        ), 503

    document = {"name": name, "email": email, "message": message}

    try:
        submissions_collection.insert_one(document)
        return redirect(url_for("success"), code=303)
    except PyMongoError:
        app.logger.exception("MongoDB insert failed")
        return render_template(
            "index.html",
            errors=["Could not save your data. Please try again later."],
            form_data={"name": name, "email": email, "message": message}
        ), 500


@app.get("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
