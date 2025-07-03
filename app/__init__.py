from flask import Flask
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # MongoDB connection
    try:
        mongo_uri = os.getenv('MONGO_URI')
        client = MongoClient(mongo_uri)
        client.admin.command('ping')
        print("✅ MongoDB connected successfully!")
        app.config['MONGO_CLIENT'] = client
        app.config['MONGO_DB'] = client.webhook_user
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        app.config['MONGO_CLIENT'] = None
        app.config['MONGO_DB'] = None
    
    return app