from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
from app.extensions import mongo

# Flask Blueprint for webhook-related routes
webhook_bp = Blueprint("webhook", __name__)

# GitHub Webhook Receiver
@webhook_bp.route("/events", methods=["POST"])
def receive_event():

    # Parse JSON payload (fallback to empty dict if missing)
    payload = request.get_json(silent=True) or {}

    # FIX 1: Normalize event_type (GitHub sometimes sends empty string)
    event_type = request.headers.get("X-GitHub-Event") or "push"

    # FIX 2: action only exists for certain events(pull_request, issues, etc.)
    action = payload.get("action")

    doc = None

    # Push event
    if "commits" in payload and "ref" in payload:
        print("payload",payload)
        author = payload.get("pusher", {}).get("name", "unknown")
        branch = payload.get("ref", "").split("/")[-1]

        doc = {
            "event": "push",
            "message": f"{author} pushed to {branch}",
            "repository": payload.get("repository", {}).get("full_name"),
            "commits": payload.get("commits", []),
            "timestamp": datetime.utcnow()
        }

    # Pull request open/update
    elif event_type == "pull_request" and action in ["opened", "synchronize"]:
        pr = payload.get("pull_request", {})
        doc = {
            "event": "pull_request",
            "message": f"{pr['user']['login']} opened PR {pr['head']['ref']} → {pr['base']['ref']}",
            "repository": payload.get("repository", {}).get("full_name"),
            "timestamp": datetime.utcnow()
        }

    # Merged PR
    elif event_type == "pull_request":
        pr = payload.get("pull_request", {})
        if pr.get("merged"):
            doc = {
                "event": "merge",
                "message": f"{pr['user']['login']} merged {pr['head']['ref']} → {pr['base']['ref']}",
                "repository": payload.get("repository", {}).get("full_name"),
                "timestamp": datetime.utcnow()
            }

    # Nothing matched (easy in debugging)
    if not doc:
        print("⚠️ No document created for event:", event_type)
        return jsonify({"status": "ignored"}), 200


    # Final insert
    result = mongo.db.events.insert_one(doc)

    return jsonify({"status": "stored"}), 200

# Fetch latest events (UI)
@webhook_bp.route("/events", methods=["GET"])
def get_events():
    events = list(
        mongo.db.events
        .find({}, {"_id": 0})
        .sort("timestamp", -1)
        .limit(20)
    )
    return jsonify(events)

# UI Home Page
@webhook_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")
