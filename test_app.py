from app.routes import app
import requests
import json

def test_app():
    with app.test_client() as client:
        # Test home page
        response = client.get('/')
        print(f"✅ Home page status: {response.status_code}")
        
        # Test webhook endpoint
        test_data = {'test': 'data'}
        response = client.post('/webhook', 
                             data=json.dumps(test_data),
                             content_type='application/json')
        print(f"✅ Webhook endpoint status: {response.status_code}")
        
        # Test API endpoint
        response = client.get('/api/events')
        print(f"✅ API endpoint status: {response.status_code}")
        print(f"📦 API response: {response.get_json()}")

if __name__ == '__main__':
    test_app()