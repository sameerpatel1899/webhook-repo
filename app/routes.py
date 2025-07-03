from flask import render_template, jsonify, request, current_app
from app import create_app
from datetime import datetime

app = create_app()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    print("🔔 Webhook received!")
    data = request.get_json()
    print(f"📦 Webhook data: {data}")

    try:
        db = current_app.config['MONGO_DB']
        if db is None:
            raise Exception("MongoDB not connected")

        event_type = request.headers.get('X-GitHub-Event')

        # Determine message based on type
        timestamp = datetime.utcnow()
        msg = ""

        if event_type == "push":
            author = data.get("pusher", {}).get("name", "Unknown")
            branch = data.get("ref", "").split("/")[-1]
            msg = f'{author} pushed to {branch} on {timestamp.strftime("%d %b %Y - %I:%M %p UTC")}'

        elif event_type == "pull_request":
            action = data.get("action")
            author = data.get("pull_request", {}).get("user", {}).get("login", "Unknown")
            from_branch = data.get("pull_request", {}).get("head", {}).get("ref")
            to_branch = data.get("pull_request", {}).get("base", {}).get("ref")
            msg = f'{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp.strftime("%d %b %Y - %I:%M %p UTC")}'

            # Optional: if action is 'closed' and 'merged', treat as merge
            if data.get("pull_request", {}).get("merged", False):
                msg = f'{author} merged branch {from_branch} to {to_branch} on {timestamp.strftime("%d %b %Y - %I:%M %p UTC")}'
                event_type = "merge"

        # Save to MongoDB
        db.events.insert_one({
            "type": event_type,
            "message": msg,
            "timestamp": timestamp
        })

        print("✅ Event saved")
        return jsonify({'status': 'received'}), 200

    except Exception as e:
        print(f"❌ Error saving to DB: {e}")
        return jsonify({'error': str(e)}), 500




# from flask import render_template, jsonify, request, current_app
# from app import create_app

# app = create_app()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     # Webhook endpoint - will be implemented in Phase 3
#     print("🔔 Webhook received!")
#     data = request.get_json()
#     print(f"📦 Webhook data: {data}")
#     return jsonify({'status': 'received'}), 200

# @app.route('/api/events')
# def get_events():
#     # API endpoint to get events - will be implemented in Phase 5
#     try:
#         if current_app.config['MONGO_DB'] is not None:
#             # This will be implemented in Phase 5
#             return jsonify({'events': [], 'message': 'MongoDB connected, ready for events'})
#         else:
#             return jsonify({'events': [], 'message': 'MongoDB not connected'})
#     except Exception as e:
#         return jsonify({'events': [], 'error': str(e)})






@app.route('/api/events')
def get_events():
    try:
        db = current_app.config['MONGO_DB']
        if db is None:
            raise Exception("MongoDB not connected")

        events_cursor = db.events.find().sort("timestamp", -1).limit(10)
        events = [{"message": e["message"], "timestamp": e["timestamp"].isoformat()} for e in events_cursor]

        return jsonify({"events": events})

    except Exception as e:
        return jsonify({"events": [], "error": str(e)})
